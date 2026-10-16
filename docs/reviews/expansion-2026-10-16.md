# Review of the resource expansion

The expansion is measured against [commit 3519c15](https://github.com/reacher-z/Awesome-Jev/tree/3519c15d7e00686a8dbf9b1e184c68726327ab1e), not against zero. The baseline contained 3,495 unique indexed sources and 67 curated entries. The [frozen baseline](../../data/expansion-baseline-2026-10-16.json) records known identities and evidence; an [exclusion-only supplement](../../data/expansion-baseline-supplement-2026-10-16.json), derived entirely from that same commit, adds older citations and title variants initially missed by extraction. It does not change the baseline or admit new resources.

## Accepted intake

| Batch | Accepted into the ledgers | Evidence depth |
| --- | ---: | --- |
| GitHub projects | 130 | Public README content screening; original short relevance summaries. |
| Hugging Face artifacts | 146 | Public model, dataset, evaluation-archive or Space card screening. |
| Primary guides and evaluations | 34 | Substantive official documentation and primary evaluation/report pages. |
| Research papers | 345 | Original-abstract checks via Hugging Face or reconstruction from OpenAlex metadata. |
| **Total** | **655** | **310 content-screened resources and 345 abstract-checked papers.** |

All accepted identities are listed in the [intake](../../data/expansion-intake-2026-10-16.json). The [generated progress report](../../data/expansion-progress-2026-10-16.json) independently excludes prior URLs, repository/README aliases, arXiv DOI aliases, duplicate evidence hashes, duplicate paper titles, unreviewed additions and metadata-only records. Its count remains 655 after the baseline supplement and alias checks. Source artifacts are not necessarily independent models, test sets or studies.

The new sources comprise 290 directly related resources, 24 adjacent resources and 341 background-method papers. The relationship labels distinguish relevance to Jev from evidence about TypeSafe's proprietary implementation. The expanded directory and its Chinese counterpart display every accepted source, its relationship, and its evidence tier directly in HTML.

## Scope and corrections

The independent [batch-review record](../../data/expansion-review-2026-10-16.json) retains exclusion reasons, primary evidence URLs, metadata corrections and review limits. This is assisted maintenance review, not a claim that every full paper or every codebase was manually examined.

- The final GitHub review removed six of 136 proposed projects: prospective-only integration, a chat-routing false positive, a fork/port counted separately, a connectivity-only example and a changed README whose remaining work included Jev. Seventeen ambiguous primary READMEs were refetched; sixteen matched their input hashes, and the changed case was excluded. Accepted descriptions were rewritten as original short summaries.
- The Hugging Face review removed two sampled/repackaged datasets from 148 proposals. Fifteen selected public cards were refetched and matched the retained hashes. Two model-namespace repositories contain experiment code and are categorized as projects, not model weights. Separate metadata annotations correct JEVal and Granite titles and identify the Tetris artifact as a simulation using measured constants. A soft-label dataset annotation avoids treating edited teacher probabilities as independently established calibration.
- The paper review removed 22 of 367 proposals: five conference recordings, one project record, six thesis records and ten scope mismatches. All input abstract hashes were checked against the retained provider snapshots; 45 targeted abstracts and 11 official registration/institutional pages received focused inspection. The remaining papers retain `abstract_checked`, with no claim that their canonical publisher pages or full papers were separately read.
- The 34 primary web resources favor substantive concepts, worked cookbooks, SDK usage and evaluation methodology. Individual auto-generated API type pages, legal pages, corporate pages and translated duplicates were not used to inflate the count. Release and case-study statements remain provider-reported; benchmark results were not reproduced.

No source was newly granted `editorial_reviewed`. No model weights or datasets were downloaded, no model/API benchmark was run, and no remote source instructions or code were executed. All repositories remain public; verification artifacts do not contain account emails, sign-in state or credentials.

## Publication and continued maintenance

The main curated collection also gained four versioned preprints: REFLEX with Jev, Mnemon, Bongard and VideoJev. Those four source identities are counted once in the 655 additions, not again because they appear in the curated list. The curated collection now has 71 resources, including 32 direct papers and 40 BibTeX entries.

The separate twice-daily public-source workflow remains enabled. Its data-only PR and human merge/publication boundaries are unchanged. Future exploration can add another reviewed intake batch and rebuild the report; a clock change alone or a repeated source does not count as progress.

## 中文说明

本轮相对固定版本3519c15新增655项资源，包含310项正文筛查资源和345篇摘要检查论文；不是把原有3,495项重新计数。补充清单只补齐旧引用的排除依据，不修改原基线。仓库README、模型卡、数据卡、论文摘要及原始评测页面均保留来源、抓取时间和哈希；关系标签区分290项直接相关、24项邻近领域和341项背景研究。

复核剔除了尚未实现的集成、移植副本、格式/抽样数据、被误当论文的会议录像与项目记录，以及范围偏离材料。没有新增编辑审阅等级，不代表全文精读、科学同行评审或实验复现。四篇新精选论文只在655项中计数一次；持续扫描继续保留，后续新增仍须经过相同的去重、范围与证据检查。
