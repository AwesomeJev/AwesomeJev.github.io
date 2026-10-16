# Review of the resource expansion

The expansion is measured against [commit 3519c15](https://github.com/reacher-z/Awesome-Jev/tree/3519c15d7e00686a8dbf9b1e184c68726327ab1e), not against zero. The baseline contained 3,495 unique indexed sources and 67 curated entries. The [frozen baseline](../../data/expansion-baseline-2026-10-16.json) records known identities and evidence; an [exclusion-only supplement](../../data/expansion-baseline-supplement-2026-10-16.json), derived entirely from that same commit, adds older citations and title variants initially missed by extraction. It does not change the baseline or admit new resources.

## First published intake

| Batch | Accepted into the ledgers | Evidence depth |
| --- | ---: | --- |
| GitHub projects | 130 | Public README content screening; original short relevance summaries. |
| Hugging Face artifacts | 146 | Public model, dataset, evaluation-archive or Space card screening. |
| Primary guides and evaluations | 34 | Substantive official documentation and primary evaluation/report pages. |
| Research papers | 345 | Original-abstract checks via Hugging Face or reconstruction from OpenAlex metadata. |
| **Total** | **655** | **310 content-screened resources and 345 abstract-checked papers.** |

All accepted identities are listed in the [intake](../../data/expansion-intake-2026-10-16.json). The [generated progress report](../../data/expansion-progress-2026-10-16.json) independently excludes prior URLs, repository/README aliases, arXiv DOI aliases, duplicate evidence hashes, duplicate paper titles, unreviewed additions and metadata-only records. For the first published intake, the count was 655 after the baseline supplement and alias checks. Source artifacts are not necessarily independent models, test sets or studies.

That first batch comprises 290 directly related resources, 24 adjacent resources and 341 background-method papers. The relationship labels distinguish relevance to Jev from evidence about TypeSafe's proprietary implementation. The expanded directory and its Chinese counterpart display every accepted source, its relationship, and its evidence tier directly in HTML.

## Scope and corrections

The independent [batch-review record](../../data/expansion-review-2026-10-16.json) retains exclusion reasons, primary evidence URLs, metadata corrections and review limits. This is assisted maintenance review, not a claim that every full paper or every codebase was manually examined.

- The final GitHub review removed six of 136 proposed projects: prospective-only integration, a chat-routing false positive, a fork/port counted separately, a connectivity-only example and a changed README whose remaining work included Jev. Seventeen ambiguous primary READMEs were refetched; sixteen matched their input hashes, and the changed case was excluded. Accepted descriptions were rewritten as original short summaries.
- The Hugging Face review removed two sampled/repackaged datasets from 148 proposals. Fifteen selected public cards were refetched and matched the retained hashes. Two model-namespace repositories contain experiment code and are categorized as projects, not model weights. Separate metadata annotations correct JEVal and Granite titles and identify the Tetris artifact as a simulation using measured constants. A soft-label dataset annotation avoids treating edited teacher probabilities as independently established calibration.
- The paper review removed 22 of 367 proposals: five conference recordings, one project record, six thesis records and ten scope mismatches. All input abstract hashes were checked against the retained provider snapshots; 45 targeted abstracts and 11 official registration/institutional pages received focused inspection. The remaining papers retain `abstract_checked`, with no claim that their canonical publisher pages or full papers were separately read.
- The 34 primary web resources favor substantive concepts, worked cookbooks, SDK usage and evaluation methodology. Individual auto-generated API type pages, legal pages, corporate pages and translated duplicates were not used to inflate the count. Release and case-study statements remain provider-reported; benchmark results were not reproduced.

No source was newly granted `editorial_reviewed`. No model weights or datasets were downloaded, no model/API benchmark was run, and no remote source instructions or code were executed. All repositories remain public; verification artifacts do not contain account emails, sign-in state or credentials.

## Publication and continued maintenance

The main curated collection also gained four versioned preprints: REFLEX with Jev, Mnemon, Bongard and VideoJev. Those four source identities are counted once in the 655 additions, not again because they appear in the curated list. The initial expanded curated collection had 71 resources, including 32 direct papers and 40 BibTeX entries.

The separate twice-daily public-source workflow remains enabled. Its data-only PR and human merge/publication boundaries are unchanged. Future exploration can add another reviewed intake batch and rebuild the report; a clock change alone or a repeated source does not count as progress.

## 中文说明

本轮相对固定版本3519c15新增655项资源，包含310项正文筛查资源和345篇摘要检查论文；不是把原有3,495项重新计数。补充清单只补齐旧引用的排除依据，不修改原基线。仓库README、模型卡、数据卡、论文摘要及原始评测页面均保留来源、抓取时间和哈希；关系标签区分290项直接相关、24项邻近领域和341项背景研究。

复核剔除了尚未实现的集成、移植副本、格式/抽样数据、被误当论文的会议录像与项目记录，以及范围偏离材料。没有新增编辑审阅等级，不代表全文精读、科学同行评审或实验复现。四篇新精选论文只在655项中计数一次；持续扫描继续保留，后续新增仍须经过相同的去重、范围与证据检查。


## Follow-up intake: reproducibility and robustness

A second reviewed release adds **58 distinct resources**: 32 additional projects from the reserve, 12 paper-linked reproducibility artifacts, and 14 robustness tools or result archives. One project appeared in both candidate batches; its richer robustness record was retained once, not counted twice. The cumulative expansion is **713 new sources**, including 368 content-screened artifacts and 345 abstract-checked papers. The full index contains 4,208 unique sources, with 4,161 checked at their explicit tiers and 47 metadata-only entries.

Eight selected project READMEs and six selected reproducibility cards were independently refetched; every fetched body matched the input hash. Five selected robustness cards were separately refetched and matched. File inventories were inspected for the reproducibility artifacts, without downloading dataset rows or model weights, executing software, or reproducing results.

Material limits are visible in the directory descriptions. SecurityEval distributes saved observations without original input or response text; Bongard omits part of its training recipe; Chinese-Jev model weights remain pending; some agent datasets omit question texts or raw trajectories. JEV-Contrast stores the gold answer first in both candidate arrays, so evaluation requires shuffling with label remapping. Mock demonstrations, synthetic policy-author fixtures and partially reviewed LLM-assisted annotations remain labeled as such. A neutral display title keeps a small zero-shot Laya diagnostic from reading as a universal model verdict.

Four sources already included in the first intake were promoted to the main curated collection: the Artificial Analysis Decision Index, Entagl's dated workflow evaluation, and the official SDE cascade and Structure recovery cookbooks. This brings the curated collection to 75 entries; these promotions add **zero** to the distinct expansion count. Artificial Analysis includes private questions, Entagl's private customer replays limit reproduction, and the cookbook walkthroughs are not independently reproduced experiments.

**后续批次：** 本次新增58项，跨批次重复项目只保留一次，累计净新增713项。其中368项为正文筛查、345篇为摘要检查；全文精读、模型运行和实验复现均未被声称。关键复现限制、正确选项位置泄漏、模拟或合成标签等信息已直接写入展示简介。四项既有来源提升为精选条目不增加净新增计数，精选目录现有75项。
