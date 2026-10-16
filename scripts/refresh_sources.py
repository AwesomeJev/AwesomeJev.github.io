#!/usr/bin/env python3
"""Incrementally refresh public sources without erasing earlier evidence.

Downloaded documents are untrusted data. Only short evidence and hashes enter
the ledgers; response bodies are cached in memory, never in the repository.
No credentials, cookies, proxy settings or downloaded code are used.
"""
from __future__ import annotations

import argparse
from collections import OrderedDict
import concurrent.futures as cf
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import http.client
import ipaddress
import json
import os
from pathlib import Path
import re
import socket
import ssl
import subprocess
import sys
import threading
import time
import urllib.parse

try:
    from . import collect_ecosystem as ecosystem
    from . import collect_research as research
    from . import build_source_index as index
    from .validate import LEAK_PATTERNS
except ImportError:
    import collect_ecosystem as ecosystem
    import collect_research as research
    import build_source_index as index
    from validate import LEAK_PATTERNS

ROOT = Path(__file__).resolve().parents[1]
LEVEL = {"metadata_only": 0, "abstract_checked": 1, "content_screened": 2, "editorial_reviewed": 3}
SECRET_QUERY = re.compile(r"(?:token|api.?key|password|secret|signature|credential|authorization)", re.I)
DIRECT_QUERIES = ["Jev TypeSafe", "typed decision model", "System One model Jev", "RLCD calibrated decisions"]
MAX_BODY = 6_000_000


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class FetchError(Exception):
    """Safe, fixed-message exception: never include response text or secrets."""


def public_url(url: str):
    """Validate syntax before DNS or requests; document identifiers remain intact."""
    if not isinstance(url, str) or len(url) > 4096 or re.search(r"[\x00-\x20\\]", url):
        raise FetchError("unsafe_url_syntax")
    try:
        p = urllib.parse.urlsplit(url)
        host = (p.hostname or "").rstrip(".").lower()
        if p.scheme not in {"http", "https"} or not host or p.username is not None or p.password is not None:
            raise FetchError("unsafe_url_scheme_or_credentials")
        if p.port not in {None, 80 if p.scheme == "http" else 443}:
            raise FetchError("unsupported_port")
        if "." not in host and ":" not in host:
            raise FetchError("non_public_host")
        if host in {"localhost", "localhost.localdomain"} or host.endswith((".localhost", ".local", ".internal", ".home", ".lan")):
            raise FetchError("non_public_host")
        if any(SECRET_QUERY.search(k) for k, _ in urllib.parse.parse_qsl(p.query, keep_blank_values=True)):
            raise FetchError("credential_query_rejected")
        try:
            if not ipaddress.ip_address(host).is_global:
                raise FetchError("non_public_ip")
        except ValueError:
            host.encode("idna")
        return p
    except (ValueError, UnicodeError):
        raise FetchError("unsafe_url_syntax") from None


def public_addresses(host: str, port: int):
    """Resolve once; require every result to be global and pin the connection."""
    try:
        rows = socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)
        addresses = list(dict.fromkeys(row[4][0] for row in rows))
        if not addresses or any(not ipaddress.ip_address(a).is_global for a in addresses):
            raise FetchError("dns_non_public_address")
        return addresses
    except (OSError, ValueError):
        raise FetchError("dns_resolution_failed") from None


class PublicFetcher:
    """Bounded GETs with checked redirects, DNS pinning and no ambient auth."""
    def __init__(self, retries=2, timeout=18, pause=0.0, cache_bytes=32 * 1024 * 1024):
        self.retries, self.timeout, self.pause = retries, timeout, pause
        self.cache = OrderedDict()
        self.cache_bytes = cache_bytes
        self.cached_bytes = 0
        self.lock = threading.Lock()
        self.requests = 0

    def _request(self, url):
        p = public_url(url)
        host = p.hostname.encode("idna").decode("ascii")
        port = p.port or (443 if p.scheme == "https" else 80)
        addresses = public_addresses(host, port)
        connection_type = http.client.HTTPSConnection if p.scheme == "https" else http.client.HTTPConnection
        kwargs = {"timeout": self.timeout}
        if p.scheme == "https":
            kwargs["context"] = ssl.create_default_context()
        conn = connection_type(host, port, **kwargs)
        # HTTPSConnection still verifies the original hostname/SNI; only TCP is
        # pinned, preventing a second DNS resolution from reaching a private IP.
        conn._create_connection = lambda _address, timeout, source_address=None: socket.create_connection((addresses[0], port), timeout, source_address)
        try:
            target = urllib.parse.urlunsplit(("", "", p.path or "/", p.query, ""))
            conn.request("GET", target, headers={"User-Agent": "AwesomeJev-Public-Refresh/1.0", "Accept": "application/json,text/plain,text/html", "Accept-Encoding": "identity"})
            with self.lock:
                self.requests += 1
            response = conn.getresponse()
            headers = {k.lower(): v for k, v in response.getheaders()}
            body = response.read(MAX_BODY + 1) if response.status == 200 else b""
            if len(body) > MAX_BODY:
                raise FetchError("response_size_limit")
            return response.status, headers, body
        finally:
            conn.close()

    def fetch(self, url):
        public_url(url)
        with self.lock:
            cached = self.cache.get(url)
            if cached:
                self.cache.move_to_end(url)
        if cached:
            return cached
        current = url
        for hop in range(6):
            public_url(current)
            for attempt in range(self.retries + 1):
                try:
                    status, headers, raw = self._request(current)
                except FetchError as e:
                    if str(e) == "dns_resolution_failed" and attempt < self.retries:
                        time.sleep(min(2 ** attempt, 8))
                        continue
                    raise
                except (OSError, http.client.HTTPException):
                    if attempt == self.retries:
                        raise FetchError("network_failure") from None
                    time.sleep(min(2 ** attempt, 8))
                    continue
                if status == 429 or 500 <= status < 600:
                    if attempt == self.retries:
                        raise FetchError("http_" + str(status))
                    retry = headers.get("retry-after", "")
                    delay = min(float(retry), 8) if retry.isdigit() else min(2 ** attempt, 8)
                    time.sleep(delay)
                    continue
                break
            if status in {301, 302, 303, 307, 308}:
                location = headers.get("location", "")
                if not location:
                    raise FetchError("redirect_without_location")
                target = urllib.parse.urljoin(current, location)
                public_url(target)  # Reject before the next network request.
                current = target
                continue
            if status != 200:
                raise FetchError("http_" + str(status))
            ctype = headers.get("content-type", "")
            if raw.startswith(b"%PDF") or ctype.startswith(("image/", "audio/", "video/")):
                raise FetchError("unsupported_binary_document")
            result = raw, current, ctype
            with self.lock:
                if len(raw) <= self.cache_bytes:
                    previous = self.cache.pop(url, None)
                    if previous:
                        self.cached_bytes -= len(previous[0])
                    while self.cache and self.cached_bytes + len(raw) > self.cache_bytes:
                        _, removed = self.cache.popitem(last=False)
                        self.cached_bytes -= len(removed[0])
                    self.cache[url] = result
                    self.cached_bytes += len(raw)
            if self.pause:
                time.sleep(self.pause)
            return result
        raise FetchError("redirect_limit")


def canonical_source(url):
    public_url(url)
    p = urllib.parse.urlsplit(url)
    if p.hostname in {"github.com", "www.github.com", "raw.githubusercontent.com", "huggingface.co", "hf.co"}:
        result = ecosystem.canonical(url)
    else:
        result = index.canonical(url)
    if not result:
        raise FetchError("excluded_discovery_url")
    public_url(result)
    return result


def identity(row):
    url = row.get("url") or row.get("canonical_url") or ""
    public_url(url)
    key = index.canonical(url)
    if urllib.parse.urlsplit(key).hostname == "github.com":
        key = key.lower()
    # Revisions are provenance, not new logical source documents.
    if key.startswith(ecosystem.SPACE_URL + "/blob/"):
        key = re.sub(r"/blob/[^/]+/", "/blob/main/", key, count=1)
    return key


def content_hash(row):
    return row.get("content_sha256") or row.get("abstract_sha256")


def record_safe(row):
    try:
        identity(row)
        for key in ("retrieved_url", "retrieval_url"):
            if row.get(key):
                public_url(row[key])
        for url in row.get("discovered_from", []):
            public_url(url)
        text = json.dumps(row, ensure_ascii=False)
        return not any(pattern.search(text) for pattern in LEAK_PATTERNS.values())
    except (FetchError, TypeError, ValueError):
        return False


@dataclass
class Ledger:
    rows: list[dict]
    lines: list[str]

    @classmethod
    def read(cls, path):
        if not path.exists():
            return cls([], [])
        lines = path.read_bytes().decode("utf-8").splitlines(keepends=True)
        if any(not line.strip() for line in lines):
            raise ValueError("blank_ledger_record")
        return cls([json.loads(line) for line in lines], lines)


def merge_records(old: Ledger, incoming, max_new=None):
    """Keep old bytes on unchanged hashes/failure; never grant editorial status."""
    rows, lines = list(old.rows), list(old.lines)
    positions = {identity(row): i for i, row in enumerate(rows)}
    hashes = {content_hash(row) for row in rows if content_hash(row)}
    changes = {"added": [], "changed": [], "editorial_review_required": [], "duplicates": 0, "preserved_after_failure": 0, "rejected": 0}
    candidates = {}
    for row in incoming:
        if not record_safe(row):
            changes["rejected"] += 1
            continue
        key = identity(row)
        if key not in candidates or LEVEL.get(row.get("verification_level"), 0) > LEVEL.get(candidates[key].get("verification_level"), 0):
            candidates[key] = row
    for key, candidate in sorted(candidates.items()):
        new = dict(candidate)
        new.pop("_rank", None)
        if new.get("verification_level") == "editorial_reviewed":
            new["verification_level"] = "content_screened"
            new["checked_via"] = "Automated public-source refresh; editorial review not performed."
        if key in positions:
            i = positions[key]
            prior = rows[i]
            if content_hash(new) and content_hash(new) == content_hash(prior):
                continue
            if LEVEL.get(new.get("verification_level"), 0) < LEVEL.get(prior.get("verification_level"), 0) and prior.get("verification_level") != "editorial_reviewed":
                changes["preserved_after_failure"] += 1
                continue
            if new.get("verification_level") == "metadata_only" or new.get("status") in {"unavailable", "audit_error", "insufficient_content"}:
                changes["preserved_after_failure"] += 1
                continue
            if prior.get("verification_level") == "editorial_reviewed":
                changes["editorial_review_required"].append({"url": key, "old_content_sha256": content_hash(prior), "observed_content_sha256": content_hash(new), "observed_verification_level": new["verification_level"], "retrieved_url": new.get("retrieved_url", new.get("retrieval_url")), "note": "Prior reviewed record preserved; changed content requires maintainer review."})
                continue
            # Retain fields the machine collector does not own, including any
            # manually supplied notes; preserve explicit editorial annotations.
            merged = {**prior, **new}
            for field in ("editorial_note", "manual_notes", "reviewed_by", "review_date", "curated"):
                if field in prior:
                    merged[field] = prior[field]
            rows[i] = merged
            lines[i] = json.dumps(merged, ensure_ascii=False, sort_keys=True) + "\n"
            if content_hash(merged):
                hashes.add(content_hash(merged))
            changes["changed"].append(key)
        else:
            if max_new is not None and len(changes["added"]) >= max_new:
                continue
            if content_hash(new) and content_hash(new) in hashes:
                changes["duplicates"] += 1
                continue
            positions[key] = len(rows)
            rows.append(new)
            separator = "\n" if lines and not lines[-1].endswith("\n") else ""
            lines.append(separator + json.dumps(new, ensure_ascii=False, sort_keys=True) + "\n")
            if content_hash(new):
                hashes.add(content_hash(new))
            changes["added"].append(key)
    return Ledger(rows, lines), changes


class Scan:
    def __init__(self, fetcher, workers=8):
        self.fetcher, self.workers = fetcher, workers
        self.errors, self.excluded = [], 0
        self.lock = threading.Lock()
        self.index_revision = None
        self.api_gate = threading.Lock()
        self.next_api_request = 0.0
        self.successful_queries = 0

    def error(self, url, code):
        try:
            public_url(url)
            item = {"url": url, "code": code[:80]}
        except FetchError:
            item = {"url_sha256": hashlib.sha256(str(url).encode()).hexdigest(), "code": "unsafe_discovery_url"}
        with self.lock:
            self.errors.append(item)

    def discover_index(self):
        seeds, records = {}, []
        try:
            info = json.loads(self.fetcher.fetch("https://huggingface.co/api/spaces/" + ecosystem.SPACE)[0])
            revision = info["sha"]
            if not re.fullmatch(r"[a-f0-9]{40}", revision):
                raise ValueError("invalid_revision")
            self.index_revision = revision
        except (FetchError, ValueError, KeyError, TypeError) as e:
            self.error(ecosystem.SPACE_URL, "index_discovery_failed:" + type(e).__name__)
            return records, seeds
        base = ecosystem.SPACE_URL + "/raw/" + revision + "/"
        files = {}
        for name in ("README.md", "news.html", "data/index.json", "data/methodology.json", "data/vision.json", "data/v03.json"):
            try:
                raw, resolved, _ = self.fetcher.fetch(base + name)
                parsed = json.loads(raw) if name.endswith(".json") else None
                if len(raw) < 100 or name.endswith(".json") and not isinstance(parsed, dict):
                    raise ValueError("insufficient_index_content")
                files[name] = parsed if parsed is not None else raw.decode("utf-8", errors="replace")
                records.append({"url": ecosystem.SPACE_URL if name == "README.md" else ecosystem.SPACE_URL + "/blob/main/" + name,
                    "title": "Jev Decision Index — " + name, "topic": "community-evaluation-index", "relation": "direct", "verification_level": "content_screened", "status": "screened", "retrieved_at": now(), "retrieved_url": resolved, "resolved_revision": revision, "content_sha256": hashlib.sha256(raw).hexdigest(), "content_bytes": len(raw), "checked_via": "Automated retrieval and structural inspection of current community index source; not editorial review.", "evidence": "Current public index document parsed for linked artifacts and evaluation provenance.", "relevance": "Community source for independent Jev-inspired implementations and evaluation.", "discovered_from": [ecosystem.SPACE_URL]})
            except (FetchError, ValueError, TypeError) as e:
                self.error(base + name, "index_file_failed:" + type(e).__name__)

        def add(url, topic, relation, origin, why):
            try:
                key = canonical_source(url)
                if key == ecosystem.SPACE_URL:
                    return
                seeds.setdefault(key, {"url": key, "title": key.rsplit("/", 1)[-1], "topic": topic, "relation": relation, "relevance": why, "discovered_from": [origin], "discovery_depth": 0})
            except FetchError:
                self.excluded += 1
        readme = files.get("README.md", "")
        front = readme.split("---")[1] if isinstance(readme, str) and readme.count("---") >= 2 else ""
        for model in re.findall(r"^-\s+([^\s]+/[^\s]+)\s*$", front, re.M):
            add("https://huggingface.co/" + model, "decision-model-card", "direct", base + "README.md", "Model explicitly linked by the current Jev Decision Index.")
        idx = files.get("data/index.json") or {}
        for model in as_list(idx.get("models")) if isinstance(idx, dict) else []:
            if not isinstance(model, dict):
                continue
            meta = model.get("meta") or {}
            for field, topic in (("model_url", "decision-model-card"), ("code_url", "implementation-repository")):
                if isinstance(meta, dict) and meta.get(field):
                    add(meta[field], topic, "direct", base + "data/index.json", "Artifact linked by current evaluated-entrant metadata.")
        for url in ecosystem.links(str(files.get("news.html", ""))):
            add(url, "ecosystem-news-artifact", "direct", base + "news.html", "Artifact linked by the current community news corpus; source claims require separate validation.")
        methodology = files.get("data/methodology.json") or {}
        if isinstance(methodology, dict):
            for bench in as_list(methodology.get("benchmarks")) + as_list(methodology.get("added_benchmarks")):
                for url in ecosystem.links(json.dumps(bench)):
                    add(url, "benchmark-source", "adjacent", base + "data/methodology.json", "Upstream evaluation source cited by the Decision Index methodology.")
            reproduction = methodology.get("reproduce")
            repo = reproduction.get("github") if isinstance(reproduction, dict) else None
            if repo:
                add(repo, "evaluation-harness", "direct", base + "data/methodology.json", "Public reproduction harness linked by the index; private tests may remain unavailable.")
        for url in ecosystem.links(json.dumps(files.get("data/vision.json", {}))):
            add(url, "vision-decision-artifact", "direct", base + "data/vision.json", "Artifact linked by the current vision evaluation metadata.")
        return records, seeds

    def scan_ecosystem(self, old, max_new=None, smoke=False):
        records, seeds = self.discover_index()
        old_keys = {identity(r) for r in old.rows}
        for row in old.rows:
            key = identity(row)
            if key == ecosystem.SPACE_URL or key.startswith(ecosystem.SPACE_URL + "/blob/"):
                continue
            seeds.setdefault(key, {"url": row.get("url", key), "title": row.get("title", key), "topic": row.get("topic", "ecosystem-artifact"), "relation": row.get("relation", "adjacent"), "relevance": row.get("relevance", "Previously recorded public source."), "discovered_from": row.get("discovered_from", []), "discovery_depth": row.get("discovery_depth", 0)})
        visited, new_attempts = set(), 0
        original = ecosystem.fetch
        ecosystem.fetch = self.fetcher.fetch
        try:
            for depth in (0, 1):
                batch = []
                for key, seed in sorted(seeds.items()):
                    if key in visited or seed.get("discovery_depth", 0) > depth:
                        continue
                    if key not in old_keys:
                        if max_new is not None and new_attempts >= max_new:
                            continue
                        new_attempts += 1
                    batch.append(seed)
                    visited.add(key)
                if smoke:
                    batch = batch[:8]
                print(json.dumps({"phase": "ecosystem", "depth": depth, "documents": len(batch)}), flush=True)
                with cf.ThreadPoolExecutor(max_workers=self.workers) as pool:
                    futures = {pool.submit(ecosystem.audit, seed): seed for seed in batch}
                    for i, future in enumerate(cf.as_completed(futures), 1):
                        seed = futures[future]
                        try:
                            row, children = future.result()
                            if row.get("verification_level") == "metadata_only":
                                self.error(seed["url"], row.get("status", "content_unavailable"))
                            if ecosystem.eligible(row):
                                records.append(row)
                            else:
                                self.excluded += 1
                            for child in children:
                                try:
                                    key = canonical_source(child["url"])
                                    child["url"] = key
                                    seeds.setdefault(key, child)
                                except FetchError:
                                    self.excluded += 1
                        except (FetchError, ValueError, TypeError, KeyError) as e:
                            self.error(seed["url"], "document_failed:" + type(e).__name__)
                        if i % 200 == 0:
                            print(json.dumps({"phase": "ecosystem", "completed": i}), flush=True)
        finally:
            ecosystem.fetch = original
        return records

    def query(self, topic, query, provider):
        if provider == "openalex_api":
            url = research.OPENALEX_API + "?" + urllib.parse.urlencode({"filter": "title.search:" + query, "per-page": 200, "select": "id,doi,title,authorships,publication_year,abstract_inverted_index,primary_location,locations"})
        else:
            url = research.API + "?" + urllib.parse.urlencode({"q": query, "limit": 120})
        with self.api_gate:
            delay = max(0, self.next_api_request - time.monotonic())
            if delay:
                time.sleep(delay)
            self.next_api_request = time.monotonic() + .4
        try:
            raw, final, _ = self.fetcher.fetch(url)
            data = json.loads(raw)
            if provider == "openalex_api":
                data = research.convert_openalex(data.get("results", []))
            if not isinstance(data, list):
                raise ValueError("invalid_paper_response")
            clean = []
            for item in data:
                if not isinstance(item, dict):
                    continue
                paper = item.get("paper", item)
                if not isinstance(paper, dict):
                    continue
                paper = dict(paper)
                for key in ("title", "summary"):
                    paper[key] = paper.get(key) if isinstance(paper.get(key), str) else ""
                paper["authors"] = [{"name": a["name"]} for a in as_list(paper.get("authors")) if isinstance(a, dict) and isinstance(a.get("name"), str)]
                clean.append({"paper": paper})
            with self.lock:
                self.successful_queries += 1
            return topic, query, {"data": clean, "provider": provider, "retrieval_url": final, "retrieved_at": now(), "http_status": 200}
        except (FetchError, ValueError, TypeError, KeyError, AttributeError) as e:
            self.error(url, "paper_query_failed:" + type(e).__name__)
            return topic, query, {"data": []}

    def scan_research(self, smoke=False):
        jobs = [("direct", q, research.PROVIDER) for q in DIRECT_QUERIES]
        background = [(t, q, research.PROVIDER) for t, queries in research.QUERIES.items() for q in queries]
        background += [(t, q, "openalex_api") for t, queries in research.OPENALEX_QUERIES.items() for q in queries]
        jobs += background[:2] if smoke else background
        with cf.ThreadPoolExecutor(max_workers=min(self.workers, 3)) as pool:
            results = list(pool.map(lambda args: self.query(*args), jobs))
        records, _ = research.build_records(results)
        for row in records:
            row.pop("_rank", None)
        direct = []
        for _, query, wrapper in results:
            for item in wrapper.get("data", []):
                paper = item.get("paper", item)
                pid = re.sub(r"v\d+$", "", str(paper.get("id", "")))
                title = " ".join(str(paper.get("title", "")).split())
                abstract = " ".join(str(paper.get("summary", "")).split())
                text = title + " " + abstract
                if not direct_paper(title, abstract) or len(abstract.split()) < 30 or not re.fullmatch(r"\d{4}\.\d{4,5}", pid):
                    continue
                direct.append({"url": "https://arxiv.org/abs/" + pid, "title": title, "authors": [a.get("name", "") for a in paper.get("authors", []) if a.get("name")], "published_at": paper.get("publishedAt"), "topic": "direct-decision-research", "relation": "direct", "verification_level": "abstract_checked", "status": "screened", "retrieved_at": wrapper["retrieved_at"], "retrieval_url": wrapper["retrieval_url"], "abstract_provider": wrapper["provider"], "abstract_sha256": research.sha(abstract), "abstract_word_count": len(abstract.split()), "evidence_excerpt": research.evidence(abstract, ["Jev", "decision"]), "relevance": "Original abstract explicitly discusses Jev or typed decision models; findings remain author-reported.", "screening_method": "Direct Jev/typed-decision title-and-abstract rules; no full-paper review or reproduction.", "full_text_reviewed": False, "canonical_page_separately_fetched": False, "discovery_queries": [query]})
        return records, direct


def as_list(value):
    return value if isinstance(value, list) else []


def direct_paper(title, abstract):
    text = title + " " + abstract
    explicit = bool(re.search(r"typesafe|typed[- ]decision|system[- ]one models?|\brlcd\b", text, re.I))
    if re.search(r"japanese encephalitis|encephalitis virus", text, re.I) and not re.search(r"typesafe", text, re.I):
        return False
    if explicit:
        return bool(re.search(r"decision|probabilit|calibrat", text, re.I))
    return bool(re.search(r"\bjev\b", text, re.I) and re.search(r"\bllms?\b|language models?|artificial intelligence|neural (?:model|network)", text, re.I) and re.search(r"decision|probabilit|calibrat", text, re.I))


def pending_reviews(previous, observed, current_rows):
    """Carry unresolved human review across provider failures; compare capped semantics."""
    current = {identity(r): content_hash(r) for r in current_rows}
    pending = {}
    for item in previous.get("editorial_refresh_candidates", []):
        if isinstance(item, dict) and item.get("url") in current and current[item["url"]] != item.get("observed_content_sha256"):
            pending[item["url"]] = item
    for item in observed:
        prior = pending.get(item["url"])
        if prior and prior.get("observed_content_sha256") == item.get("observed_content_sha256") and prior.get("old_content_sha256") == item.get("old_content_sha256"):
            continue
        pending[item["url"]] = item
    result = [pending[k] for k in sorted(pending)][:100]
    def semantic(items):
        return sorted((r["url"], r.get("old_content_sha256"), r.get("observed_content_sha256")) for r in items)[:100]
    changed = semantic(result) != semantic(previous.get("editorial_refresh_candidates", []))
    return result, changed, len(pending)


def write_if_changed(path, text):
    if path.exists() and path.read_bytes() == text.encode("utf-8"):
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".refresh-tmp")
    temp.write_text(text, encoding="utf-8")
    temp.replace(path)
    return True


def publish_summary(report):
    text = "\n".join(["## Public source scan", "", "Status: **" + report["status"] + "**.", f"Added: {report['added_count']}; updated: {report['changed_count']}; editorial changes awaiting review: {report['editorial_review_required_count']}.", f"Provider/document issues: {report['error_count']}. Earlier evidence was retained on failures.", "", "Automated source screening is not scientific review or reproduction. No source instructions or downloaded code were executed.", ""])
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as f:
            f.write(text)
    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as f:
            f.write("changed=" + str(report["changed"]).lower() + "\n")
            for key in ("added_count", "changed_count", "editorial_review_required_count", "error_count"):
                f.write(key + "=" + str(report[key]) + "\n")


def main(argv=None):
    started_at = now()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=8, help="Public document fetch concurrency (1–16); scholarly API concurrency is at most 3")
    parser.add_argument("--max-new", type=int, default=None, help="Optional cap on newly added records; existing records are retained")
    parser.add_argument("--smoke", action="store_true", help="Small real-network dry-run; do not write ledgers, generated files or scan report")
    args = parser.parse_args(argv)
    if not 1 <= args.workers <= 16 or args.max_new is not None and args.max_new < 0:
        parser.error("workers must be 1–16 and max-new nonnegative")
    paths = [ROOT / "data/ecosystem-sources.jsonl", ROOT / "data/research-sources.jsonl"]
    originals = [Ledger.read(path) for path in paths]
    fetcher = PublicFetcher()
    scan = Scan(fetcher, args.workers)
    limit = min(args.max_new, 5) if args.smoke and args.max_new is not None else 5 if args.smoke else args.max_new
    ecosystem_rows = scan.scan_ecosystem(originals[0], limit, args.smoke)
    research_rows, direct = scan.scan_research(args.smoke)
    merged_ecosystem, ec = merge_records(originals[0], ecosystem_rows + direct, limit)
    remaining = None if limit is None else max(0, limit - len(ec["added"]))
    merged_research, rc = merge_records(originals[1], research_rows, remaining)
    changes = {k: ec[k] + rc[k] for k in ("added", "changed", "editorial_review_required")}
    report_path = ROOT / "data/scan-latest.json"
    previous = json.loads(report_path.read_text()) if report_path.exists() else {}
    pending, pending_changed, pending_count = pending_reviews(previous, changes["editorial_review_required"], merged_ecosystem.rows + merged_research.rows)
    changed = bool(changes["added"] or changes["changed"] or pending_changed)
    successful_content = sum(r.get("verification_level") != "metadata_only" for r in ecosystem_rows) + scan.successful_queries
    status = "failed" if not successful_content else "partial" if scan.errors else "success"
    if status == "failed":
        changed = False
    if not args.smoke:
        for path, ledger in zip(paths, (merged_ecosystem, merged_research)):
            write_if_changed(path, "".join(ledger.lines))
        subprocess.run([sys.executable, str(ROOT / "scripts/build_source_index.py")], cwd=ROOT, check=True)
        counts = json.loads((ROOT / "data/source-counts.json").read_text())["counts"]
    else:
        counts = json.loads((ROOT / "data/source-counts.json").read_text())["counts"]
    report = {"schema_version": 1, "started_at": started_at, "completed_at": now(), "status": status, "changed": changed, "dry_run": args.smoke, "added_count": len(changes["added"]), "changed_count": len(changes["changed"]), "editorial_review_required_count": pending_count, "added_urls": changes["added"][:100], "changed_urls": changes["changed"][:100], "editorial_refresh_candidates": pending, "editorial_examples_truncated": pending_count > 100, "error_count": len(scan.errors), "errors": sorted(scan.errors, key=lambda r: json.dumps(r, sort_keys=True))[:100], "counts": counts, "index_revision": scan.index_revision, "network_requests": fetcher.requests, "excluded_discoveries": scan.excluded, "preserved_after_failure": ec["preserved_after_failure"] + rc["preserved_after_failure"], "duplicate_candidates_skipped": ec["duplicates"] + rc["duplicates"], "privacy_rejected_records": ec["rejected"] + rc["rejected"], "verification_note": "Public document or original-abstract machine screening only; prior reviewed evidence is preserved and changed editorial sources require human review. Metadata-only records do not count as checked sources."}
    # Report every attempt, including failures. The publisher must gate on
    # report.changed, not this report's timestamp or a raw git-diff count.
    if not args.smoke:
        write_if_changed(report_path, json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    publish_summary(report)
    print(json.dumps(report, ensure_ascii=False, indent=2), flush=True)
    return 1 if status == "failed" else 0


if __name__ == "__main__":
    raise SystemExit(main())
