"""Prevent primary-abstract imports from bypassing fixed-version protection."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts import validate


class PrimaryAbstractSchemaTests(unittest.TestCase):
    def check(self, **changes):
        row = {
            "url": "https://arxiv.org/abs/2609.10000", "title": "Fixture paper",
            "topic": "direct-decision-research", "relation": "direct",
            "retrieved_at": "2026-10-16T00:00:00Z", "verification_level": "abstract_checked",
            "relevance": "Synthetic schema regression fixture.", "abstract_sha256": "a" * 64,
            "abstract_page_sha256": "b" * 64, "abstract_word_count": 50,
            "retrieval_status": "success", "http_status": 200, "screening_method": "Fixture abstract check.",
            "abstract_provider": "arxiv_primary_abstract_page", "editorial_reviewed": False,
            "canonical_page_separately_fetched": True, "reviewed_version": "v2",
            "reviewed_version_url": "https://arxiv.org/abs/2609.10000v2",
        }
        row.update(changes)
        with tempfile.TemporaryDirectory() as tmp, patch.object(validate, "errors", []):
            root = Path(tmp)
            path = root / "sources.jsonl"
            path.write_text(json.dumps(row) + "\n")
            with patch.object(validate, "ROOT", root):
                validate.check_ledger(path)
            return list(validate.errors)

    def test_valid_primary_evidence_passes_without_requiring_new_optional_dates(self):
        self.assertEqual(self.check(), [])

    def test_provider_and_version_aliases_cannot_bypass_version_protection(self):
        errors = self.check(abstract_provider="arxiv_primary_page", reviewed_version_url=None,
                            reviewed_version=None, version_url="https://arxiv.org/abs/2609.10000v2", version="v2")
        self.assertTrue(any("version-protected provider" in e for e in errors))
        self.assertTrue(any("reviewed version URL" in e for e in errors))

    def test_different_paper_or_version_cannot_supply_the_pinned_identity(self):
        for url in ("https://arxiv.org/abs/2609.10001v2", "https://arxiv.org/abs/2609.10000v3"):
            with self.subTest(url=url):
                self.assertTrue(any("reviewed version URL" in e for e in self.check(reviewed_version_url=url)))

    def test_missing_primary_fetch_evidence_is_rejected(self):
        for changes in ({"abstract_page_sha256": ""}, {"abstract_page_sha256": int("1" * 64)},
                        {"canonical_page_separately_fetched": False}, {"canonical_page_separately_fetched": 1}):
            with self.subTest(changes=changes):
                self.assertTrue(any("primary-page evidence" in e for e in self.check(**changes)))

    def test_conflicting_url_fields_cannot_bypass_the_scanner_identity_check(self):
        for url in ("https://arxiv.org/abs/2609.10001", "https://[invalid-host/"):
            with self.subTest(url=url):
                errors = self.check(canonical_url="https://arxiv.org/abs/2609.10000", url=url)
                self.assertTrue(any("canonical identity must match" in e for e in errors))

    def test_index_supplied_abstracts_do_not_need_primary_page_fields(self):
        for provider in ("huggingface_papers_api", "openalex_api"):
            with self.subTest(provider=provider):
                self.assertEqual(self.check(abstract_provider=provider, reviewed_version=None,
                                           reviewed_version_url=None, abstract_page_sha256=None,
                                           canonical_page_separately_fetched=False), [])


if __name__ == "__main__":
    unittest.main()
