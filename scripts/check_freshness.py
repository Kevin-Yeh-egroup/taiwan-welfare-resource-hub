#!/usr/bin/env python
"""Check source freshness with HTTP metadata and content fingerprints."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

USER_AGENT = "taiwan-welfare-resource-hub/0.1 (+https://github.com/Kevin-Yeh-egroup/taiwan-welfare-resource-hub)"


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def load_json(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8-sig"))


def is_ssl_certificate_error(exc: Exception) -> bool:
    return "CERTIFICATE_VERIFY_FAILED" in str(exc)


def open_url(request: urllib.request.Request, *, timeout: int, allow_insecure_fallback: bool = False):
    try:
        return urllib.request.urlopen(request, timeout=timeout)
    except urllib.error.URLError as exc:
        if allow_insecure_fallback and is_ssl_certificate_error(exc):
            context = ssl._create_unverified_context()
            response = urllib.request.urlopen(request, timeout=timeout, context=context)
            response.ssl_warning = str(exc)
            return response
        raise


def get_url(url: str, method: str = "HEAD", *, allow_insecure_fallback: bool = False) -> dict:
    request = urllib.request.Request(url, method=method, headers={"User-Agent": USER_AGENT})
    started = time.time()
    with open_url(request, timeout=25, allow_insecure_fallback=allow_insecure_fallback) as response:
        body = b""
        if method == "GET":
            body = response.read(1_000_000)
        elapsed = round(time.time() - started, 3)
        headers = {key.lower(): value for key, value in response.headers.items()}
        return {
            "status": response.status,
            "url": response.geturl(),
            "elapsedSeconds": elapsed,
            "etag": headers.get("etag"),
            "lastModified": headers.get("last-modified"),
            "contentLength": headers.get("content-length"),
            "contentType": headers.get("content-type"),
            "sha256": hashlib.sha256(body).hexdigest() if body else None,
            "sslWarning": getattr(response, "ssl_warning", None),
        }


def check(url: str, *, allow_insecure_fallback: bool = False) -> dict:
    try:
        result = get_url(url, "HEAD", allow_insecure_fallback=allow_insecure_fallback)
        if result["status"] >= 400 or not result.get("etag") and not result.get("lastModified"):
            get_result = get_url(url, "GET", allow_insecure_fallback=allow_insecure_fallback)
            result.update({k: v for k, v in get_result.items() if v is not None})
        return {"ok": True, **result}
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as exc:
        try:
            get_result = get_url(url, "GET", allow_insecure_fallback=allow_insecure_fallback)
            return {"ok": True, **get_result, "headWarning": str(exc)}
        except Exception as get_exc:
            return {"ok": False, "error": str(get_exc), "headError": str(exc)}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


def source_urls(source: dict) -> list[str]:
    urls = [source.get("url")]
    if source.get("resourceUrl"):
        urls.append(source["resourceUrl"])
    return [url for url in urls if url]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sources", default="data/sources.json")
    parser.add_argument("--out", default="data/freshness-report.json")
    parser.add_argument("--snapshots", default="data/source-snapshots.json")
    parser.add_argument("--sleep", type=float, default=0.7)
    args = parser.parse_args()

    sources_path = Path(args.sources)
    sources_data = load_json(sources_path, {})
    previous = load_json(Path(args.snapshots), {})
    previous_sources = previous.get("sources", {})

    report_sources = []
    snapshot_sources = {}
    changed = 0
    transport_warnings = 0
    warnings = []

    for source in sources_data.get("sources", []):
        entries = []
        for url in source_urls(source):
            result = check(url, allow_insecure_fallback=source.get("allowInsecureSslFallback", False))
            fingerprint = {
                "etag": result.get("etag"),
                "lastModified": result.get("lastModified"),
                "contentLength": result.get("contentLength"),
                "sha256": result.get("sha256"),
            }
            key = f"{source['id']}::{url}"
            old = previous_sources.get(key)
            is_changed = bool(old and fingerprint != old.get("fingerprint"))
            if is_changed:
                changed += 1
            entries.append({
                "url": url,
                "ok": result.get("ok", False),
                "status": result.get("status"),
                "finalUrl": result.get("url"),
                "lastModified": result.get("lastModified"),
                "etag": result.get("etag"),
                "contentLength": result.get("contentLength"),
                "contentType": result.get("contentType"),
                "changedSinceLastRun": is_changed,
                "error": result.get("error"),
                "sslWarning": result.get("sslWarning"),
                "checkedAt": now_iso(),
            })
            if result.get("sslWarning"):
                transport_warnings += 1
            snapshot_sources[key] = {
                "sourceId": source["id"],
                "url": url,
                "fingerprint": fingerprint,
                "checkedAt": now_iso(),
            }
            time.sleep(args.sleep)

        if any(not entry["ok"] for entry in entries):
            warnings.append({"level": "warning", "sourceId": source["id"], "message": "One or more URLs failed freshness check."})
        report_sources.append({
            "id": source["id"],
            "name": source.get("name"),
            "jurisdiction": source.get("jurisdiction"),
            "refreshPolicy": source.get("refreshPolicy", {}),
            "entries": entries,
        })

    report = {
        "generatedAt": now_iso(),
        "summary": {
            "checked": sum(len(item["entries"]) for item in report_sources),
            "changed": changed,
            "transportWarnings": transport_warnings,
            "warnings": len(warnings),
        },
        "warnings": warnings,
        "sources": report_sources,
    }

    Path(args.out).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    Path(args.snapshots).write_text(json.dumps({"generatedAt": now_iso(), "sources": snapshot_sources}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Checked {report['summary']['checked']} URLs; changed={changed}; warnings={len(warnings)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
