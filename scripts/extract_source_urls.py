#!/usr/bin/env python
"""Extract URL seeds from DOCX and PDF source documents."""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree

URL_RE = re.compile(r"https?://[^\s<>'\"\\\]\)}\u3000]+", re.IGNORECASE)


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def clean_url(value: str) -> str:
    return value.rstrip(".,;:，。；：）)]}>\"'")


def extract_urls(text: str) -> list[str]:
    return sorted({clean_url(match.group(0)) for match in URL_RE.finditer(text or "")})


def docx_text(path: Path) -> str:
    chunks: list[str] = []
    with zipfile.ZipFile(path) as archive:
      for name in archive.namelist():
          if not name.startswith("word/"):
              continue
          if name.endswith(".xml") or name.endswith(".rels"):
              raw = archive.read(name)
              try:
                  chunks.append(raw.decode("utf-8", errors="ignore"))
              except UnicodeDecodeError:
                  chunks.append(raw.decode("utf-8-sig", errors="ignore"))

    joined = "\n".join(chunks)
    try:
        root = ElementTree.fromstring(f"<root>{joined}</root>")
        text = " ".join(node.text or "" for node in root.iter())
        return html.unescape(joined + "\n" + text)
    except ElementTree.ParseError:
        return html.unescape(joined)


def pdf_text(path: Path) -> tuple[str, list[str]]:
    warnings: list[str] = []
    chunks: list[str] = []
    try:
        from pypdf import PdfReader
    except Exception as exc:  # pragma: no cover - environment dependent
        warnings.append(f"pypdf unavailable: {exc}")
        raw = path.read_bytes()
        return raw.decode("latin-1", errors="ignore"), warnings

    try:
        reader = PdfReader(str(path))
        for page in reader.pages:
            chunks.append(page.extract_text() or "")
    except Exception as exc:
        warnings.append(f"PDF text extraction failed: {exc}")

    try:
        chunks.append(path.read_bytes().decode("latin-1", errors="ignore"))
    except Exception as exc:
        warnings.append(f"PDF raw scan failed: {exc}")

    return "\n".join(chunks), warnings


def find_files(inputs: list[str]) -> list[Path]:
    files: list[Path] = []
    for item in inputs:
        path = Path(item)
        if path.is_dir():
            files.extend(sorted(path.rglob("*.docx")))
            files.extend(sorted(path.rglob("*.pdf")))
        elif path.is_file() and path.suffix.lower() in {".docx", ".pdf"}:
            files.append(path)
    return sorted(set(files))


def process_file(path: Path) -> dict:
    result = {
        "path": str(path),
        "name": path.name,
        "status": "ok",
        "urls": [],
        "warnings": [],
    }
    try:
        if path.suffix.lower() == ".docx":
            text = docx_text(path)
        elif path.suffix.lower() == ".pdf":
            text, warnings = pdf_text(path)
            result["warnings"].extend(warnings)
        else:
            result["status"] = "skipped"
            return result
        result["urls"] = extract_urls(text)
    except Exception as exc:
        result["status"] = "error"
        result["warnings"].append(str(exc))
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", help="Files or directories to scan.")
    parser.add_argument("--out", default="data/extracted-urls.json", help="Output JSON path.")
    args = parser.parse_args()

    files = find_files(args.inputs)
    output = {
        "generatedAt": now_iso(),
        "inputCount": len(args.inputs),
        "fileCount": len(files),
        "files": [process_file(path) for path in files],
    }
    all_urls = sorted({url for item in output["files"] for url in item.get("urls", [])})
    output["urlCount"] = len(all_urls)
    output["urls"] = all_urls

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Scanned {len(files)} files; found {len(all_urls)} unique URLs; wrote {out_path}")
    if not files:
        print("Warning: no DOCX/PDF files found.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
