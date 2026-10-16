# Source ledgers

This directory makes discovery and screening inspectable. It does not claim that every resource is high quality or that every experiment has been independently reproduced.

| File | Role |
| --- | --- |
| `ecosystem-sources.jsonl` | Direct and adjacent ecosystem sources, retrieved page evidence, provenance, and content hashes. |
| `research-sources.jsonl` | Direct studies and background research, with primary-page or scholarly-API abstract provenance and explicit screening scope. |
| `ecosystem-sources.excluded.jsonl` | Candidates excluded by the ecosystem screen. |
| `source-curation.json` | Maintainer-reviewed exclusions and display-only metadata corrections, with primary-source evidence. |
| `source-counts.json` | Counts after cross-ledger URL, content-hash, and paper-title deduplication. |

Verification levels are `editorial_reviewed`, `content_screened`, `abstract_checked`, and `metadata_only`. The first denotes targeted editorial inspection; the next two record source-page or original-abstract checks at the scope stated in each record. Metadata-only entries and failed fetches do not count as checked content. Abstracts supplied through an index API do not imply that the original publisher page was fetched.

Read [the audit methodology](../docs/source-audit.md). Generate the browser index with:

```sh
python3 scripts/build_source_index.py
```

The ledgers retain minimal evidence and public bibliographic facts, not full articles or model weights. Third-party excerpts and linked resources retain their original rights and licenses; the project's MIT license applies to original project code and writing.

The [2026-10-16 curated-paper reconciliation](curated-paper-refresh-2026-10-16.json) records a separate seven-page targeted fetch, distinct from the scheduled scan report. Its evidence lives in the ecosystem ledger; see the [review](../docs/reviews/scan-2026-10-16.md#scheduled-scan-review-pr-3-and-curated-paper-reconciliation).


The expansion baseline, intake and progress files document the user-requested addition of more than 300 genuinely new resources. The baseline fixes the pre-expansion commit and known identities/evidence. The intake records accepted public URLs; the progress report counts only new, nonduplicate, evidence-checked intake entries. Their presence does not imply full-paper review or model execution. See [the reviewed directory](../docs/expansion-2026-10-16.md).

Primary arXiv abstract imports use `abstract_provider: arxiv_primary_abstract_page`, a same-paper fixed `reviewed_version_url`, its matching `reviewed_version`, a primary-page SHA-256, and `canonical_page_separately_fetched: true`. Keep initial submission in `published_at` / `first_submitted` and the inspected revision date in `reviewed_version_date`. The validator rejects aliases that would bypass the scanner's version protection, conflicting URL identities and missing primary-page evidence. Index-supplied abstracts retain their own provider provenance; they are not required to claim a separately fetched primary page.
