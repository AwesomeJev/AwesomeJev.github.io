"""Check publisher badges on actual curated resources in both languages."""

from pathlib import Path
import shutil
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(shutil.which("node"), "Node is required for shared renderer checks")
class ResourceProvenanceTests(unittest.TestCase):
    def test_community_additions_do_not_inherit_the_official_badge(self):
        script = r'''
import assert from "node:assert/strict";
import {resources, translations} from "./site/catalog.mjs";
import {renderResource} from "./site/resource-view.mjs";
const cases = [
  ["https://github.com/bufbuild/protoc-gen-jev", "Community resource", "社区资源"],
  ["https://github.com/evan-py-chen/jev-survey", "Community resource", "社区资源"],
  ["https://github.com/earino/zero-shot-complaint-benchmark", "Community resource", "社区资源"],
  ["https://github.com/typesafe-ai/typesafe-sdk-python", "Official", "官方资源"],
  ["https://github.com/typesafe-ai/WorkflowEvals", "Official", "官方资源"],
];
for (const [url, en, zh] of cases) {
  const resource = resources.find(row => row.url === url);
  assert.ok(resource, `Missing regression resource: ${url}`);
  for (const [language, expected] of [["en", en], ["zh", zh]]) {
    const markup = renderResource(resource, language, translations);
    const badge = markup.match(/class="resource-provenance">([^<]+)</)?.[1];
    assert.equal(badge, expected, `${language}: ${url}`);
  }
}
'''
        result = subprocess.run(["node", "--input-type=module", "-e", script],
                                cwd=ROOT, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
