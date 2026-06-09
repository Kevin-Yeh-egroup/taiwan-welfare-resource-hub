#!/usr/bin/env python
"""Build QA and operating artifacts for the welfare resource hub."""

from __future__ import annotations

import datetime as dt
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

COUNTY_ORDER = [
    "臺北市",
    "新北市",
    "桃園市",
    "臺中市",
    "臺南市",
    "高雄市",
    "基隆市",
    "新竹市",
    "新竹縣",
    "苗栗縣",
    "彰化縣",
    "南投縣",
    "雲林縣",
    "嘉義市",
    "嘉義縣",
    "屏東縣",
    "宜蘭縣",
    "花蓮縣",
    "臺東縣",
    "澎湖縣",
    "金門縣",
    "連江縣",
]

NEEDS = [
    {
        "id": "income",
        "label": "低收入／生活扶助",
        "terms": ["低收入", "中低收入", "生活扶助", "社會救助", "資格審核"],
        "localExpected": True,
        "priority": "high",
    },
    {
        "id": "emergency",
        "label": "急難救助",
        "terms": ["急難", "急難救助", "急難紓困", "事故", "臨時生活"],
        "localExpected": True,
        "priority": "high",
    },
    {
        "id": "medical",
        "label": "醫療／健保補助",
        "terms": ["醫療", "健保", "保費", "住院", "看護", "就醫"],
        "localExpected": True,
        "priority": "high",
    },
    {
        "id": "disability",
        "label": "身心障礙服務",
        "terms": ["身心障礙", "身障", "輔具", "生活補助", "復康巴士", "交通接送"],
        "localExpected": True,
        "priority": "high",
    },
    {
        "id": "elder",
        "label": "長者／老人津貼",
        "terms": ["老人", "長者", "中低收入老人", "老人生活津貼", "老人福利"],
        "localExpected": True,
        "priority": "high",
    },
    {
        "id": "long_care",
        "label": "長照／照顧者",
        "terms": ["長照", "照顧者", "家庭照顧者", "喘息", "居家服務", "1966"],
        "localExpected": False,
        "priority": "medium",
    },
    {
        "id": "child_family",
        "label": "兒少／家庭支持",
        "terms": ["兒少", "兒童", "少年", "托育", "家庭支持", "脆弱家庭", "特殊境遇"],
        "localExpected": True,
        "priority": "medium",
    },
    {
        "id": "housing",
        "label": "租屋／居住壓力",
        "terms": ["租金", "租屋", "房租", "住宅補貼", "承租"],
        "localExpected": False,
        "priority": "medium",
    },
    {
        "id": "education",
        "label": "學費／助學",
        "terms": ["學費", "助學", "獎學", "清寒", "學生", "學雜費"],
        "localExpected": False,
        "priority": "medium",
    },
]


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def display_values(values):
    return [value for value in values or [] if value and str(value).lower() != "none"]


def record_text(record: dict) -> str:
    parts = [
        record.get("id"),
        record.get("name"),
        record.get("summary"),
        record.get("provider"),
        record.get("jurisdiction"),
        record.get("county"),
        *(record.get("districts") or []),
        *display_values(record.get("audiences")),
        *display_values(record.get("serviceCategories")),
        *(record.get("needTags") or []),
        record.get("eligibility"),
        *(record.get("howToApply") or []),
        *(record.get("documents") or []),
    ]
    for item in record.get("benefitItems") or []:
        parts.extend([item.get("label"), item.get("amount"), item.get("note")])
    for item in record.get("applicationConditions") or []:
        parts.extend([item.get("label"), item.get("requirement"), item.get("note")])
    return " ".join(str(part) for part in parts if part).lower()


def is_foundation(record: dict) -> bool:
    source_type = record.get("source", {}).get("type")
    return source_type == "foundation-program-page" or str(record.get("id", "")).startswith("sfaa-foundation-")


def is_private(record: dict) -> bool:
    return is_foundation(record)


def is_central(record: dict) -> bool:
    if is_private(record):
        return False
    source_type = record.get("source", {}).get("type", "")
    scope = f"{record.get('county', '')} {record.get('jurisdiction', '')}"
    if re.search(r"全國|全省|中央", scope):
        return True
    return bool(re.search(r"official-(portal|hotline|program|annual-standard|faq|service-network)", source_type))


def is_local(record: dict) -> bool:
    if is_private(record) or is_central(record):
        return False
    source_type = record.get("source", {}).get("type", "")
    provider = f"{record.get('provider', '')} {source_type}"
    return bool(re.search(r"政府|社會局|社會處|衛生局|公所|open-data|official-map|official-local|official-online", provider))


def has_dated_source(record: dict) -> bool:
    confidence = record.get("freshness", {}).get("confidence", "")
    return bool(record.get("freshness", {}).get("sourceUpdatedAt")) or confidence in {
        "source-dated",
        "source-dated-list",
        "checked",
        "official-report",
        "official-statistical-brief",
    }


def source_level(record: dict) -> str:
    confidence = record.get("freshness", {}).get("confidence", "")
    source_type = record.get("source", {}).get("type", "")
    if confidence == "needs-local-confirmation":
        return "confirm"
    if "cross-check" in source_type:
        return "cross-check"
    if has_dated_source(record):
        return "strong"
    if is_central(record) or is_local(record):
        return "entry"
    return "review"


def matches_need(record: dict, need: dict) -> bool:
    text = record_text(record)
    return any(term.lower() in text for term in need["terms"])


def classify_pair(local_count: int, strong_count: int, confirm_count: int, central_count: int, private_count: int, need: dict) -> str:
    if strong_count:
        return "local-strong"
    if local_count:
        return "local-needs-confirmation" if confirm_count else "local-entry"
    if central_count:
        return "central-ok" if not need["localExpected"] else "central-fallback"
    if private_count:
        return "private-only"
    return "gap"


def status_score(status: str, need: dict) -> int:
    base = {
        "gap": 100,
        "central-fallback": 78,
        "private-only": 62,
        "local-needs-confirmation": 46,
        "local-entry": 28,
        "central-ok": 16,
        "local-strong": 0,
    }.get(status, 0)
    if need["priority"] == "high":
        base += 12
    if not need["localExpected"] and status == "central-fallback":
        base -= 28
    return max(base, 0)


def build_coverage(records: list[dict]) -> dict:
    central_by_need = {
        need["id"]: [record for record in records if is_central(record) and matches_need(record, need)]
        for need in NEEDS
    }
    rows = []
    summary = Counter()
    gap_candidates = []

    for county in COUNTY_ORDER:
        cells = []
        for need in NEEDS:
            local_records = [
                record
                for record in records
                if record.get("county") == county and is_local(record) and matches_need(record, need)
            ]
            private_records = [
                record
                for record in records
                if record.get("county") == county and is_private(record) and matches_need(record, need)
            ]
            central_records = central_by_need[need["id"]]
            strong_records = [record for record in local_records if source_level(record) == "strong"]
            confirm_records = [record for record in local_records if source_level(record) in {"confirm", "cross-check"}]
            status = classify_pair(
                len(local_records),
                len(strong_records),
                len(confirm_records),
                len(central_records),
                len(private_records),
                need,
            )
            summary[status] += 1
            sample = (strong_records or local_records or central_records or private_records)[:3]
            cell = {
                "needId": need["id"],
                "needLabel": need["label"],
                "status": status,
                "score": status_score(status, need),
                "localCount": len(local_records),
                "strongLocalCount": len(strong_records),
                "confirmLocalCount": len(confirm_records),
                "centralFallbackCount": len(central_records),
                "privateCount": len(private_records),
                "sampleRecords": [
                    {
                        "id": record.get("id"),
                        "name": record.get("name"),
                        "sourceLevel": source_level(record),
                        "sourceUrl": record.get("source", {}).get("url"),
                    }
                    for record in sample
                ],
            }
            cells.append(cell)
            if cell["score"] >= 60:
                gap_candidates.append({
                    "county": county,
                    "needId": need["id"],
                    "needLabel": need["label"],
                    "status": status,
                    "score": cell["score"],
                    "query": " ".join(need["terms"][:2]),
                    "reason": "完全缺口" if status == "gap" else "需要地方細節或官方來源強化",
                })
        rows.append({"county": county, "cells": cells})

    total_pairs = len(COUNTY_ORDER) * len(NEEDS)
    strong_pairs = summary["local-strong"] + summary["central-ok"]
    return {
        "generatedAt": now_iso(),
        "counties": COUNTY_ORDER,
        "needs": NEEDS,
        "summary": {
            "totalPairs": total_pairs,
            "strongOrCentralOkPairs": strong_pairs,
            "attentionPairs": total_pairs - strong_pairs,
            "statusCounts": dict(summary),
        },
        "rows": rows,
        "gapCandidates": sorted(gap_candidates, key=lambda item: (-item["score"], item["county"], item["needLabel"])),
    }


def build_source_health(records: list[dict], freshness_report: dict) -> dict:
    confidence_counts = Counter(record.get("freshness", {}).get("confidence", "needs-review") for record in records)
    source_level_counts = Counter(source_level(record) for record in records)
    source_type_counts = Counter(record.get("source", {}).get("type", "unknown") for record in records)
    hard_warnings = freshness_report.get("warnings") or []
    transient_warnings = freshness_report.get("transientWarnings") or []
    return {
        "generatedAt": now_iso(),
        "summary": {
            "records": len(records),
            "sourcesChecked": freshness_report.get("summary", {}).get("checked", 0),
            "hardWarnings": len(hard_warnings),
            "transientWarnings": len(transient_warnings),
            "transportWarnings": freshness_report.get("summary", {}).get("transportWarnings", 0),
        },
        "hardWarnings": hard_warnings,
        "transientWarnings": transient_warnings,
        "confidenceCounts": dict(confidence_counts),
        "sourceLevelCounts": dict(source_level_counts),
        "topSourceTypes": source_type_counts.most_common(12),
    }


def build_batch_gate(coverage: dict, source_health: dict) -> dict:
    high_candidates = coverage["gapCandidates"][:30]
    hard_warnings = source_health["summary"]["hardWarnings"]
    attention_pairs = coverage["summary"]["attentionPairs"]
    should_open_broad_batch = False
    if hard_warnings >= 5:
        recommended_mode = "source-hardening"
    elif attention_pairs >= 90:
        recommended_mode = "targeted-coverage"
    else:
        recommended_mode = "maintain-and-target"
    return {
        "generatedAt": now_iso(),
        "decision": {
            "openBroadBatch": should_open_broad_batch,
            "recommendedMode": recommended_mode,
            "nextBatchLabel": "Batch 7 should be targeted only",
            "reason": "Use coverage and source-health signals before adding records by volume.",
        },
        "gates": [
            {
                "id": "hard-warning",
                "label": "來源硬警告",
                "trigger": "hardWarnings > 0",
                "currentValue": hard_warnings,
                "action": "先修壞連結或不可驗證來源，再新增資料。",
            },
            {
                "id": "coverage-gap",
                "label": "覆蓋缺口",
                "trigger": "high-score coverage candidates exist",
                "currentValue": len(high_candidates),
                "action": "只補矩陣列出的高分缺口。",
            },
            {
                "id": "no-result-query",
                "label": "查不到語句",
                "trigger": "validated common user wording returns 0 results",
                "currentValue": 0,
                "action": "先補同義詞或官方 fallback，再決定是否新增資料。",
            },
        ],
        "topCandidates": high_candidates,
    }


def main() -> int:
    root = Path(".")
    resources = read_json(root / "data" / "resources.json").get("records", [])
    freshness_report = read_json(root / "data" / "freshness-report.json")
    coverage = build_coverage(resources)
    source_health = build_source_health(resources, freshness_report)
    batch_gate = build_batch_gate(coverage, source_health)
    write_json(root / "data" / "coverage-matrix.json", coverage)
    write_json(root / "data" / "source-health-summary.json", source_health)
    write_json(root / "data" / "batch-gate.json", batch_gate)
    print(
        "Built operational artifacts: "
        f"{coverage['summary']['totalPairs']} coverage pairs, "
        f"{source_health['summary']['hardWarnings']} hard warnings, "
        f"{len(batch_gate['topCandidates'])} batch-gate candidates."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
