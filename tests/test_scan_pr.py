"""Security and idempotence checks for the scan-to-PR publication boundary."""

import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts import open_scan_pr as scan


IDENTITY = {"repository": scan.REPOSITORY, "base_sha": "a" * 40, "run_id": "123", "run_attempt": "1"}
OLD_SHA = "b" * 40


def files(retrieved_at="2026-10-15T00:00:00Z", content="public evidence"):
    row = {"url": "https://example.org/source", "title": "Synthetic source", "retrieved_at": retrieved_at, "evidence": content}
    data = {name: b"{}\n" for name in scan.ALLOWED}
    for name in scan.LEDGERS:
        data[name] = (json.dumps(row) + "\n").encode()
    data["data/scan-latest.json"] = json.dumps({"status": "success", "changed": True, "added_count": 1, "changed_count": 0}).encode()
    return data


def artifact(directory, payload, identity=IDENTITY):
    manifest = {"format": 1, **identity, "changed": True, "files": {}}
    for name, data in payload.items():
        path = directory / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        manifest["files"][name] = {"sha256": scan.digest(data), "bytes": len(data)}
    (directory / "manifest.json").write_text(json.dumps(manifest))


class FakeGitHub:
    """No network; unexpected API writes fail the test."""

    def __init__(self, previous=False, opened=False, closed=False, owner=scan.BOT, main_sha=IDENTITY["base_sha"]):
        self.previous, self.opened, self.closed, self.owner, self.main_sha = previous, opened, closed, owner, main_sha
        self.calls = []

    def request(self, method, endpoint, data=None, optional=False):
        self.calls.append((method, endpoint, data))
        if method == "GET":
            if endpoint == "/git/ref/heads/main":
                return {"object": {"sha": self.main_sha}}
            if endpoint == "/git/ref/heads/" + scan.BRANCH:
                return {"object": {"sha": OLD_SHA}} if self.previous else None
            if endpoint.startswith("/pulls?"):
                if "state=closed" in endpoint:
                    return [{"number": 7, "merged_at": None}] if self.closed else []
                return [{"number": 7, "user": {"login": scan.BOT}, "body": scan.MARKER}] if self.opened else []
            if endpoint == "/commits/" + OLD_SHA:
                return {"committer": {"login": self.owner}, "commit": {"message": scan.TITLE}}
            if endpoint == "/git/commits/" + IDENTITY["base_sha"]:
                return {"tree": {"sha": "d" * 40}}
        if method == "POST" and endpoint in {"/git/blobs", "/git/trees", "/git/commits"}:
            return {"sha": "c" * 40}
        if method == "POST" and endpoint == "/git/refs":
            return {"ref": data["ref"]}
        if method == "PATCH" and endpoint == "/git/refs/heads/" + scan.BRANCH:
            return {"ref": "refs/heads/" + scan.BRANCH}
        if (method, endpoint) in {("POST", "/pulls"), ("PATCH", "/pulls/7")}:
            return {"html_url": "https://github.com/" + scan.REPOSITORY + "/pull/7"}
        raise AssertionError("Unexpected API operation: " + method + " " + endpoint)


class ArtifactBoundaryTests(unittest.TestCase):
    def test_timestamp_only_changes_do_not_create_substantive_updates(self):
        self.assertEqual(scan.meaningful_fingerprint(files()), scan.meaningful_fingerprint(files("2026-10-16T00:00:00Z")))
        self.assertNotEqual(scan.meaningful_fingerprint(files()), scan.meaningful_fingerprint(files(content="changed public evidence")))

    def test_editorial_only_hash_changes_are_substantive_without_clock_churn(self):
        baseline = files()
        candidate = files()
        report = json.loads(candidate[scan.REPORT])
        report["editorial_refresh_candidates"] = [{"url": "https://example.org/source", "old_content_sha256": "a" * 64, "observed_content_sha256": "b" * 64, "retrieved_at": "2026-10-15T00:00:00Z"}]
        candidate[scan.REPORT] = json.dumps(report).encode()
        self.assertNotEqual(scan.meaningful_fingerprint(baseline), scan.meaningful_fingerprint(candidate))
        first = scan.meaningful_fingerprint(candidate)
        report["started_at"] = "2026-10-16T00:00:00Z"
        report["editorial_refresh_candidates"][0]["retrieved_at"] = "2026-10-16T00:00:00Z"
        candidate[scan.REPORT] = json.dumps(report).encode()
        self.assertEqual(first, scan.meaningful_fingerprint(candidate))
        without_report = {name: value for name, value in baseline.items() if name != scan.REPORT}
        self.assertEqual(scan.meaningful_fingerprint(without_report), scan.meaningful_fingerprint(baseline))

    def test_manifest_is_bound_to_run_and_source_commit(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            artifact(directory, files())
            _, loaded = scan.load_bundle(directory, IDENTITY)
            self.assertEqual(set(loaded), set(scan.ALLOWED))
            for key, value in (("run_id", "124"), ("run_attempt", "2"), ("base_sha", "e" * 40)):
                with self.subTest(key=key), self.assertRaises(scan.ScanError):
                    scan.load_bundle(directory, {**IDENTITY, key: value})

    def test_extra_code_file_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            artifact(directory, files())
            (directory / "injected.py").write_text("# Must never cross the artifact boundary\n")
            with self.assertRaises(scan.ScanError):
                scan.load_bundle(directory, IDENTITY)

    def test_symlink_and_hash_mismatch_are_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary) / "bundle"
            directory.mkdir()
            artifact(directory, files())
            target = directory / scan.ALLOWED[0]
            target.write_bytes(target.read_bytes() + b"\n")
            with self.assertRaises(scan.ScanError):
                scan.load_bundle(directory, IDENTITY)
            target.unlink()
            target.symlink_to(Path(temporary) / "elsewhere.jsonl")
            with self.assertRaises(scan.ScanError):
                scan.load_bundle(directory, IDENTITY)


class PublicationTests(unittest.TestCase):
    def test_main_advance_or_human_branch_edits_prevent_writes(self):
        for api in (FakeGitHub(main_sha="f" * 40), FakeGitHub(previous=True, owner="fixture-maintainer")):
            with self.subTest(api=api), self.assertRaises(scan.ScanError):
                scan.publish(api, IDENTITY, files())
            self.assertTrue(all(method == "GET" for method, _, _ in api.calls))

    def test_identical_pending_or_declined_update_is_not_reposted(self):
        for api in (FakeGitHub(previous=True, opened=True), FakeGitHub(previous=True, closed=True)):
            with self.subTest(api=api), patch.object(scan, "remote_comparison_files", return_value=files()):
                scan.publish(api, IDENTITY, files("2026-10-16T00:00:00Z"))
                self.assertTrue(all(method == "GET" for method, _, _ in api.calls))

    def test_new_pr_writes_only_allowlisted_data_to_dedicated_branch(self):
        api = FakeGitHub()
        scan.publish(api, IDENTITY, files())
        tree = next(data for method, endpoint, data in api.calls if (method, endpoint) == ("POST", "/git/trees"))
        self.assertEqual({row["path"] for row in tree["tree"]}, set(scan.ALLOWED))
        refs = [data for method, endpoint, data in api.calls if (method, endpoint) == ("POST", "/git/refs")]
        self.assertEqual(refs, [{"ref": "refs/heads/" + scan.BRANCH, "sha": "c" * 40}])
        pr = next(data for method, endpoint, data in api.calls if (method, endpoint) == ("POST", "/pulls"))
        self.assertEqual(pr["base"], "main")
        self.assertIn("/actions/runs/123", pr["body"])
        self.assertLessEqual(len(pr["body"]), 6000)
        self.assertNotIn("auto_merge", pr)

    def test_existing_bot_branch_is_updated_without_force_and_pr_is_reused(self):
        api = FakeGitHub(previous=True, opened=True)
        with patch.object(scan, "remote_comparison_files", return_value=files(content="older public evidence")):
            scan.publish(api, IDENTITY, files())
        ref = next(data for method, endpoint, data in api.calls if method == "PATCH" and endpoint.startswith("/git/refs/"))
        self.assertIs(ref["force"], False)
        commit = next(data for method, endpoint, data in api.calls if (method, endpoint) == ("POST", "/git/commits"))
        self.assertEqual(commit["parents"], [OLD_SHA, IDENTITY["base_sha"]])
        self.assertTrue(any(method == "PATCH" and endpoint == "/pulls/7" for method, endpoint, _ in api.calls))
        self.assertFalse(any(method == "POST" and endpoint == "/pulls" for method, endpoint, _ in api.calls))


if __name__ == "__main__":
    unittest.main()
