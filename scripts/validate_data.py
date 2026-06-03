#!/usr/bin/env python
"""Validate public data files before preview or deployment."""

from __future__ import annotations

import json
import sys
import urllib.parse
from pathlib import Path

REQUIRED_RECORD_FIELDS = [
    "id",
    "name",
    "summary",
    "provider",
    "county",
    "audiences",
    "serviceCategories",
    "eligibility",
    "howToApply",
    "contact",
    "source",
    "freshness",
]


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def valid_url(url: str | None) -> bool:
    if not url:
        return True
    parsed = urllib.parse.urlparse(url)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def validate_candidate_file(path: Path, errors: list[str]) -> None:
    candidates = load(path)
    if candidates.get("mode") != "candidate-only":
        errors.append(f"{path.name} must remain candidate-only.")
    candidate_ids = set()
    for index, candidate in enumerate(candidates.get("candidates", []), start=1):
        candidate_id = candidate.get("id")
        if not candidate_id:
            errors.append(f"{path.name} candidate {index} missing id.")
        elif candidate_id in candidate_ids:
            errors.append(f"{path.name} duplicate candidate id: {candidate_id}")
        candidate_ids.add(candidate_id)
        if not candidate.get("foundationId"):
            errors.append(f"{path.name} candidate {candidate_id} missing foundationId.")
        if candidate.get("reviewStatus") != "candidate-review-required":
            errors.append(f"{path.name} candidate {candidate_id} must require review.")
        if candidate.get("canConvertToResource") is not False:
            errors.append(f"{path.name} candidate {candidate_id} must not be auto-convertible.")
        if not valid_url(candidate.get("pageUrl")):
            errors.append(f"{path.name} candidate {candidate_id} has invalid pageUrl.")
        if not candidate.get("matchedKeywords"):
            errors.append(f"{path.name} candidate {candidate_id} has no matched keywords.")


def main() -> int:
    root = Path.cwd()
    resources_path = root / "data" / "resources.json"
    sources_path = root / "data" / "sources.json"
    errors: list[str] = []

    for path in [resources_path, sources_path, root / "index.html", root / "robots.txt", root / "vercel.json"]:
        if not path.exists():
            errors.append(f"Missing required file: {path}")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    resources = load(resources_path)
    sources = load(sources_path)
    source_ids = {source["id"] for source in sources.get("sources", [])}
    record_ids = set()

    for index, record in enumerate(resources.get("records", []), start=1):
        for field in REQUIRED_RECORD_FIELDS:
            if field not in record:
                errors.append(f"Record {index} missing field: {field}")
        record_id = record.get("id")
        if record_id in record_ids:
            errors.append(f"Duplicate record id: {record_id}")
        record_ids.add(record_id)

        if not valid_url(record.get("contact", {}).get("website")):
            errors.append(f"Record {record_id} has invalid contact website.")
        if not valid_url(record.get("source", {}).get("url")):
            errors.append(f"Record {record_id} has invalid source URL.")
        if record.get("source", {}).get("id") not in source_ids:
            errors.append(f"Record {record_id} source id is not in data/sources.json.")
        if not record.get("audiences"):
            errors.append(f"Record {record_id} has no audience.")
        if not record.get("serviceCategories"):
            errors.append(f"Record {record_id} has no service category.")

    for candidates_path in sorted((root / "data").glob("foundation-program-candidates*.json")):
        validate_candidate_file(candidates_path, errors)

    if "noindex,nofollow,noarchive" not in (root / "index.html").read_text(encoding="utf-8"):
        errors.append("index.html is missing review-stage noindex meta.")
    if "X-Robots-Tag" not in (root / "vercel.json").read_text(encoding="utf-8"):
        errors.append("vercel.json is missing X-Robots-Tag header.")

    if errors:
        print("Validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Validation passed: {len(record_ids)} records, {len(source_ids)} sources.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
