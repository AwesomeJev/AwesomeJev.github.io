# Source audit

**Research snapshot: 15 October 2026 · Retrieval audit: 16 October 2026, 01:30 UTC**

[Resource index](../README.md) · [Machine-readable audit](../data/editorial-audit.json) · [Source counts](../data/source-counts.json)

The collection contains **3,400 distinct source documents**, of which **3,352 passed a stated content or abstract check**. These are document counts, not independent studies, reproduced experiments, or papers read in full. The **1,929 records based on retrieved original source pages** are reported separately from the abstract-only layer.

| Verification tier | Distinct records | Meaning |
| --- | ---: | --- |
| `editorial_reviewed` | 4 | Core Decision Index sources received focused editorial inspection. |
| `content_screened` | 1,925 | A public README, card, or web page was retrieved and automatically screened for substantive, relevant content. An arXiv landing page is still an abstract page, not the full paper. |
| `abstract_checked` | 1,423 | An original abstract was screened through Hugging Face Papers or reconstructed from OpenAlex metadata. This does not establish retrieval of the original publisher page. |
| `metadata_only` | 48 | Discovery or metadata exists, but the content check did not pass. Excluded from checked-source totals. |

The input ledgers contain 3,408 records. Canonical URL and exact content-hash checks remove eight duplicates. The raw research ledger contains 897 Hugging Face abstract records and 527 OpenAlex abstract records before merging. Full downloaded source texts and reconstructed full abstracts are not published in these ledgers; they retain provenance, hashes, concise evidence and relevance notes.

## How sources entered the collection

The [Jev Decision Index](https://huggingface.co/spaces/multimodalart/jev-decision-index) is fixed at commit `5d09dd9cf226338c68fad22284c4982e6680af7d`. Its model metadata, news and methodology lead to model cards, evaluation sources and repositories. One substantial discovery path is:

```text
Decision Index news
  → hellogumbo/awesome-jev
  → each linked project's actual public README
  → recorded content hash and relevance check
```

The [community list](https://github.com/hellogumbo/awesome-jev) supplies discovery links; its descriptions alone do not count as checking the linked projects. The ecosystem collector retrieves those projects' own documents. It requires substantive readable text and explicit topic evidence; implementation pages reached on the dependency hop must discuss Jev, TypeSafe AI or typed decisions. Generic dependencies that fail this check remain in a separate exclusion ledger. No linked project code was executed.

The background layer searches calibration, selective prediction, scoring rules, constrained decoding, model programming, routing and judge reliability. It is deliberately broader than the recommended reading list. Its presence does not establish any mechanism inside Jev.

## What the 60-source audit checked

We inspected **60 selected sources**: 10 direct papers, 10 model cards, 15 application repositories, 10 dataset cards and 15 background abstracts. Papers and model cards were selected to span useful mechanisms; the other groups used a fixed sampling seed. This targeted audit is not a statistically representative precision estimate.

The review read abstracts or selected substantive README/card passages, checked topic fit and provenance, and compared response hashes. All 45 sampled ecosystem records were retrieved again with matching hashes. For the background sample, 12 original arXiv abstracts were readable; two DOI requests failed and one publisher returned an application shell. Those three were checked through their original OpenAlex-reconstructed abstracts and retain abstract-only status. **No sampled study was fully reproduced, and this audit does not imply full-paper review.** Per-source notes are in [editorial-audit.json](../data/editorial-audit.json).

The sampled applications describe concrete Jev integrations, including skill routing, command-line decisions, coding tools, Home Assistant and a Sudoku testbed. Their existence is relevant ecosystem evidence; their reliability, security and performance claims are not thereby validated.

## Findings and repairs

**Document identifiers must survive normalization.** The first merge stripped all URL queries, incorrectly merging four distinct CiteSeer works and two OpenReview works. The builder now retains nontracking identifiers such as `doi` and `id`. This corrected the unique count from 3,396 to 3,400. Genuine removals are seven exact-content duplicates and one duplicate canonical paper URL. Examples include renamed SemIf/OpenJev repositories and the renamed Decision Index Space.

**Titles need a display fallback.** Fourteen clear extraction failures selected headings such as “Citation”, “Installation” or code comments instead of an artifact title. The browser projection uses repository or dataset identifiers for these cases. Raw extraction values remain available in the ledgers. Matching titles alone do not establish duplicate projects: several unrelated repositories use names such as “Jev Router”.

**Some categories are coarse.** The Sieve-9B, Sieve-27B and crivo dataset cards in the sample are evaluation-result archives, although their raw topic says `training-dataset`. They remain useful sources, with this correction recorded. The Twitter financial sentiment card also lists a total inconsistent with the sum of its split counts; those numbers should not be reused without checking the dataset.

**Architectures and claims differ.** Tev1's card explicitly describes ordinary next-token generation of option letters. It should not be presented as a non-autoregressive implementation merely because it is Jev-inspired. Other cards make strong calibration or hallucination claims that remain publisher assertions. The selected papers distinguish probability coherence, marginal calibration, label accuracy, adversarial decision changes and closed-loop outcomes; these are different measurements.

**Background is not direct evidence.** Edge-NPU scheduling and personalized federated learning appear in the contextual sample. They belong in the broad research index, not automatically in a concise Jev reading list. Public and private Decision Index score components also remain distinct: a public leaderboard does not make its unreleased private tests reproducible.

## Publication privacy and remaining limits

The audit searched project scripts, ledgers, documentation, website and workflow files for personal filesystem paths, common real-token forms and private-key markers. It found no confirmed exposed credentials or personal machine paths. A path-pattern match in the validator is its detection expression. Collection used public unauthenticated requests; no inference keys or private user conversations were supplied, and external examples were not installed or run. Public author and project names remain as source attribution.

These checks do not certify external projects as private or secure. For example, one sampled integration explicitly sends selected conversation content to its inference provider. Inclusion is not an installation recommendation.

Exact hashes identify the retrieved bytes, not the truth of claims. Mutable pages may change, semantically equivalent mirrors may escape byte-level deduplication, and independently released model variants are separate artifacts rather than independent studies. A large checked-source count establishes breadth of discovery; the editorial shortlist and reproducible evaluation protocol provide the narrower basis for conclusions.

## 中文说明

本次合并后共有 **3,400 个来源文档**，其中 **3,352 个经过明确分级的检查**：4 个核心来源经编辑复核、1,925 个原始页面经自动正文筛查、1,423 个仅检查摘要；另有 48 个仅元数据记录，不计入已检查数量。前两类共 1,929 个，与摘要层单独统计。

我们进一步阅读了 60 条分层样本的摘要或关键正文段落，没有宣称逐篇精读全部论文，也没有运行实验。抽查发现并修复了 URL 文档 ID 被误删造成的错误去重；通用标题、结果档案分类及上游数据数量矛盾均已记录。来源的存在不等于其准确率、校准、隐私或安全承诺得到验证。

采集只访问公开资源，不使用推理密钥，不上传私人对话，不发布完整抓取正文。公开作者和项目名称作为来源归属保留；外部项目自身的数据处理行为仍需单独审查。
