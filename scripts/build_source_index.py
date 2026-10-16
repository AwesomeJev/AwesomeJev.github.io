#!/usr/bin/env python3
"""Build the public browser index from provenance-preserving source ledgers."""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
CHECKED = {"content_screened", "editorial_reviewed", "abstract_checked"}


def canonical(url: str) -> str:
    p = urlsplit(url.strip())
    host = p.netloc.lower().removeprefix("www.")
    path = p.path.rstrip("/")
    if host in {"arxiv.org", "export.arxiv.org"}:
        host = "arxiv.org"
        path = re.sub(r"^/(pdf|html)/", "/abs/", path)
        path = re.sub(r"v\d+(?:\.pdf)?$", "", path).removesuffix(".pdf")
    if host == "huggingface.co" and path.startswith("/papers/"):
        host, path = "arxiv.org", "/abs/" + path.split("/")[-1]
        path = re.sub(r"v\d+$", "", path)
    if host == "github.com":
        path = re.sub(r"/blob/[^/]+/(?:README(?:\.[a-zA-Z-]+)?(?:\.md|\.rst|\.txt)?)$", "", path, flags=re.I)
        path = path.removesuffix(".git")
    # Query parameters can identify a paper (OpenReview id, CiteSeer doi)
    # or a model report. Strip tracking parameters, never resource identity.
    query = urlencode(sorted((key, value) for key, value in parse_qsl(p.query, keep_blank_values=True)
                             if not key.lower().startswith("utm_")
                             and key.lower() not in {"fbclid", "gclid", "msclkid"}))
    return urlunsplit(("https", host, path, query, ""))


def category(row: dict) -> str:
    if row.get("relation") == "background":
        return "Research foundations"
    url = row.get("url", row.get("canonical_url", ""))
    if "arxiv.org" in url or "huggingface.co/papers/" in url:
        return "Papers"
    if "huggingface.co/datasets/" in url:
        return "Datasets"
    if "huggingface.co/" in url and "/spaces/" not in url:
        return "Models"
    if "github.com" in url:
        return "Projects"
    return "Guides and evaluations"


def build() -> dict:
    raw = []
    for name in ("ecosystem-sources.jsonl", "research-sources.jsonl"):
        source = ROOT / "data" / name
        if source.exists():
            for line in source.read_text().splitlines():
                if line.strip():
                    row = json.loads(line)
                    row["ledger"] = name
                    raw.append(row)
    # Preserve the strongest verification record when multiple discovery paths converge.
    rank = {"editorial_reviewed": 0, "content_screened": 1, "abstract_checked": 2, "metadata_only": 3}
    raw.sort(key=lambda r: (rank.get(r.get("verification_level"), 9), r.get("url", r.get("canonical_url", ""))))
    urls, hashes, titles = set(), set(), set()
    rows, duplicates = [], []
    for row in raw:
        url = canonical(row.get("url", row.get("canonical_url", "")))
        if not urlsplit(url).netloc:
            raise ValueError("Missing source URL")
        level = row.get("verification_level", "metadata_only")
        content_hash = row.get("content_sha256", row.get("abstract_sha256", ""))
        title = row.get("title", url)
        if re.match(r"^(?:pip install|git clone|1\.\s*encoder|\{|Start the server)", title, re.I) or re.sub(r"[^a-z]", "", title.casefold()) in {"citation", "acknowledgments", "acknowledgements", "license", "usage", "installation", "readme", "introduction", "modelcard", "datasetcard", "datasplits", "quickstart", "macmlx"}:
            title = urlsplit(url).path.strip("/").removeprefix("datasets/").removeprefix("spaces/") or urlsplit(url).netloc
        title_key = re.sub(r"\W+", "", title.casefold())
        is_paper = row.get("relation") == "background" or "arxiv.org/abs/" in url
        reason = "canonical_url" if url in urls else "content_hash" if content_hash and content_hash in hashes else "paper_title" if is_paper and len(title_key) > 20 and title_key in titles else None
        if reason:
            duplicates.append({"url": url, "reason": reason, "ledger": row["ledger"]})
            continue
        urls.add(url)
        if content_hash:
            hashes.add(content_hash)
        if is_paper:
            titles.add(title_key)
        date = row.get("published_at", "")
        labels = {"editorial_reviewed": "Editorially reviewed", "content_screened": "Content screened", "abstract_checked": "Abstract screened", "metadata_only": "Metadata only"}
        rows.append({
            "id": hashlib.sha256(url.encode()).hexdigest()[:12],
            "title": title,
            "url": url,
            "category": category(row),
            "description": row.get("relevance", row.get("evidence", "")),
            "year": str(date)[:4] if date else "",
            "status": labels.get(level, level),
            "relation": row.get("relation", "adjacent"),
            "verification_level": level,
            "content_sha256": content_hash,
            "retrieved_at": row.get("retrieved_at", ""),
            "ledger": row["ledger"],
        })
    counts = dict(collections.Counter(row["verification_level"] for row in rows))
    counts.update(raw_records=len(raw), unique_records=len(rows), duplicate_records=len(duplicates), checked_sources=sum(row["verification_level"] in CHECKED for row in rows))
    generated = max((r["retrieved_at"] for r in rows), default="")
    rows.sort(key=lambda r: (r["relation"] == "background", r["category"], r["title"].casefold()))
    return {"generated_at": generated, "counts": counts, "sources": rows, "duplicates": duplicates}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Fail if the committed website index is stale")
    args = parser.parse_args()
    payload = build()
    destination = ROOT / "site" / "data" / "source-index.json"
    output = json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n"
    if args.check:
        if not destination.exists() or destination.read_text() != output:
            raise SystemExit("Source index is stale: run python3 scripts/build_source_index.py")
    else:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(output)
        (ROOT / "data" / "source-counts.json").write_text(json.dumps({"generated_at": payload["generated_at"], "counts": payload["counts"]}, indent=2) + "\n")
        badge = {"schemaVersion": 1, "label": "content screened", "message": f"{payload['counts']['checked_sources']:,} sources", "color": "087E8B", "labelColor": "0B3954"}
        (destination.parent / "source-badge.json").write_text(json.dumps(badge) + "\n")
    print(json.dumps(payload["counts"], indent=2))


if __name__ == "__main__":
    main()
