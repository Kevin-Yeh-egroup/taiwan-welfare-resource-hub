#!/usr/bin/env python
"""Crawl foundation websites and produce review-only candidate welfare pages."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html
import json
import re
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
from html.parser import HTMLParser
from pathlib import Path

USER_AGENT = "taiwan-welfare-resource-hub/0.1 (+https://github.com/Kevin-Yeh-egroup/taiwan-welfare-resource-hub)"

SERVICE_KEYWORDS = [
    "服務",
    "服務項目",
    "服務內容",
    "服務方案",
    "方案",
    "專案",
    "計畫",
    "補助",
    "扶助",
    "救助",
    "急難",
    "清寒",
    "獎學",
    "獎助",
    "醫療",
    "照護",
    "照顧",
    "長照",
    "身障",
    "身心障礙",
    "老人",
    "兒少",
    "兒童",
    "少年",
    "青少年",
    "家庭",
    "婦女",
    "弱勢",
    "低收入",
    "中低收入",
    "社福",
    "福利",
]

APPLICATION_KEYWORDS = [
    "申請",
    "資格",
    "條件",
    "文件",
    "表單",
    "辦法",
    "名額",
    "受理",
    "報名",
    "洽詢",
    "聯絡",
    "電話",
]

CURRENT_YEAR_KEYWORDS = [
    "2026",
    "115年",
    "115年度",
    "2025",
    "114年",
    "114年度",
    "最新消息",
    "公告",
]

NEGATIVE_KEYWORDS = [
    "捐款",
    "捐助",
    "徵信",
    "財報",
    "章程",
    "董事",
    "隱私",
    "人才招募",
    "招聘",
    "志工招募",
    "購物",
]

PRIORITY_CATEGORY_KEYWORDS = [
    "急難",
    "清寒",
    "醫療",
    "低收入",
    "中低收入",
    "身心障礙",
    "老人",
    "兒童",
    "青少年",
    "長期照顧",
    "家庭",
]

PRIORITY_NAME_KEYWORDS = [
    "芥菜種",
    "國泰",
    "富邦",
    "陽光",
    "和泰",
    "新光",
    "惠眾",
    "惠明",
    "為恭",
    "天主教",
    "介惠",
    "弘化",
    "曹仲植",
]


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def now_date() -> str:
    return dt.date.today().isoformat()


def clean(value) -> str | None:
    if value is None:
        return None
    text = re.sub(r"\s+", " ", str(value)).strip()
    return None if text in {"", "null", "None"} else text


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def is_ssl_certificate_error(exc: Exception) -> bool:
    return "CERTIFICATE_VERIFY_FAILED" in str(exc)


def open_url(request: urllib.request.Request, *, timeout: int, allow_insecure_fallback: bool = True):
    try:
        return urllib.request.urlopen(request, timeout=timeout)
    except urllib.error.URLError as exc:
        if allow_insecure_fallback and is_ssl_certificate_error(exc):
            context = ssl._create_unverified_context()
            response = urllib.request.urlopen(request, timeout=timeout, context=context)
            response.ssl_warning = str(exc)
            return response
        raise


def decode_body(body: bytes, charset: str | None) -> str:
    charsets = [charset, "utf-8", "big5", "cp950"]
    for item in [value for value in charsets if value]:
        try:
            return body.decode(item, errors="replace")
        except LookupError:
            continue
    return body.decode("utf-8", errors="replace")


def normalize_url(value: str | None, base: str | None = None) -> str | None:
    text = clean(value)
    if not text:
        return None
    text = html.unescape(text)
    if base:
        text = urllib.parse.urljoin(base, text)
    if text.startswith("www."):
        text = f"https://{text}"
    parsed = urllib.parse.urlparse(text)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return None
    path = urllib.parse.quote(urllib.parse.unquote(parsed.path), safe="/%:@")
    query = urllib.parse.quote(urllib.parse.unquote(parsed.query), safe="=&%:@")
    parsed = parsed._replace(path=path, query=query, fragment="")
    return urllib.parse.urlunparse(parsed)


def is_same_site(url: str, root: str) -> bool:
    left = urllib.parse.urlparse(url).netloc.lower().removeprefix("www.")
    right = urllib.parse.urlparse(root).netloc.lower().removeprefix("www.")
    return left == right


def is_probably_document(url: str) -> bool:
    path = urllib.parse.urlparse(url).path.lower()
    return path.endswith((".pdf", ".doc", ".docx", ".odt", ".xls", ".xlsx", ".zip", ".rar", ".jpg", ".jpeg", ".png", ".gif"))


def canonical_url_key(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    path = parsed.path.rstrip("/") or "/"
    parsed = parsed._replace(path=path, query=parsed.query.rstrip("&"), fragment="")
    return urllib.parse.urlunparse(parsed).lower()


def is_fallback_website(url: str | None) -> bool:
    if not url:
        return True
    host = urllib.parse.urlparse(url).netloc.lower()
    return "swft.sfaa.gov.tw" in host


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.skip_depth = 0
        self.title = ""
        self.meta_description = ""
        self.links: list[dict] = []
        self._anchor: dict | None = None
        self.text_parts: list[str] = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        tag = tag.lower()
        if tag in {"script", "style", "noscript", "svg"}:
            self.skip_depth += 1
        if tag == "title":
            self.in_title = True
        if tag == "meta":
            name = attrs_dict.get("name", "").lower()
            prop = attrs_dict.get("property", "").lower()
            if name == "description" or prop == "og:description":
                self.meta_description = attrs_dict.get("content", self.meta_description)
        if tag == "a" and attrs_dict.get("href"):
            self._anchor = {"href": attrs_dict["href"], "text": ""}

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in {"script", "style", "noscript", "svg"} and self.skip_depth:
            self.skip_depth -= 1
        if tag == "title":
            self.in_title = False
        if tag == "a" and self._anchor:
            self.links.append(self._anchor)
            self._anchor = None

    def handle_data(self, data):
        if self.skip_depth:
            return
        if self.in_title:
            self.title += data
        if self._anchor is not None:
            self._anchor["text"] += data
        self.text_parts.append(data)

    @property
    def text(self) -> str:
        return clean(" ".join(self.text_parts)) or ""


class RobotsCache:
    def __init__(self, timeout: int):
        self.timeout = timeout
        self.cache: dict[str, urllib.robotparser.RobotFileParser | None] = {}

    def can_fetch(self, url: str) -> bool:
        parsed = urllib.parse.urlparse(url)
        root = f"{parsed.scheme}://{parsed.netloc}"
        if root not in self.cache:
            parser = urllib.robotparser.RobotFileParser()
            robots_url = f"{root}/robots.txt"
            try:
                request = urllib.request.Request(robots_url, headers={"User-Agent": USER_AGENT})
                with open_url(request, timeout=self.timeout, allow_insecure_fallback=True) as response:
                    lines = decode_body(response.read(200_000), response.headers.get_content_charset()).splitlines()
                parser.parse(lines)
                self.cache[root] = parser
            except Exception:
                self.cache[root] = None
        parser = self.cache[root]
        return True if parser is None else parser.can_fetch(USER_AGENT, url)


def fetch_page(url: str, robots: RobotsCache, timeout: int) -> dict:
    if not robots.can_fetch(url):
        raise RuntimeError("robots.txt disallows fetch")
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    started = time.time()
    with open_url(request, timeout=timeout, allow_insecure_fallback=True) as response:
        body = response.read(1_500_000)
        charset = response.headers.get_content_charset()
        text = decode_body(body, charset)
        return {
            "url": response.geturl(),
            "status": response.status,
            "elapsedSeconds": round(time.time() - started, 3),
            "contentType": response.headers.get("content-type"),
            "sha256": hashlib.sha256(body).hexdigest(),
            "sslWarning": getattr(response, "ssl_warning", None),
            "html": text,
        }


def keyword_hits(text: str, keywords: list[str]) -> list[str]:
    return [keyword for keyword in keywords if keyword.lower() in text.lower()]


def summarize_text(text: str, max_len: int = 180) -> str:
    text = text.replace("\ufeff", "")
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]+", " ", text)
    text = clean(re.sub(r"[ \t\r\n]+", " ", text)) or ""
    if len(text) <= max_len:
        return text
    return f"{text[:max_len].rstrip()}..."


def score_link(link: dict) -> int:
    text = f"{link.get('text', '')} {link.get('href', '')}"
    positive = len(keyword_hits(text, SERVICE_KEYWORDS)) * 3
    application = len(keyword_hits(text, APPLICATION_KEYWORDS))
    current = len(keyword_hits(text, CURRENT_YEAR_KEYWORDS))
    negative = len(keyword_hits(text, NEGATIVE_KEYWORDS)) * 2
    return positive + application + current - negative


def score_page(title: str, text: str, url: str) -> dict:
    combined = f"{title} {url} {text[:6000]}"
    service = keyword_hits(combined, SERVICE_KEYWORDS)
    application = keyword_hits(combined, APPLICATION_KEYWORDS)
    current = keyword_hits(combined, CURRENT_YEAR_KEYWORDS)
    negative = keyword_hits(f"{title} {url}", NEGATIVE_KEYWORDS)
    score = len(service) * 3 + len(application) * 2 + len(current) * 2 - len(negative) * 3
    if any(keyword in title for keyword in ["服務", "補助", "救助", "獎學", "方案", "計畫"]):
        score += 4
    if any(keyword in url.lower() for keyword in ["service", "project", "program", "help", "news", "welfare"]):
        score += 2
    confidence = "low"
    if score >= 22 and application:
        confidence = "high"
    elif score >= 13:
        confidence = "medium"
    candidate_type = "organization-info"
    if application and service:
        candidate_type = "possible-program-page"
    if current and ("最新消息" in current or "公告" in current):
        candidate_type = "news-or-activity"
    if confidence == "high":
        candidate_type = "official-service-page"
    return {
        "score": score,
        "confidence": confidence,
        "candidateType": candidate_type,
        "matchedKeywords": sorted(set(service + application + current), key=lambda item: combined.find(item)),
        "currentYearSignals": current,
        "applicationSignals": application,
        "negativeSignals": negative,
    }


def priority_score(record: dict) -> int:
    website = record.get("contact", {}).get("website")
    if is_fallback_website(website):
        return -1
    text = " ".join([record.get("name", ""), " ".join(record.get("serviceCategories", [])), " ".join(record.get("audiences", []))])
    score = 10
    if (record.get("freshness", {}).get("sourceUpdatedAt") or "").startswith(str(dt.date.today().year)):
        score += 7
    score += sum(2 for keyword in PRIORITY_CATEGORY_KEYWORDS if keyword in text)
    score += sum(4 for keyword in PRIORITY_NAME_KEYWORDS if keyword in text)
    return score


def previous_foundation_ids(paths: list[str] | None) -> set[str]:
    ids = set()
    for path in paths or []:
        candidate_path = Path(path)
        if not candidate_path.exists():
            continue
        data = load_json(candidate_path)
        ids.update(item.get("id") for item in data.get("selectedFoundations", []) if item.get("id"))
        ids.update(item.get("foundationId") for item in data.get("candidates", []) if item.get("foundationId"))
    return ids


def choose_foundations(resources: list[dict], limit: int, *, exclude_ids: set[str] | None = None, only_current_year: bool = False) -> list[dict]:
    current_year = str(dt.date.today().year)
    exclude_ids = exclude_ids or set()
    candidates = []
    for record in resources:
        if not record.get("id", "").startswith("sfaa-foundation-") or priority_score(record) < 0:
            continue
        if record["id"] in exclude_ids:
            continue
        if only_current_year and not (record.get("freshness", {}).get("sourceUpdatedAt") or "").startswith(current_year):
            continue
        candidates.append(record)
    candidates.sort(
        key=lambda record: (
            priority_score(record),
            record.get("freshness", {}).get("sourceUpdatedAt") or "",
            record.get("name", ""),
        ),
        reverse=True,
    )
    return candidates[:limit]


def page_candidate_id(foundation_id: str, url: str) -> str:
    digest = hashlib.sha1(url.encode("utf-8")).hexdigest()[:12]
    return f"{foundation_id}-candidate-{digest}"


def extract_candidate_pages(root_url: str, page_data: dict, max_pages: int) -> list[dict]:
    parser = LinkParser()
    parser.feed(page_data["html"])
    links = []
    seen = {root_url}
    for link in parser.links:
        url = normalize_url(link.get("href"), page_data["url"])
        if not url or url in seen or is_probably_document(url) or not is_same_site(url, root_url):
            continue
        seen.add(url)
        link_item = {"url": url, "text": clean(link.get("text")) or "", "score": score_link(link)}
        if link_item["score"] > 0:
            links.append(link_item)
    links.sort(key=lambda item: item["score"], reverse=True)
    return [{"url": root_url, "text": "首頁", "score": 1}, *links[: max(0, max_pages - 1)]]


def crawl_foundation(record: dict, robots: RobotsCache, args) -> tuple[list[dict], dict | None]:
    website = normalize_url(record.get("contact", {}).get("website"))
    if not website or is_fallback_website(website):
        return [], {"foundationId": record["id"], "foundationName": record["name"], "error": "No crawlable organization website."}
    errors = []
    fetched_pages = []
    candidates = []
    try:
        root = fetch_page(website, robots, args.timeout)
    except Exception as exc:
        return [], {"foundationId": record["id"], "foundationName": record["name"], "website": website, "error": str(exc)}

    pages = extract_candidate_pages(website, root, args.max_pages_per_site)
    for page in pages:
        try:
            page_data = root if page["url"] == website else fetch_page(page["url"], robots, args.timeout)
            parser = LinkParser()
            parser.feed(page_data["html"])
            title = clean(html.unescape(parser.title)) or clean(page.get("text")) or record["name"]
            text = parser.text
            page_score = score_page(title, text, page_data["url"])
            fetched_pages.append(page_data["url"])
            if page_score["score"] >= args.min_score:
                candidates.append({
                    "id": page_candidate_id(record["id"], page_data["url"]),
                    "foundationId": record["id"],
                    "foundationName": record["name"],
                    "county": record.get("county"),
                    "audiences": record.get("audiences", []),
                    "serviceCategories": record.get("serviceCategories", []),
                    "website": website,
                    "pageUrl": page_data["url"],
                    "pageTitle": title,
                    "linkText": page.get("text"),
                    "summary": summarize_text(parser.meta_description or text),
                    "matchedKeywords": page_score["matchedKeywords"],
                    "currentYearSignals": page_score["currentYearSignals"],
                    "applicationSignals": page_score["applicationSignals"],
                    "negativeSignals": page_score["negativeSignals"],
                    "score": page_score["score"],
                    "confidence": page_score["confidence"],
                    "candidateType": page_score["candidateType"],
                    "reviewStatus": "candidate-review-required",
                    "canConvertToResource": False,
                    "reason": "Candidate page only. Confirm current-year eligibility, open intake, documents, and contact before converting into a public resource card.",
                    "lastChecked": now_date(),
                })
            time.sleep(args.sleep)
        except Exception as exc:
            errors.append({"url": page["url"], "error": str(exc)})
            time.sleep(args.sleep)

    deduped_candidates = {}
    for candidate in candidates:
        key = canonical_url_key(candidate["pageUrl"])
        if key not in deduped_candidates or candidate["score"] > deduped_candidates[key]["score"]:
            deduped_candidates[key] = candidate

    candidates = sorted(deduped_candidates.values(), key=lambda item: item["score"], reverse=True)
    return candidates[: args.max_candidates_per_site], {
        "foundationId": record["id"],
        "foundationName": record["name"],
        "website": website,
        "fetchedPages": fetched_pages,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--resources", default="data/resources.json")
    parser.add_argument("--out", default="data/foundation-program-candidates.json")
    parser.add_argument("--batch", default="A")
    parser.add_argument("--previous", action="append", default=[], help="Candidate JSON to exclude from this batch. Can be passed multiple times.")
    parser.add_argument("--only-current-year", action="store_true", help="Only select SFAA foundations with sourceUpdatedAt in the current year.")
    parser.add_argument("--limit", type=int, default=30)
    parser.add_argument("--max-pages-per-site", type=int, default=6)
    parser.add_argument("--max-candidates-per-site", type=int, default=3)
    parser.add_argument("--min-score", type=int, default=8)
    parser.add_argument("--timeout", type=int, default=16)
    parser.add_argument("--sleep", type=float, default=0.5)
    args = parser.parse_args()

    resources_data = load_json(Path(args.resources))
    excluded_foundation_ids = previous_foundation_ids(args.previous)
    selected = choose_foundations(
        resources_data.get("records", []),
        args.limit,
        exclude_ids=excluded_foundation_ids,
        only_current_year=args.only_current_year,
    )
    robots = RobotsCache(timeout=min(args.timeout, 10))
    all_candidates = []
    site_reports = []
    errors = []

    for record in selected:
        candidates, report = crawl_foundation(record, robots, args)
        all_candidates.extend(candidates)
        if report:
            site_reports.append(report)
            if report.get("error"):
                errors.append(report)
        print(f"{record['id']} {record['name']}: candidates={len(candidates)}")
        time.sleep(args.sleep)

    output = {
        "generatedAt": now_iso(),
        "batch": args.batch,
        "mode": "candidate-only",
        "notice": "Review-only candidate pages crawled from foundation websites. Do not treat these as public resource records until manually reviewed.",
        "crawlPolicy": {
            "userAgent": USER_AGENT,
            "robotsRespected": True,
            "maxPagesPerSite": args.max_pages_per_site,
            "maxCandidatesPerSite": args.max_candidates_per_site,
            "minScore": args.min_score,
            "sourceDataset": args.resources,
            "previousCandidateFiles": args.previous,
            "excludedFoundations": len(excluded_foundation_ids),
            "onlyCurrentYear": args.only_current_year,
        },
        "summary": {
            "selectedFoundations": len(selected),
            "websitesAttempted": len(selected),
            "websitesWithCandidates": len({item["foundationId"] for item in all_candidates}),
            "pagesFetched": sum(len(item.get("fetchedPages", [])) for item in site_reports),
            "candidates": len(all_candidates),
            "highConfidence": sum(1 for item in all_candidates if item["confidence"] == "high"),
            "mediumConfidence": sum(1 for item in all_candidates if item["confidence"] == "medium"),
            "lowConfidence": sum(1 for item in all_candidates if item["confidence"] == "low"),
            "errors": len(errors) + sum(len(item.get("errors", [])) for item in site_reports),
        },
        "selectedFoundations": [
            {
                "id": record["id"],
                "name": record["name"],
                "county": record.get("county"),
                "website": record.get("contact", {}).get("website"),
                "sourceUpdatedAt": record.get("freshness", {}).get("sourceUpdatedAt"),
                "priorityScore": priority_score(record),
                "priorityReason": "Real website plus current-year update, high-demand service category, or high-recognition foundation name.",
            }
            for record in selected
        ],
        "candidates": all_candidates,
        "siteReports": site_reports,
    }
    Path(args.out).write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(all_candidates)} candidates from {len(selected)} foundations to {args.out}; errors={output['summary']['errors']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
