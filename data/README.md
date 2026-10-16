# Source ledgers

This directory makes discovery and screening inspectable. It does not claim that every resource is high quality or that every experiment has been independently reproduced.

| File | Role |
| --- | --- |
| `ecosystem-sources.jsonl` | Direct and adjacent ecosystem sources, retrieved page evidence, provenance, and content hashes. |
| `research-sources.jsonl` | Background research identified through public scholarly APIs, with abstract-level provenance and screening rules. |
| `ecosystem-sources.excluded.jsonl` | Candidates excluded by the ecosystem screen. |
| `source-counts.json` | Counts after cross-ledger URL, content-hash, and paper-title deduplication. |

Verification levels are `editorial_reviewed`, `content_screened`, `abstract_checked`, and `metadata_only`. The first denotes targeted editorial inspection; the next two denote automated screening of retrieved content or abstracts. Metadata-only entries and failed fetches do not count as checked content. Abstracts supplied through an index API do not imply that the original publisher page was fetched.

Read [the audit methodology](../docs/source-audit.md). Generate the browser index with:

```sh
python3 scripts/build_source_index.py
```

The ledgers retain minimal evidence and public bibliographic facts, not full articles or model weights. Third-party excerpts and linked resources retain their original rights and licenses; the project's MIT license applies to original project code and writing.
