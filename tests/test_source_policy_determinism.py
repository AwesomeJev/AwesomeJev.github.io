"""Display annotations must serialize consistently across Python processes."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


class PolicyDeterminismTests(unittest.TestCase):
    def test_annotation_output_is_independent_of_python_hash_seed(self):
        annotation = {
            "url": "https://example.org/paper",
            "title": "Verified title",
            "first_submitted": "2024-01-01",
            "topic": "calibration",
            "relation": "background",
            "relevance": "Probability calibration methods.",
            "note": "Metadata fixture, not a scientific assessment.",
            "evidence_url": "https://example.org/paper",
            "reviewed_at": "2026-10-16T00:00:00Z",
        }
        code = (
            "import json,sys; from pathlib import Path; "
            "from scripts.source_policy import load_policy; "
            "policy=load_policy(Path(sys.argv[1]), lambda url:url); "
            "print(json.dumps(policy.apply({'url':'https://example.org/paper'})))"
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "policy.json"
            path.write_text(json.dumps({"schema_version": 1, "exclusions": [], "annotations": [annotation]}))
            outputs = [
                subprocess.check_output(
                    [sys.executable, "-c", code, str(path)],
                    cwd=Path(__file__).resolve().parents[1],
                    env={**os.environ, "PYTHONHASHSEED": seed},
                )
                for seed in ("1", "2", "42")
            ]
        self.assertEqual(len(set(outputs)), 1)
