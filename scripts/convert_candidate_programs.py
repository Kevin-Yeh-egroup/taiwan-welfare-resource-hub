#!/usr/bin/env python
"""Convert manually reviewed foundation candidate pages into resource records."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path
from typing import Any

SOURCE_ID = "sfaa-social-welfare-foundations"
PROGRAM_ID_PREFIX = "foundation-program-"
GENERATED_SOURCE_TYPE = "foundation-program-page"


def today() -> str:
    return dt.date.today().isoformat()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def clean(value: Any) -> str | None:
    if value is None:
        return None
    text = re.sub(r"\s+", " ", str(value)).strip()
    return text or None


def unique(values: list[Any], limit: int | None = None) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for value in values:
        text = clean(value)
        if not text or text in seen:
            continue
        seen.add(text)
        output.append(text)
        if limit and len(output) >= limit:
            break
    return output


def index_candidates(paths: list[Path]) -> dict[str, dict]:
    candidates: dict[str, dict] = {}
    for path in paths:
        payload = load_json(path)
        if payload.get("mode") != "candidate-only":
            raise ValueError(f"{path} must remain candidate-only.")
        for candidate in payload.get("candidates", []):
            candidate_id = candidate.get("id")
            if candidate_id in candidates:
                raise ValueError(f"Duplicate candidate id across files: {candidate_id}")
            candidates[candidate_id] = candidate
    return candidates


def foundation_records(resources: dict) -> dict[str, dict]:
    records = {}
    for record in resources.get("records", []):
        record_id = record.get("id")
        if isinstance(record_id, str) and record_id.startswith("sfaa-foundation-"):
            records[record_id] = record
    return records


def program_id(candidate_id: str) -> str:
    match = re.match(r"sfaa-foundation-([a-z]\d{4})-candidate-([a-f0-9]+)$", candidate_id)
    if not match:
        safe = re.sub(r"[^a-zA-Z0-9]+", "-", candidate_id).strip("-").lower()
        return f"{PROGRAM_ID_PREFIX}{safe}"
    foundation_code, digest = match.groups()
    return f"{PROGRAM_ID_PREFIX}{foundation_code}-{digest}"


def has_current_year_signal(candidate: dict) -> bool:
    signals = set(candidate.get("currentYearSignals") or [])
    return bool(signals & {"2026", "115年", "115年度"})


def confidence(candidate: dict) -> str:
    return "source-dated" if has_current_year_signal(candidate) else "checked"


def contact_from_foundation(foundation: dict, candidate: dict) -> dict:
    contact = dict(foundation.get("contact") or {})
    website = clean(foundation.get("contact", {}).get("website")) or clean(candidate.get("website"))
    if website:
        contact["website"] = website
    return {key: value for key, value in contact.items() if clean(value)}


def merge_need_tags(override: dict, candidate: dict, foundation: dict) -> list[str]:
    values: list[Any] = []
    values.extend(override.get("needTags") or [])
    values.extend(candidate.get("matchedKeywords") or [])
    values.extend(
        [
            foundation.get("name") or candidate.get("foundationName"),
            candidate.get("linkText"),
            candidate.get("pageTitle"),
            "人工確認方案",
            "民間資源",
            "今年度仍需電話確認",
        ]
    )
    values.extend(candidate.get("currentYearSignals") or [])
    return unique(values, limit=36)


def default_how_to_apply(candidate: dict) -> list[str]:
    steps = [
        "開啟來源頁確認今年度受理狀態、服務區域、名額與申請期限。",
        "依頁面準備申請表、資格證明、身分資料與需求說明。",
        "送件或前往服務前，先以電話或 Email 確認最新規則，避免白跑一趟。",
    ]
    if "線上申請" in " ".join(candidate.get("matchedKeywords") or []):
        steps.insert(1, "若來源頁提供線上申請，先確認系統是否開放與是否需註冊。")
    return steps


def build_summary(override: dict, candidate: dict) -> str:
    summary = clean(override.get("summary")) or clean(candidate.get("summary"))
    if not summary:
        return "此為人工確認後轉入的民間社會福利方案頁；申請前仍需向單位確認最新資格、文件與受理狀態。"
    if len(summary) > 260:
        return summary[:257].rstrip() + "..."
    return summary


def build_record(override: dict, candidate: dict, foundation: dict, reviewed_at: str) -> dict:
    candidate_id = candidate["id"]
    candidate_url = clean(candidate.get("pageUrl"))
    if not candidate_url:
        raise ValueError(f"{candidate_id} missing pageUrl")

    audiences = unique((override.get("audiences") or []) + (candidate.get("audiences") or []), limit=8)
    service_categories = unique(
        (override.get("serviceCategories") or [])
        + (candidate.get("serviceCategories") or [])
        + ["民間社福資源", "方案級民間資源"],
        limit=8,
    )

    return {
        "id": program_id(candidate_id),
        "name": clean(override.get("name")) or clean(candidate.get("linkText")) or clean(candidate.get("pageTitle")) or candidate_id,
        "summary": build_summary(override, candidate),
        "provider": foundation.get("provider") or foundation.get("name") or candidate.get("foundationName"),
        "jurisdiction": foundation.get("jurisdiction") or "全國",
        "county": foundation.get("county") or candidate.get("county") or "全國",
        "districts": foundation.get("districts") or [],
        "audiences": audiences,
        "serviceCategories": service_categories,
        "needTags": merge_need_tags(override, candidate, foundation),
        "eligibility": clean(override.get("eligibility"))
        or "此頁已由候選頁人工確認為方案或服務頁；實際資格、服務區域、名額與是否仍受理，以來源頁和電話確認為準。",
        "howToApply": override.get("howToApply") or default_how_to_apply(candidate),
        "documents": override.get("documents")
        or ["身分證明文件", "戶籍或居住資料", "弱勢、身障、低收或中低收等資格證明（如有）", "來源頁指定申請表與附件"],
        "contact": contact_from_foundation(foundation, candidate),
        "source": {
            "id": SOURCE_ID,
            "url": candidate_url,
            "type": GENERATED_SOURCE_TYPE,
            "candidateId": candidate_id,
        },
        "freshness": {
            "lastChecked": today(),
            "sourceUpdatedAt": None,
            "confidence": confidence(candidate),
            "notes": (
                f"Converted from manually reviewed candidate {candidate_id} on {reviewed_at}. "
                f"Candidate signals: {', '.join(candidate.get('currentYearSignals') or ['none'])}. "
                "Application details still require source-page or phone confirmation before use."
            ),
        },
        "programReview": {
            "candidateId": candidate_id,
            "reviewedAt": reviewed_at,
            "selectionPolicy": "manual-allowlist",
        },
    }


def remove_generated(records: list[dict]) -> list[dict]:
    return [
        record
        for record in records
        if not (
            str(record.get("id", "")).startswith(PROGRAM_ID_PREFIX)
            and record.get("source", {}).get("type") == GENERATED_SOURCE_TYPE
        )
    ]


def convert(resources_path: Path, candidate_paths: list[Path], allowlist_path: Path, out_path: Path) -> tuple[int, int]:
    resources = load_json(resources_path)
    allowlist = load_json(allowlist_path)
    candidates = index_candidates(candidate_paths)
    foundations = foundation_records(resources)

    programs = allowlist.get("programs") or []
    reviewed_at = clean(allowlist.get("reviewedAt")) or today()
    if not programs:
        raise ValueError(f"{allowlist_path} has no programs.")

    records = remove_generated(resources.get("records", []))
    existing_ids = {record.get("id") for record in records}
    generated: list[dict] = []
    errors: list[str] = []

    for override in programs:
        candidate_id = clean(override.get("candidateId"))
        if not candidate_id:
            errors.append("Allowlist item missing candidateId.")
            continue
        candidate = candidates.get(candidate_id)
        if not candidate:
            errors.append(f"Allowlist candidate not found: {candidate_id}")
            continue
        foundation_id = candidate.get("foundationId")
        foundation = foundations.get(foundation_id)
        if not foundation:
            errors.append(f"Foundation record not found for {candidate_id}: {foundation_id}")
            continue
        record = build_record(override, candidate, foundation, reviewed_at)
        if record["id"] in existing_ids:
            errors.append(f"Generated record id collides with existing record: {record['id']}")
            continue
        existing_ids.add(record["id"])
        generated.append(record)

    if errors:
        raise ValueError("\n".join(errors))

    resources["records"] = records + generated
    resources["generatedAt"] = dt.datetime.now(dt.timezone.utc).isoformat()
    write_json(out_path, resources)
    return len(records), len(generated)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--resources", type=Path, required=True)
    parser.add_argument("--candidates", type=Path, nargs="+", required=True)
    parser.add_argument("--allowlist", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        base_count, generated_count = convert(args.resources, args.candidates, args.allowlist, args.out)
    except Exception as exc:  # noqa: BLE001 - command-line script should print friendly failures.
        print(f"Conversion failed: {exc}", file=sys.stderr)
        return 1
    print(f"Converted {generated_count} reviewed foundation program pages. Total records: {base_count + generated_count}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
