#!/usr/bin/env python
"""Build citizen-facing resource records from allowlisted source URLs."""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import ssl
import time
import urllib.parse
import urllib.error
import urllib.request
import urllib.robotparser
from html.parser import HTMLParser
from pathlib import Path

USER_AGENT = "taiwan-welfare-resource-hub/0.1 (+https://example.invalid; contact: Kevin)"


def now_date() -> str:
    return dt.date.today().isoformat()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def clean(value):
    if value is None:
        return None
    text = str(value).strip()
    return None if text in {"", "null", "None"} else text


class PageSummaryParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.title = ""
        self.meta_description = ""
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag.lower() == "title":
            self.in_title = True
        if tag.lower() == "meta" and attrs_dict.get("name", "").lower() == "description":
            self.meta_description = attrs_dict.get("content", "")
        if tag.lower() == "a" and attrs_dict.get("href"):
            self.links.append(attrs_dict["href"])

    def handle_endtag(self, tag):
        if tag.lower() == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data


def can_fetch(url: str) -> bool:
    parsed = urllib.parse.urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    parser = urllib.robotparser.RobotFileParser()
    parser.set_url(robots_url)
    try:
        parser.read()
        return parser.can_fetch(USER_AGENT, url)
    except Exception:
        return True


def is_ssl_certificate_error(exc: Exception) -> bool:
    return "CERTIFICATE_VERIFY_FAILED" in str(exc)


def open_url(request: urllib.request.Request, *, timeout: int, allow_insecure_fallback: bool = False):
    try:
        return urllib.request.urlopen(request, timeout=timeout)
    except urllib.error.URLError as exc:
        if allow_insecure_fallback and is_ssl_certificate_error(exc):
            context = ssl._create_unverified_context()
            return urllib.request.urlopen(request, timeout=timeout, context=context)
        raise


def fetch_text(url: str, *, allow_insecure_fallback: bool = False) -> str:
    if not can_fetch(url):
        raise RuntimeError(f"robots.txt disallows fetch: {url}")
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with open_url(request, timeout=30, allow_insecure_fallback=allow_insecure_fallback) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


def summarize_page(source: dict) -> dict:
    if source.get("format") == "static-record":
        return static_record(source)

    try:
        body = fetch_text(source["url"], allow_insecure_fallback=source.get("allowInsecureSslFallback", False))
        parser = PageSummaryParser()
        parser.feed(body)
        title = re.sub(r"\s+", " ", html.unescape(parser.title)).strip() or source["name"]
        description = re.sub(r"\s+", " ", html.unescape(parser.meta_description)).strip()
        status = "checked"
    except Exception as exc:
        title = source["name"]
        description = f"來源頁面需人工確認：{exc}"
        status = "needs-review"

    return {
        "id": source["id"],
        "name": source["name"],
        "summary": description or f"{source.get('jurisdiction', '')}社會福利資源入口。",
        "provider": source.get("organization"),
        "jurisdiction": source.get("jurisdiction"),
        "county": source.get("jurisdiction") if source.get("jurisdiction") != "全國" else "全國",
        "districts": ["全市"] if source.get("jurisdiction", "").endswith("市") else [],
        "audiences": infer_audiences(source),
        "serviceCategories": infer_categories(source),
        "needTags": source.get("tags", []),
        "eligibility": "依各服務項目規定。",
        "howToApply": ["開啟來源網站", "依地區、身分或服務類型查詢", "電話確認今年度資格、名額與文件"],
        "documents": ["依各服務項目規定"],
        "contact": {"phone": None, "address": None, "website": source["url"]},
        "source": {"id": source["id"], "url": source["url"], "type": source.get("sourceType")},
        "freshness": {"lastChecked": now_date(), "sourceUpdatedAt": None, "confidence": status, "notes": title},
    }


def static_record(source: dict) -> dict:
    record = dict(source.get("record", {}))
    record.setdefault("id", source["id"])
    record.setdefault("name", source.get("name"))
    record.setdefault("summary", f"{source.get('jurisdiction', '全國')}社會福利官方入口。")
    record.setdefault("provider", source.get("organization"))
    record.setdefault("jurisdiction", source.get("jurisdiction", "全國"))
    record.setdefault("county", source.get("jurisdiction", "全國"))
    record.setdefault("districts", [])
    record.setdefault("audiences", infer_audiences(source))
    record.setdefault("serviceCategories", infer_categories(source))
    record.setdefault("needTags", source.get("tags", []))
    record.setdefault("eligibility", "依各服務項目規定。")
    record.setdefault("howToApply", ["開啟官方來源網站", "依身分、地區或需求查詢", "電話確認最新資格、名額與文件"])
    record.setdefault("documents", ["依各服務項目規定"])
    record.setdefault("contact", {})
    record["contact"].setdefault("website", source.get("url"))
    record.setdefault("source", {"id": source["id"], "url": source.get("url"), "type": source.get("sourceType")})
    record.setdefault(
        "freshness",
        {
            "lastChecked": now_date(),
            "sourceUpdatedAt": None,
            "confidence": "official-entry",
            "notes": "Official source entry; specific programs should be checked from the linked source.",
        },
    )
    return record


def infer_audiences(source: dict) -> list[str]:
    text = " ".join([source.get("name", ""), " ".join(source.get("tags", []))])
    pairs = [
        ("老人", "老人"),
        ("兒少", "兒少"),
        ("兒童", "兒童少年"),
        ("婦女", "婦女"),
        ("身障", "身心障礙者"),
        ("身心障礙", "身心障礙者"),
        ("家庭", "家庭"),
    ]
    values = [label for key, label in pairs if key in text]
    return values or ["一般民眾"]


def infer_categories(source: dict) -> list[str]:
    tags = source.get("tags", [])
    values = []
    if "地圖" in tags:
        values.append("地圖查詢")
    if "開放資料" in tags:
        values.append("地圖資料")
    if "社會福利" in tags or "資源網" in tags:
        values.append("入口平台")
    if "縣市政府" in tags or "社會局處" in tags:
        values.append("地方社福窗口")
    if "就業" in tags or "職訓" in tags:
        values.append("就業與職訓")
    if "健保" in tags:
        values.append("醫療與健保")
    if "長照" in tags:
        values.append("長照")
    return values or ["社福資源"]


def extract_json_array(text: str):
    text = html.unescape(text)
    pre_candidates = re.findall(r"<pre[^>]*>\s*(\[\s*\{.*?\}\s*\])\s*</pre>", text, flags=re.S | re.I)
    candidates = pre_candidates or re.findall(r"\[\s*\{.*?\}\s*\]", text, flags=re.S)
    if not candidates:
        return None
    candidates.sort(key=len, reverse=True)
    for candidate in candidates:
        try:
            return json.loads(html.unescape(candidate))
        except json.JSONDecodeError:
            continue
    return None


def import_tainan(source: dict, limit: int | None = None) -> list[dict]:
    url = source.get("resourceUrl") or source["url"]
    text = fetch_text(url, allow_insecure_fallback=source.get("allowInsecureSslFallback", False))
    rows = extract_json_array(text)
    if not rows:
        raise RuntimeError("Could not find JSON array in Tainan resource page.")
    records = []
    for index, row in enumerate(rows[:limit] if limit else rows):
        district = clean(row.get("d"))
        audience = clean(row.get("o"))
        category = clean(row.get("u")) or clean(row.get("k")) or "社福資源"
        service_item = clean(row.get("k"))
        name = clean(row.get("name")) or f"臺南福利資源 {index + 1}"
        source_row_id = clean(row.get("id")) or "row"
        records.append({
            "id": f"tainan-{source_row_id}-{index + 1}",
            "name": name,
            "summary": clean(row.get("content")) or "臺南市福利地圖資源點。",
            "provider": name,
            "jurisdiction": "臺南市",
            "county": "臺南市",
            "districts": [district] if district else [],
            "audiences": [audience] if audience else ["一般民眾"],
            "serviceCategories": [item for item in [category, service_item] if item],
            "needTags": [item for item in [audience, category, service_item, district, "臺南", "福利地圖"] if item],
            "eligibility": clean(row.get("content")) or "依資源點規定。",
            "howToApply": ["先電話確認服務時間與名額", "確認服務對象與需要文件", "依資源點指示申請或前往"],
            "documents": ["依資源點規定"],
            "contact": {
                "phone": clean(row.get("phone")),
                "address": clean(row.get("addr")),
                "website": clean(row.get("url")) or source["url"],
                "latitude": clean(row.get("Latitude")),
                "longitude": clean(row.get("Longitude")),
            },
            "source": {"id": source["id"], "url": source["url"], "type": source.get("sourceType")},
            "freshness": {"lastChecked": now_date(), "sourceUpdatedAt": None, "confidence": "checked", "notes": "Imported from Tainan welfare map open-data resource."},
        })
    return records


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sources", default="data/sources.json")
    parser.add_argument("--out", default="data/resources.json")
    parser.add_argument("--limit", type=int, default=None, help="Optional per-source import limit for testing.")
    parser.add_argument("--sleep", type=float, default=0.7)
    args = parser.parse_args()

    sources_data = load_json(Path(args.sources))
    records = []
    errors = []

    for source in sources_data.get("sources", []):
        try:
            if source.get("format") == "tainan-welfare-json":
                records.extend(import_tainan(source, limit=args.limit))
            else:
                records.append(summarize_page(source))
        except Exception as exc:
            errors.append({
                "sourceId": source.get("id"),
                "url": source.get("resourceUrl") or source.get("url"),
                "error": str(exc),
            })
            records.append(summarize_page(source))
        time.sleep(args.sleep)

    output = {
        "generatedAt": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "status": "generated",
        "notice": "Generated from allowlisted sources. Review before public publication.",
        "errors": errors,
        "records": records,
    }
    Path(args.out).write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(records)} records to {args.out}; errors={len(errors)}")
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
