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

USER_AGENT = "taiwan-welfare-resource-hub/0.1 (+https://github.com/Kevin-Yeh-egroup/taiwan-welfare-resource-hub)"


def now_date() -> str:
    return dt.date.today().isoformat()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def load_optional_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return load_json(path)


def merge_record(base: dict, override: dict | None) -> dict:
    if not override:
        return base
    merged = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = merge_record(merged[key], value)
        else:
            merged[key] = value
    return merged


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


def request_json(
    url: str,
    *,
    method: str = "GET",
    payload: dict | None = None,
    headers: dict | None = None,
    allow_insecure_fallback: bool = False,
    timeout: int = 45,
):
    body = None
    request_headers = {"User-Agent": USER_AGENT, **(headers or {})}
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        request_headers.setdefault("Content-Type", "application/json")
    request = urllib.request.Request(url, data=body, headers=request_headers, method=method)
    with open_url(request, timeout=timeout, allow_insecure_fallback=allow_insecure_fallback) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return json.loads(response.read().decode(charset, errors="replace"))


def parse_date(value) -> str | None:
    text = clean(value)
    if not text:
        return None
    match = re.match(r"(\d{4})[-/](\d{1,2})[-/](\d{1,2})", text)
    if not match:
        return None
    year, month, day = match.groups()
    return f"{int(year):04d}-{int(month):02d}-{int(day):02d}"


def normalize_url(value: str | None) -> str | None:
    text = clean(value)
    if not text:
        return None
    if text.startswith("www."):
        text = f"https://{text}"
    parsed = urllib.parse.urlparse(text)
    if parsed.scheme in {"http", "https"} and parsed.netloc:
        return text
    return None


def slug(value: str) -> str:
    text = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return text or "row"


def append_unique(values: list[str], item: str | None) -> None:
    item = clean(item)
    if item and item not in values:
        values.append(item)


def code_values(primary, secondary, code_map: dict[str, str]) -> list[str]:
    values: list[str] = []
    raw_items = []
    if primary:
        raw_items.append(primary)
    if isinstance(secondary, list):
        raw_items.extend(secondary)
    elif secondary:
        raw_items.extend(str(secondary).split(","))

    for raw in raw_items:
        key = clean(raw)
        append_unique(values, code_map.get(key, key) if key else None)
    return values


def code_map_from_payload(payload) -> dict[str, str]:
    rows = payload.get("resultList", []) if isinstance(payload, dict) else []
    return {clean(row.get("no")): clean(row.get("value1")) for row in rows if clean(row.get("no")) and clean(row.get("value1"))}


def format_address(item: dict, city_map: dict[str, str], district_map: dict[str, str]) -> str | None:
    city = city_map.get(clean(item.get("city")) or "", "")
    district = district_map.get(clean(item.get("district")) or "", "")
    address = clean(item.get("address")) or ""
    full = f"{city}{district}{address}".strip()
    return full or None


FOUNDATION_AUDIENCE_KEYWORDS = [
    ("盲", "身心障礙者"),
    ("障礙", "身心障礙者"),
    ("老人", "老人"),
    ("長照", "老人"),
    ("兒童", "兒童及青少年"),
    ("少年", "兒童及青少年"),
    ("青少年", "兒童及青少年"),
    ("婦女", "婦女"),
    ("家庭", "家庭"),
    ("清寒", "經濟弱勢"),
    ("急難", "經濟弱勢"),
    ("醫療", "傷病者"),
]

FOUNDATION_CATEGORY_KEYWORDS = [
    ("獎學", "清寒獎學金"),
    ("清寒", "經濟扶助"),
    ("急難", "急難救助"),
    ("醫療", "醫療照護"),
    ("長照", "長期照顧服務"),
    ("老人", "老人福利"),
    ("兒童", "兒童及青少年福利"),
    ("少年", "兒童及青少年福利"),
    ("障礙", "身心障礙福利"),
]


def infer_foundation_values(name: str, pairs: list[tuple[str, str]]) -> list[str]:
    values: list[str] = []
    for keyword, label in pairs:
        if keyword in name:
            append_unique(values, label)
    return values


def foundation_status_text(status: str | None) -> str:
    return {"A": "運作中"}.get(clean(status) or "", clean(status) or "未標示")


def build_sfaa_headers(source: dict) -> dict:
    return {
        "Origin": "https://swft.sfaa.gov.tw",
        "Referer": source.get("url", "https://swft.sfaa.gov.tw/fund/fh0300#"),
    }


def import_sfaa_foundations(source: dict, limit: int | None = None) -> list[dict]:
    api_base = source.get("apiBase", "https://swft.sfaa.gov.tw/api").rstrip("/")
    headers = build_sfaa_headers(source)
    allow_insecure = source.get("allowInsecureSslFallback", False)
    page_size = int(source.get("pageSize", 500))
    search_url = source.get("apiUrl") or f"{api_base}/main/foundBasic/found/searchFront"
    detail_sleep = float(source.get("detailSleepSeconds", 0.04))

    code_maps = {}
    for code in ["CITY", "DISTRICT", "SRVOBJECT", "SRVTYPE"]:
        payload = request_json(
            f"{api_base}/system/codeType/getOneWithCode/{code}",
            headers=headers,
            allow_insecure_fallback=allow_insecure,
        )
        code_maps[code] = code_map_from_payload(payload)

    rows: list[dict] = []
    page = 1
    while True:
        payload = {
            "serviceObject": [""],
            "serviceType": [""],
            "cities": [""],
            "name": "",
            "page": page,
            "pageSize": page_size,
        }
        response = request_json(
            search_url,
            method="POST",
            payload=payload,
            headers=headers,
            allow_insecure_fallback=allow_insecure,
            timeout=70,
        )
        batch = response.get("resultList", [])
        rows.extend(batch)
        total = int(response.get("pagination", {}).get("total") or len(rows))
        if limit and len(rows) >= limit:
            rows = rows[:limit]
            break
        if len(rows) >= total or not batch:
            break
        page += 1

    records = []
    for index, row in enumerate(rows, start=1):
        foundation_uuid = clean(row.get("uuid"))
        detail = {}
        if foundation_uuid:
            try:
                detail_payload = request_json(
                    f"{api_base}/main/foundBasic/found/findEntityConvertVo/{foundation_uuid}",
                    headers=headers,
                    allow_insecure_fallback=allow_insecure,
                    timeout=50,
                )
                detail = detail_payload.get("result", {}) if isinstance(detail_payload, dict) else {}
            except Exception:
                detail = {}
            time.sleep(detail_sleep)

        item = {**row, **detail}
        name = clean(item.get("name")) or f"全國性社會福利財團法人 {index}"
        county = code_maps["CITY"].get(clean(item.get("city")) or "", "全國")
        district = code_maps["DISTRICT"].get(clean(item.get("district")) or "", "")
        audiences = code_values(item.get("mserviceObject"), item.get("sserviceObject"), code_maps["SRVOBJECT"])
        service_categories = code_values(item.get("mserviceType"), item.get("sserviceType"), code_maps["SRVTYPE"])

        if not audiences:
            audiences = infer_foundation_values(name, FOUNDATION_AUDIENCE_KEYWORDS)
        if not service_categories:
            service_categories = infer_foundation_values(name, FOUNDATION_CATEGORY_KEYWORDS)
        append_unique(audiences, "一般民眾")
        append_unique(service_categories, "民間社福資源")
        append_unique(service_categories, "社福基金會")

        modified = parse_date(row.get("modifyDate") or item.get("modifyDate"))
        licensed = parse_date(item.get("licenseDate") or row.get("licenseDate"))
        status = foundation_status_text(item.get("status") or row.get("status"))
        confidence = "source-dated" if modified and modified.startswith(str(dt.date.today().year)) else "checked"
        address = format_address(item, code_maps["CITY"], code_maps["DISTRICT"])
        website = normalize_url(item.get("url")) or source["url"]
        phone = clean(item.get("phone")) or clean(item.get("contactPhone"))
        email = clean(item.get("contactEmail"))
        main_categories = "、".join(service_categories[:3])
        main_audiences = "、".join(audiences[:3])

        need_tags = []
        for value in [
            name,
            clean(item.get("no")),
            county,
            district,
            "財團法人",
            "基金會",
            "民間基金會",
            "社會福利基金會",
            "民間資源",
            "全國性",
            "今年度仍在運作",
            "2026",
            *audiences,
            *service_categories,
        ]:
            append_unique(need_tags, value)

        records.append({
            "id": f"sfaa-foundation-{slug(clean(item.get('no')) or foundation_uuid or str(index))}",
            "name": name,
            "summary": f"{name}為衛福部社家署全國性社會福利財團法人名錄所列機構，登記地在{county}{district}。主要服務：{main_categories}；主要對象：{main_audiences}。",
            "provider": name,
            "jurisdiction": "全國",
            "county": county,
            "districts": [district] if district else [],
            "audiences": audiences,
            "serviceCategories": service_categories,
            "needTags": need_tags,
            "eligibility": f"官方名錄狀態為「{status}」。實際補助、收案條件、服務地區與今年度方案，仍需以基金會網站或電話確認。",
            "howToApply": [
                "先開啟基金會網站或官方名錄頁，確認是否有今年度服務、補助或活動公告。",
                "以電話或 Email 詢問服務地區、資格、名額、收案時間與文件。",
                "若是急難或經濟弱勢需求，先說明戶籍/居住地、家庭狀況、目前困難與是否已有低收/中低收入戶資格。",
            ],
            "documents": [
                "身分證明文件",
                "戶籍或居住地資料",
                "低收入戶、中低收入戶、身障或其他弱勢證明（如有）",
                "收入、醫療、急難事實或其他方案指定文件",
            ],
            "contact": {
                "phone": phone,
                "email": email,
                "address": address,
                "website": website,
            },
            "source": {"id": source["id"], "url": source["url"], "type": source.get("sourceType")},
            "freshness": {
                "lastChecked": now_date(),
                "sourceUpdatedAt": modified,
                "confidence": confidence,
                "notes": f"{now_date()} 自官方名錄查得狀態為「{status}」；最近資料更新：{modified or '未標示'}；設立日期：{licensed or '未標示'}。",
            },
        })
    return records


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
    parser.add_argument("--overrides", default="data/resource-detail-overrides.json")
    parser.add_argument("--limit", type=int, default=None, help="Optional per-source import limit for testing.")
    parser.add_argument("--sleep", type=float, default=0.7)
    args = parser.parse_args()

    sources_data = load_json(Path(args.sources))
    detail_overrides = load_optional_json(Path(args.overrides)).get("records", {})
    records = []
    errors = []

    for source in sources_data.get("sources", []):
        try:
            if source.get("format") == "tainan-welfare-json":
                records.extend(import_tainan(source, limit=args.limit))
            elif source.get("format") == "sfaa-foundation-json":
                records.extend(import_sfaa_foundations(source, limit=args.limit))
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

    records = [merge_record(record, detail_overrides.get(record.get("id"))) for record in records]

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
