"""Incremental evidence and public-network boundary regressions, no network."""
import hashlib
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

from scripts import refresh_sources as refresh
from scripts import validate


def row(url="https://example.org/source", body="earlier", level="content_screened", **extra):
    return {"url": url, "title": "Fixture source", "topic": "fixture", "relation": "direct",
            "verification_level": level, "retrieved_at": "2026-10-15T00:00:00Z",
            "content_sha256": hashlib.sha256(body.encode()).hexdigest(),
            "relevance": "Synthetic regression fixture.", "checked_via": "Fixture content.", **extra}


def ledger(*rows):
    return refresh.Ledger(list(rows), [json.dumps(r, ensure_ascii=True) + "\r\n" for r in rows])


def catalog(root, papers=()):
    path = root / "site/papers.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"papers": list(papers)}))
    return path


def paper(number=0, **extra):
    return {"category": "Papers", "title": "Jev source fixture " + str(number),
            "url": f"https://arxiv.org/abs/2609.{10000 + number}v1", **extra}


class CuratedDiscoveryTests(unittest.TestCase):
    def test_every_catalog_paper_is_seeded_independent_of_external_search(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            entries = [paper(i) for i in range(7)]
            seeds = refresh.curated_paper_seeds(catalog(root, entries))
            self.assertEqual(set(seeds), {refresh.index.canonical(p["url"]) for p in entries})
            # A later catalog addition must need no collector code change.
            entries.append(paper(7))
            self.assertEqual(len(refresh.curated_paper_seeds(catalog(root, entries))), 8)

    def test_versions_deduplicate_and_excluded_catalog_sources_are_not_fetched(self):
        entries = [paper(), paper(url="https://arxiv.org/pdf/2609.10000v2.pdf"), paper(1)]
        with tempfile.TemporaryDirectory() as tmp:
            seeds = refresh.curated_paper_seeds(catalog(Path(tmp), entries))
        self.assertEqual(len(seeds), 2)
        allowed, excluded = "https://arxiv.org/abs/2609.10000", "https://arxiv.org/abs/2609.10001"
        policy = Mock()
        policy.exclusion.side_effect = lambda url: {"reason": "Fixture exclusion"} if url == excluded else None
        scan = refresh.Scan(refresh.PublicFetcher(), curated_seeds=seeds, policy=policy)
        external = {allowed: {**seeds[allowed], "discovered_from": ["https://example.org/index"]}}
        with patch.object(scan, "discover_index", return_value=([], external)), patch.object(refresh.ecosystem, "audit", side_effect=lambda seed: (row(seed["url"]), [])) as audit, contextlib.redirect_stdout(io.StringIO()):
            records = scan.scan_ecosystem(ledger(row(allowed)))
        self.assertEqual(audit.call_count, 1)
        self.assertEqual(records[0]["url"], allowed)
        self.assertEqual(scan.curation_excluded, {excluded})
        self.assertIn(refresh.CURATED_PAPERS_ORIGIN, audit.call_args.args[0]["discovered_from"])

    def test_catalog_labels_never_replace_fetched_evidence_or_grant_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            seeds = refresh.curated_paper_seeds(catalog(Path(tmp), [paper(verification_level="editorial_reviewed", content_sha256="catalog-claim")]))
        seed = next(iter(seeds.values()))
        self.assertNotIn("verification_level", seed)
        self.assertNotIn("content_sha256", seed)
        raw = b"<html><title>Jev fixture</title><p>" + b"Typed decision models require careful probability calibration and reliable evaluation. " * 8 + b"</p></html>"
        fetcher = Mock()
        fetcher.fetch.return_value = (raw, seed["url"], "text/html")
        scan = refresh.Scan(fetcher, curated_seeds=seeds)
        with patch.object(scan, "discover_index", return_value=([], {})), contextlib.redirect_stdout(io.StringIO()):
            records = scan.scan_ecosystem(ledger())
        self.assertEqual(records[0]["verification_level"], "content_screened")
        self.assertEqual(records[0]["content_sha256"], hashlib.sha256(raw).hexdigest())
        fetcher.fetch.side_effect = refresh.FetchError("network_failure")
        with patch.object(scan, "discover_index", return_value=([], {})), contextlib.redirect_stdout(io.StringIO()):
            failed = scan.scan_ecosystem(ledger())
        self.assertEqual(failed[0]["verification_level"], "metadata_only")
        self.assertNotIn("content_sha256", failed[0])

    def test_malformed_catalog_fails_before_network_without_echoing_input(self):
        invalid = ["https://example.org/paper", "https://127.0.0.1/paper",
                   "https://arxiv.org/abs/2609.10000?token=fixture-sensitive-value",
                   "https://arxiv.org/abs/2609.10000#fragment"]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for url in invalid:
                catalog(root, [paper(url=url)])
                with self.subTest(url=url.split("?", 1)[0]), patch.object(refresh, "ROOT", root), patch.object(refresh.PublicFetcher, "fetch") as fetch, contextlib.redirect_stderr(io.StringIO()) as output:
                    with self.assertRaises(SystemExit) as error:
                        refresh.main([])
                    self.assertEqual(error.exception.code, 2)
                    self.assertIn("invalid_curated_paper_entry_1", output.getvalue())
                    self.assertNotIn(url, output.getvalue())
                    fetch.assert_not_called()
            catalog(root).write_text("not JSON")
            with self.assertRaisesRegex(ValueError, "invalid_curated_paper_catalog"):
                refresh.curated_paper_seeds(root / "site/papers.json")


class DiagnosticTests(unittest.TestCase):
    def test_fixed_fetch_codes_preserved_but_arbitrary_messages_never_logged(self):
        for message in ("http_429", "http_503", "network_failure", "dns_resolution_failed"):
            self.assertEqual(refresh.safe_exception_code(refresh.FetchError(message)), message)
        private_message = "upstream response contains fixture-sensitive-value"
        fetcher = Mock()
        fetcher.fetch.side_effect = refresh.FetchError(private_message)
        scan = refresh.Scan(fetcher)
        scan.query("direct", "Jev", refresh.research.PROVIDER)
        self.assertEqual(scan.errors[0]["code"], "paper_query_failed:unclassified_fetch_error")
        self.assertNotIn(private_message, json.dumps(scan.errors))
        fetcher.fetch.side_effect = refresh.FetchError("http_429")
        with patch.object(refresh.time, "sleep"):
            scan.query("direct", "Jev", refresh.research.PROVIDER)
        self.assertEqual(scan.errors[1]["code"], "paper_query_failed:http_429")

    def test_error_totals_cover_all_issues_even_when_examples_are_truncated(self):
        issues = [{"url": f"https://example.org/source-{i}", "code": "unavailable"} for i in range(101)]
        issues += [{"url": "https://example.org/query", "code": "paper_query_failed:http_429"}]
        report = refresh.error_report(issues)
        self.assertEqual(report["error_count"], 102)
        self.assertEqual(report["error_examples_count"], 100)
        self.assertTrue(report["error_examples_truncated"])
        self.assertEqual(report["error_code_counts"], {"paper_query_failed:http_429": 1, "unavailable": 101})
        empty = refresh.error_report([])
        self.assertFalse(empty["error_examples_truncated"])
        self.assertEqual(empty["error_code_counts"], {})


class IncrementalEvidenceTests(unittest.TestCase):
    def test_canonical_body_fetch_updates_only_page_provenance_not_review_scope(self):
        url = "https://arxiv.org/abs/2609.12345"
        prior = row(url, level="abstract_checked", abstract_provider="huggingface_papers_api",
                    abstract_sha256=hashlib.sha256(b"original abstract").hexdigest(),
                    canonical_page_separately_fetched=False, full_text_reviewed=False,
                    editorial_reviewed=False)
        prior.pop("content_sha256")
        fresh = row(url, body="primary page", status="screened", retrieved_url=url + "v2")
        result, _ = refresh.merge_records(ledger(prior), [fresh])
        updated = result.rows[0]
        self.assertTrue(updated["canonical_page_separately_fetched"])
        for field in ("abstract_provider", "abstract_sha256", "full_text_reviewed", "editorial_reviewed"):
            self.assertEqual(updated[field], prior[field])
        self.assertEqual(updated["verification_level"], "content_screened")

    def test_same_body_legacy_flag_repair_preserves_dates_and_other_evidence(self):
        url = "https://arxiv.org/abs/2609.12345"
        prior = row(url, status="screened", canonical_page_separately_fetched=False,
                    abstract_provider="huggingface_papers_api", full_text_reviewed=False,
                    editorial_reviewed=False, editorial_note="Retain this note")
        fresh = row(url, status="screened", retrieved_url=url,
                    retrieved_at="2026-10-16T00:00:00Z", title="Changed automatic title")
        result, changes = refresh.merge_records(ledger(prior), [fresh])
        self.assertEqual(result.rows[0], {**prior, "canonical_page_separately_fetched": True})
        self.assertEqual(changes["changed"], [url])
        # Repeating the same observation becomes a byte-identical no-op.
        repeated, repeated_changes = refresh.merge_records(result, [fresh])
        self.assertEqual(repeated.lines, result.lines)
        self.assertEqual(repeated_changes["changed"], [])

    def test_mirror_body_does_not_substantiate_a_canonical_page_claim(self):
        url = "https://arxiv.org/abs/2609.12345"
        prior = row(url, canonical_page_separately_fetched=False,
                    abstract_provider="huggingface_papers_api", full_text_reviewed=False,
                    editorial_reviewed=False)
        fresh = row(url, body="changed mirror body", status="screened",
                    retrieved_url="https://example.org/paper-mirror",
                    canonical_page_separately_fetched=True)
        result, _ = refresh.merge_records(ledger(prior), [fresh])
        self.assertFalse(result.rows[0]["canonical_page_separately_fetched"])
        self.assertFalse(result.rows[0]["full_text_reviewed"])
        self.assertFalse(result.rows[0]["editorial_reviewed"])

    def test_canonical_page_flag_requires_body_hash_and_screened_status(self):
        url = "https://arxiv.org/abs/2609.12345"
        valid = row(url, status="screened", retrieved_url=url)
        for candidate in [dict(valid, status="unavailable"),
                          dict(valid, content_sha256=""),
                          dict(valid, verification_level="abstract_checked"),
                          dict(valid, retrieved_url=None)]:
            with self.subTest(candidate_status=candidate.get("status")):
                self.assertFalse(refresh.canonical_page_observed(candidate))

    def test_unchanged_hash_preserves_exact_old_record_bytes_and_manual_fields(self):
        prior = row(editorial_note="Manually inspected evidence", title="Corrected title")
        old = ledger(prior)
        new = row(retrieved_at="2026-10-16T00:00:00Z", title="Automatically extracted title")
        result, changes = refresh.merge_records(old, [new])
        self.assertEqual(result.lines, old.lines)
        self.assertEqual(result.rows, old.rows)
        self.assertFalse(changes["added"] or changes["changed"])

    def test_partial_failure_keeps_prior_success_and_accepts_new_source(self):
        old = ledger(row())
        failed = row(level="metadata_only", status="unavailable")
        failed.pop("content_sha256")
        added = row("https://example.org/new", body="new evidence")
        result, changes = refresh.merge_records(old, [failed, added])
        self.assertEqual(result.lines[0], old.lines[0])
        self.assertEqual(len(result.rows), 2)
        self.assertEqual(changes["preserved_after_failure"], 1)

    def test_missing_provider_results_never_remove_prior_rows(self):
        old = ledger(row(), row("https://example.org/second", body="second"))
        result, changes = refresh.merge_records(old, [])
        self.assertEqual(result, old)
        self.assertEqual(changes["added"], [])

    def test_changed_editorial_source_is_preserved_pending_human_review(self):
        old = ledger(row(level="editorial_reviewed", editorial_note="Reviewed original"))
        fresh = row(body="new source revision")
        result, changes = refresh.merge_records(old, [fresh])
        self.assertEqual(result.lines, old.lines)
        self.assertEqual(len(changes["editorial_review_required"]), 1)
        self.assertEqual(changes["editorial_review_required"][0]["observed_content_sha256"], fresh["content_sha256"])

    def test_automated_new_record_never_receives_editorial_tier(self):
        result, _ = refresh.merge_records(ledger(), [row(level="editorial_reviewed")])
        self.assertEqual(result.rows[0]["verification_level"], "content_screened")

    def test_lower_evidence_tier_does_not_replace_fuller_prior_evidence(self):
        old = ledger(row())
        result, _ = refresh.merge_records(old, [row(body="abstract revision", level="abstract_checked")])
        self.assertEqual(result.lines, old.lines)

    def test_duplicate_versions_and_mirrored_content_do_not_inflate_additions(self):
        a = row("https://arxiv.org/abs/2609.12345v1", body="paper")
        b = row("https://arxiv.org/pdf/2609.12345v2.pdf", body="paper")
        c = row("https://example.org/mirror", body="paper")
        result, changes = refresh.merge_records(ledger(), [a, b, c])
        self.assertEqual(len(result.rows), 1)
        self.assertEqual(len(changes["added"]), 1)

    def test_max_new_limits_only_additions_not_existing_rows(self):
        old = ledger(row())
        incoming = [row("https://example.org/a", "a"), row("https://example.org/b", "b")]
        result, changes = refresh.merge_records(old, incoming, max_new=1)
        self.assertEqual(result.lines[0], old.lines[0])
        self.assertEqual(len(changes["added"]), 1)

    def test_metadata_only_new_source_is_tracked_with_its_original_tier(self):
        result, _ = refresh.merge_records(ledger(), [row(level="metadata_only", status="unavailable")])
        self.assertEqual(result.rows[0]["verification_level"], "metadata_only")

    def test_ledger_read_and_noop_preserve_crlf_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sources.jsonl"
            raw = ledger(row()).lines[0].encode()
            path.write_bytes(raw)
            loaded = refresh.Ledger.read(path)
            result, _ = refresh.merge_records(loaded, [row(retrieved_at="later")])
            self.assertFalse(refresh.write_if_changed(path, "".join(result.lines)))
            self.assertEqual(path.read_bytes(), raw)

    def test_pending_review_survives_fetch_failure_and_same_hash_new_snapshot_url(self):
        old = row(level="editorial_reviewed")
        fresh = row(body="changed", retrieved_url="https://example.org/revision-a")
        _, change = refresh.merge_records(ledger(old), [fresh])
        previous = {"editorial_refresh_candidates": change["editorial_review_required"]}
        pending, changed, _ = refresh.pending_reviews(previous, [], [old])
        self.assertEqual(pending, previous["editorial_refresh_candidates"])
        self.assertFalse(changed)
        observed = [dict(pending[0], retrieved_url="https://example.org/revision-b")]
        pending2, changed2, _ = refresh.pending_reviews(previous, observed, [old])
        self.assertEqual(pending2, pending)
        self.assertFalse(changed2)

    def test_more_than_100_pending_examples_do_not_create_repeated_changes(self):
        old = [row(f"https://example.org/source-{i:03}", level="editorial_reviewed") for i in range(120)]
        fresh = [dict(r, content_sha256=hashlib.sha256(b"new").hexdigest(), verification_level="content_screened") for r in old]
        _, changes = refresh.merge_records(ledger(*old), fresh)
        pending, _, count = refresh.pending_reviews({}, changes["editorial_review_required"], old)
        self.assertEqual(count, 120)
        self.assertEqual(len(pending), 100)
        _, changed, _ = refresh.pending_reviews({"editorial_refresh_candidates": pending}, changes["editorial_review_required"], old)
        self.assertFalse(changed)


class PublicFetchTests(unittest.TestCase):
    def test_discovery_excludes_inference_api_and_normalizes_acl_pdf(self):
        with self.assertRaises(refresh.FetchError):
            refresh.canonical_source("https://api.codiv.ai/v1/systemone")
        self.assertEqual(refresh.canonical_source("https://aclanthology.org/2025.gem-1.63.pdf"), "https://aclanthology.org/2025.gem-1.63")

    def test_invalid_protocol_private_ip_and_credential_urls_are_rejected(self):
        credentials = "https://" + "fixture-user" + ":" + "fixture-password" + "@example.org/source"
        for url in ["file:///fixture", "ftp://example.org/a", "http://127.0.0.1/a", "https://[::1]/a", "http://example.internal/a", "https://example.org/?token=fixture", credentials]:
            with self.subTest(url=url.split(":", 1)[0]):
                with self.assertRaises(refresh.FetchError):
                    refresh.public_url(url)

    def test_redirect_to_private_address_is_rejected_before_second_request(self):
        client = refresh.PublicFetcher()
        with patch.object(client, "_request", return_value=(302, {"location": "http://127.0.0.1/private"}, b"")) as request:
            with self.assertRaises(refresh.FetchError):
                client.fetch("https://example.org/source")
            self.assertEqual(request.call_count, 1)

    def test_mixed_public_private_dns_rejected_before_connection(self):
        answers = [(2, 1, 6, "", ("93.184.216.34", 443)), (2, 1, 6, "", ("127.0.0.1", 443))]
        with patch.object(refresh.socket, "getaddrinfo", return_value=answers), patch.object(refresh.http.client, "HTTPSConnection") as connection:
            with self.assertRaises(refresh.FetchError):
                refresh.PublicFetcher()._request("https://example.org/source")
            connection.assert_not_called()

    def test_connection_pins_public_ip_but_retains_tls_hostname(self):
        response = Mock(status=200)
        response.getheaders.return_value = [("Content-Type", "text/plain")]
        response.read.return_value = b"public fixture"
        connection = Mock()
        connection.getresponse.return_value = response
        connection.request.side_effect = lambda *a, **k: connection._create_connection(("ignored.example", 443), 18)
        with patch.object(refresh, "public_addresses", return_value=["93.184.216.34"]), patch.object(refresh.http.client, "HTTPSConnection", return_value=connection) as https, patch.object(refresh.socket, "create_connection") as socket_connect:
            refresh.PublicFetcher()._request("https://example.org/source")
            self.assertEqual(https.call_args.args[:2], ("example.org", 443))
            self.assertEqual(socket_connect.call_args.args[0], ("93.184.216.34", 443))

    def test_retry_backoff_accepts_transient_failure_without_exposing_response(self):
        client = refresh.PublicFetcher(retries=2)
        replies = [(429, {"retry-after": "0"}, b""), (503, {}, b""), (200, {"content-type": "text/plain"}, b"ok")]
        with patch.object(client, "_request", side_effect=replies) as request, patch.object(refresh.time, "sleep"):
            self.assertEqual(client.fetch("https://example.org/source")[0], b"ok")
            self.assertEqual(request.call_count, 3)

    def test_body_cache_has_total_byte_budget(self):
        client = refresh.PublicFetcher(cache_bytes=5)
        with patch.object(client, "_request", return_value=(200, {}, b"four")):
            client.fetch("https://example.org/a")
            client.fetch("https://example.org/b")
        self.assertLessEqual(client.cached_bytes, 5)
        self.assertEqual(list(client.cache), ["https://example.org/b"])

    def test_biomedical_jev_is_not_direct_ai_research(self):
        self.assertFalse(refresh.direct_paper("Japanese encephalitis virus (JEV)", "A neural model supports clinical decisions using JEV infection probabilities."))
        self.assertTrue(refresh.direct_paper("Jev evaluation", "TypeSafe's typed decision model is evaluated for probability calibration."))


class RefreshRunTests(unittest.TestCase):
    def test_new_direct_paper_satisfies_the_public_ledger_schema(self):
        scan = refresh.Scan(refresh.PublicFetcher())
        abstract = "TypeSafe Jev is a typed decision model. " + "This synthetic fixture discusses probability calibration and model evaluation. " * 5
        wrapper = {"data": [{"paper": {"id": "2609.12345", "title": "Jev calibration fixture", "summary": abstract, "authors": [{"name": "Fixture Author"}]}}], "retrieved_at": "2026-10-15T00:00:00Z", "retrieval_url": "https://huggingface.co/api/papers/search?q=Jev", "provider": "huggingface_papers_api", "http_status": 200}
        with patch.object(scan, "query", side_effect=lambda topic, q, provider: (topic, q, wrapper)):
            _, direct = scan.scan_research(smoke=True)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sources.jsonl"
            path.write_text(json.dumps(direct[0]) + "\n")
            with patch.object(validate, "ROOT", Path(tmp)), patch.object(validate, "errors", []) as errors:
                validate.check_ledger(path)
                self.assertEqual(errors, [])

    def test_all_provider_failures_return_failure_and_preserve_previous_ledger(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "data").mkdir()
            original = "".join(ledger(row()).lines)
            (root / "data/ecosystem-sources.jsonl").write_bytes(original.encode())
            (root / "data/research-sources.jsonl").write_text("")
            (root / "data/source-counts.json").write_text(json.dumps({"counts": {"checked_sources": 1}}))
            catalog(root)
            with patch.object(refresh, "ROOT", root), patch.object(refresh.Scan, "scan_ecosystem", return_value=[]), patch.object(refresh.Scan, "scan_research", return_value=([], [])), patch.object(refresh.subprocess, "run"), patch.dict(refresh.os.environ, {}, clear=True), contextlib.redirect_stdout(io.StringIO()):
                code = refresh.main([])
            report = json.loads((root / "data/scan-latest.json").read_text())
            self.assertEqual(code, 1)
            self.assertEqual(report["status"], "failed")
            self.assertFalse(report["changed"])
            self.assertEqual((root / "data/ecosystem-sources.jsonl").read_bytes(), original.encode())

    def test_smoke_does_not_write_ledgers_or_report_or_build_index(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "data").mkdir()
            (root / "data/source-counts.json").write_text(json.dumps({"counts": {}}))
            catalog(root)
            with patch.object(refresh, "ROOT", root), patch.object(refresh.Scan, "scan_ecosystem", return_value=[row()]), patch.object(refresh.Scan, "scan_research", return_value=([], [])), patch.object(refresh.subprocess, "run") as build, patch.dict(refresh.os.environ, {}, clear=True), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(refresh.main(["--smoke"]), 0)
            build.assert_not_called()
            self.assertFalse((root / "data/scan-latest.json").exists())
            self.assertFalse((root / "data/ecosystem-sources.jsonl").exists())


if __name__ == "__main__":
    unittest.main()
