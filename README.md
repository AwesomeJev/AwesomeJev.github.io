# Awesome Jev

[![Website](https://img.shields.io/badge/website-awesomejev.github.io-087E8B?style=flat-square&labelColor=0B3954)](https://awesomejev.github.io/) [![Checks](https://img.shields.io/github/actions/workflow/status/reacher-z/Awesome-Jev/ci.yml?branch=main&style=flat-square&label=checks&color=087E8B&labelColor=0B3954)](https://github.com/reacher-z/Awesome-Jev/actions/workflows/ci.yml) [![License](https://img.shields.io/badge/license-MIT-C81D25?style=flat-square&labelColor=0B3954)](LICENSE)

A curated list of **Jev and typed decision model** papers, models, datasets, evaluation tools, and practical guides.

**[Main repository](https://github.com/reacher-z/Awesome-Jev)** · [Website](https://awesomejev.github.io/) · [中文](README.zh-CN.md) · [Survey](docs/survey.md) · [BibTeX](references.bib) · [Contribute](CONTRIBUTING.md)

Independent community project; not affiliated with TypeSafe AI. Last curated: **2026-10-15**. The website is published from [AwesomeJev.github.io](https://github.com/AwesomeJev/AwesomeJev.github.io).

## Contents

- [Overview and official resources](#overview-and-official-resources)
- [Papers](#papers)
  - [Evaluation and benchmarking](#evaluation-and-benchmarking)
  - [Probability calibration and coherence](#probability-calibration-and-coherence)
  - [Judging and selective automation](#judging-and-selective-automation)
  - [Robustness and security](#robustness-and-security)
  - [Architectures, memory, and multimodality](#architectures-memory-and-multimodality)
- [Models](#models)
- [Benchmarks and evaluation tools](#benchmarks-and-evaluation-tools)
- [Datasets](#datasets)
- [SDKs and integrations](#sdks-and-integrations)
- [Practical guides](#practical-guides)
- [Foundations and related research](#foundations-and-related-research)
- [Quick start](#quick-start)
- [Source audit](#source-audit)
- [Contributing](#contributing)
- [License](#license)

## Overview and official resources

TypeSafe's Jev accepts a state and typed questions, returning decisions and probabilities for application code. Schema validity, semantic correctness, and probability calibration are separate properties.

- [Introducing System One Models & Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev) — launch article and provider claims.
- [Documentation](https://docs.typesafe.ai/introduction) · [API](https://docs.typesafe.ai/api) · [Models and versions](https://docs.typesafe.ai/models).
- [Choice](https://docs.typesafe.ai/primitives/choice) — choose from up to 255 options; returns a distribution and confidence.
- [Score](https://docs.typesafe.ai/primitives/score) — a probability-weighted position on descriptive, ordered levels.
- [Noul](https://docs.typesafe.ai/primitives/noul) — the probability of yes; no separate confidence field.
- [Confidence](https://docs.typesafe.ai/confidence) · [Jev 1.13 limitations](https://docs.typesafe.ai/model-jaggedness/jev-1.13).
- [Experimental images](https://docs.typesafe.ai/images) · [Box](https://docs.typesafe.ai/primitives/box) — opt-in capabilities; Box requires Jev 1.14.

On **2026-10-15**, `jev-latest` points to `jev-1.13.0` and `jev-preview` to `jev-1.14.0`. Pin the version for evaluation. See the [survey](docs/survey.md) for the conceptual distinctions and evaluation protocol.

## Papers

All 16 direct studies below are **arXiv preprints**. Dates identify the linked, reviewed version, not necessarily the first submission. Results are author-reported; this project has not reproduced their experiments. Titles that contain speed or cost claims retain the authors' wording. [Bibliography](references.bib) · [Evidence comparison](docs/survey.md)

### Evaluation and benchmarking

- **[System1-Arena: Which Decisions Can Be Left to System 1?](https://arxiv.org/abs/2610.21244v1)** — Chen et al. *2026-10-15, arXiv v1*. Matched requests and closed-loop tasks for decision and reasoning models.
- **[JEV versus LLMs: Accuracy, Cost and Calibration on Seven Political Science Replications](https://arxiv.org/abs/2610.06625v2)** — Denney & DiGiuseppe. *2026-10-06, arXiv v2*. Seven domain-specific replications; accuracy, cost, and calibration.
- **[Evaluating and Benchmarking the System One Model Jev](https://arxiv.org/abs/2609.37647v1)** — Deußer, Sparrenberg & Sifa. *2026-09-29, arXiv v1*. Classification and decision evaluation across 37 datasets. [Code](https://github.com/AppliedMachineLearning-Lab/jev-benchmarking).
- **[Typed Decision Models: An Early Evidence Audit and Evaluation Checklist](https://arxiv.org/abs/2609.32160v1)** — Tang & Zheng. *2026-09-26, arXiv v1*. Evidence mapping and an evaluation checklist for typed decisions.

### Probability calibration and coherence

- **[Jev thinks “I don’t know”, but doesn’t say it: Introducing Sys1Cal-v1 Dataset for Probability Calibration](https://arxiv.org/abs/2609.35342v1)** — Porcedda. *2026-09-28, arXiv v1*. Controlled probability targets for testing calibration.
- **[Beyond Calibration: Do a Typed-Decision Model’s Probabilities Obey the Probability Axioms?](https://arxiv.org/abs/2609.33209v1)** — Li, He & Li. *2026-09-27, arXiv v1*. Logical coherence between related probability questions.

### Judging and selective automation

- **[Decision Models vs. LLMs as Rubric Judges: Cheaper, Faster, and Wrong in the Same Places](https://arxiv.org/abs/2609.29769v3)** — Rao & Callison-Burch. *2026-10-13, arXiv v3*. Rubric judging, correlated errors, and limits to cascade gains.
- **[JEV-as-a-Judge: Accept When Confident, Escalate When Unsure](https://arxiv.org/abs/2609.26550v5)** — Li, Miao, Krishnan & Padman. *2026-10-09, arXiv v5*. Confidence-gated escalation from Jev to a reasoning judge.

### Robustness and security

- **[Same Attack, Different Judge: A First Controlled Adversarial Comparison of Jev, LLM Judges, and Purpose-Built Safety Classifiers](https://arxiv.org/abs/2610.17820v1)** — Li, Huang, Zhang & Liu. *2026-10-13, arXiv v1*. Controlled attacks against decision models and safety classifiers.
- **[Evaluating System One Models for Agent Security Decisions: Reliability, Calibration, and Selective Automation](https://arxiv.org/abs/2609.33401v3)** — Liu. *2026-10-03, arXiv v3*. Confident security errors and selective automation under asymmetric risks.
- **[JevAdvBench: A Benchmark and Black-Box Attacks for Reinforcement Learning for Calibrated Decisions Models](https://arxiv.org/abs/2609.31142v1)** — Hu et al. *2026-09-25, arXiv v1*. Adversarial edits compared with clean inputs and repeated-call variation.

### Architectures, memory, and multimodality

- **[Jeva: System One Models from First Principles](https://arxiv.org/abs/2610.18773v1)** — Li & Wang. *2026-10-13, arXiv v1*. Null handling, option permutation, variable candidate sets, and caching.
- **[Chinese-Jev: Bringing System One Model to Chinese-Language Tasks](https://arxiv.org/abs/2609.36965v1)** — Wang et al. *2026-09-29, arXiv v1*. Chinese decision-model training and domain-specific evaluation.
- **[From Text Decisions to Pixels: An Study of Jev-Style Visual Choice Model](https://arxiv.org/abs/2609.29283v1)** — Zhou, Yang & Zhao. *2026-09-24, arXiv v1*. Visual choice models; adaptation and calibration evaluated separately.
- **[Jev-Mem: System-One-Controlled Agentic Memory for Efficient AI Agents](https://arxiv.org/abs/2609.23986v1)** — Jiang, Li & Li. *2026-09-21, arXiv v1*. Decision-based control of agent memory construction and retrieval.
- **[this-that-model-1.0: A typed decision model that decides in 30 ms, for a millionth of a cent](https://arxiv.org/abs/2609.23886v1)** — Cheng, Dai & Sun. *2026-09-20, arXiv v1*. A typed-decision architecture with hidden-state probability readout.

## Models

These are independent implementations, not released TypeSafe weights. Licenses below are those declared by the linked model cards. API compatibility does not establish equivalent behavior or accuracy.

| Model | Publisher | Declared license | Scope |
| :--- | :--- | :--- | :--- |
| [Laya](https://huggingface.co/convaiinnovations/laya) | Convai Innovations | Apache-2.0 | Encoder-based English, multilingual, and workflow-specific checkpoints. |
| [Kev-4B](https://huggingface.co/jaredpalmer/kev-4b) | Jared Palmer | Apache-2.0 | Qwen3.5-4B-Base LoRA adapter and pointer head. |
| [Bespoke Nimble 9B v3](https://huggingface.co/bespokelabs/Bespoke-Nimble-9B-v3) | Bespoke Labs | **CC BY-NC 4.0** | Qwen3.5-9B adapter; noncommercial license. |
| [Intern-Decision-4B](https://huggingface.co/internlm/Intern-Decision-4B) | InternLM | Apache-2.0 | Decision-tuned Qwen checkpoint with image input support. |
| [Perplexity Decider v1.1 27B](https://huggingface.co/perplexity-ai/pplx-decider-v1.1-27b) | Perplexity | Apache-2.0 | Separate decision readout; check attention-mode and access notes. |
| [GLiNER2.5-Decide](https://huggingface.co/fastino/GLiNER2.5-Decide) | Fastino | Apache-2.0 | English classifier with runtime label sets and multi-label outputs. |
| [d3](https://huggingface.co/vllm-sr/d3) | vLLM Semantic Router | Apache-2.0 | Text, image, and video decisions. |
| [Clef](https://huggingface.co/Cloudflare/clef) | Cloudflare | Apache-2.0 | Multimodal decision model with a joint schema head. |

## Benchmarks and evaluation tools

- **[Jev Decision Index](https://huggingface.co/spaces/multimodalart/jev-decision-index)** — community index of models and comparative evaluations. [Methodology](https://multimodalart-jev-decision-index.static.hf.space/methodology.html) · [News](https://multimodalart-jev-decision-index.static.hf.space/news.html) · [Source](https://huggingface.co/spaces/multimodalart/jev-decision-index/tree/main). The full score includes private tests; the public leaderboard is not a complete reproducibility package.
- **[TypeSafe WorkflowEvals](https://github.com/typesafe-ai/WorkflowEvals)** — official workflow definitions, runner, recorded results, and scoring. [Interactive results](https://evals.typesafe.ai/) · [Dataset collection](https://huggingface.co/collections/typesafeAI/workflowevals). Its reference is model consensus, not independently established human ground truth.
- **[jev-benchmarking](https://github.com/AppliedMachineLearning-Lab/jev-benchmarking)** — code accompanying Deußer et al.'s 37-dataset study. [Paper](https://arxiv.org/abs/2609.37647v1).
- **[PavelRavvich / jev-bench](https://github.com/PavelRavvich/jev-bench)** — classification, raw predictions, calibration, latency, cost, and cascades. Check sampling and confidence definitions before comparing results.
- **[AY Automate benchmark](https://www.ayautomate.com/blog/jev-vs-llm-benchmark)** — routing and injection-detection experiments with linked code and raw calls; reported by the benchmark author.

For a comparison, record the model version, dataset split, probability interface, reasoning settings, access route, latency distribution, and failure handling. See the [evaluation protocol](docs/survey.md).

## Datasets

The four TypeSafe datasets contain workflow cases, model-generated references, and published runs. Counts below are case counts in the inspected snapshot, not numbers of independent human labels. The other entries serve different roles: a training mixture and an evaluation-run archive. Inspect provenance before treating either as a test benchmark.

| Dataset | Publisher | Contents |
| :--- | :--- | :--- |
| [Invoice Processing](https://huggingface.co/datasets/typesafeAI/evalsafe-invoice-processing) | TypeSafe | 150 cases; invoice actions, question-level references, and recorded runs. |
| [Customer Service](https://huggingface.co/datasets/typesafeAI/evalsafe-customer-service) | TypeSafe | 204 cases; customer-service routing and actions. |
| [Agent Trace Observability](https://huggingface.co/datasets/typesafeAI/evalsafe-agent-trace-observability) | TypeSafe | 111 cases; review decisions over agent traces. |
| [Security Incidents](https://huggingface.co/datasets/typesafeAI/evalsafe-security-incidents) | TypeSafe | 240 cases; security-alert triage and containment. |
| [Bekko System One dataset v0](https://huggingface.co/datasets/hotchpotch/bekko-system-one-dataset-v0) | hotchpotch | Decision-model training mixture; inspect component provenance and split policy. |
| [Bespoke Nimble v3 Decision Index archive](https://huggingface.co/datasets/bespokelabs/bespoke-nimble-9b-v3-decision-index) | Bespoke Labs | Published evaluation-run archive and inference materials; not an independent test set. |

## SDKs and integrations

| Project | Maintainer | Purpose |
| :--- | :--- | :--- |
| [Python SDK](https://github.com/typesafe-ai/typesafe-sdk-python) | TypeSafe | Official sync and async Python client. |
| [JavaScript / TypeScript SDK](https://github.com/typesafe-ai/typesafe-sdk-js) | TypeSafe | Official client with inferred answer types. |
| [System One Adapter](https://github.com/typesafe-ai/system-one-adapter-python) | TypeSafe | Evaluate LLM baselines through a comparable typed-question interface. |
| [Public examples](https://github.com/typesafe-ai/typesafe-public-examples) | TypeSafe | Documentation, demo, and cookbook source code. |
| [Agent skills](https://github.com/typesafe-ai/skills) | TypeSafe | Integration guidance for coding agents. |
| [n8n nodes](https://github.com/typesafe-ai/n8n-nodes-typesafe-ai) | TypeSafe | Nodes for n8n workflows. |

## Practical guides

Provider-authored recipes; validate thresholds on held-out examples from your own workload.

- [Confidence-gated routing](https://docs.typesafe.ai/patterns/confidence-routing) — route uncertain cases to another system or a person.
- [Composite scoring](https://docs.typesafe.ai/patterns/composite-scoring) — combine separate judgments with weights controlled by code.
- [LLM guardrails](https://docs.typesafe.ai/cookbooks/llm_guardrails) · [Citation checking](https://docs.typesafe.ai/cookbooks/citation_check) — inspect generated content against stated criteria and sources.
- [RAG passage classification](https://docs.typesafe.ai/cookbooks/classifying_rag_passages) — filter retrieved context.
- [Hierarchical classification](https://docs.typesafe.ai/cookbooks/hierarchical_classification) — navigate large label trees.
- [Pre-parsed value extraction](https://docs.typesafe.ai/cookbooks/pre_parsed_value_extraction_cookbook) · [Date extraction](https://docs.typesafe.ai/cookbooks/date_extraction_cookbook) — choose bounded candidates; normalize and calculate in code.

## Foundations and related research

Background literature and comparison methods. These works do **not** establish Jev's internal architecture, training objective, or sampler implementation.

| Topic | Reference | Links |
| :--- | :--- | :--- |
| Proper scoring rules | Gneiting & Raftery, *Strictly Proper Scoring Rules, Prediction, and Estimation*. JASA, 2007. | [Paper](https://sites.stat.washington.edu/people/raftery/Research/PDF/Gneiting2007jasa.pdf) · [DOI](https://doi.org/10.1198/016214506000001437) |
| Calibration | Guo et al., *On Calibration of Modern Neural Networks*. ICML, 2017. | [Paper](https://proceedings.mlr.press/v70/guo17a.html) |
| Selective prediction | Geifman & El-Yaniv, *SelectiveNet*. ICML, 2019. | [Paper](https://proceedings.mlr.press/v97/geifman19a.html) |
| LM self-assessment | Kadavath et al., *Language Models (Mostly) Know What They Know*. 2022. | [Paper](https://arxiv.org/abs/2207.05221) |
| Constrained LM programs | Beurer-Kellner et al., *Prompting Is Programming: A Query Language for Large Language Models*. PLDI, 2023. | [Paper](https://www.sri.inf.ethz.ch/publications/beurerkellner2023prompting) |
| Structured generation | Dong et al., *XGrammar*. 2024. | [Paper](https://arxiv.org/abs/2411.15100) · [Code](https://github.com/mlc-ai/xgrammar) |
| Composable pipelines | Khattab et al., *DSPy*. 2023. | [Paper](https://arxiv.org/abs/2310.03714) |
| Efficient execution | Zheng et al., *SGLang*. NeurIPS, 2024. | [Paper](https://papers.nips.cc/paper_files/paper/2024/file/724be4472168f31ba1c9ac630f15dec8-Paper-Conference.pdf) · [Code](https://github.com/sgl-project/sglang) |

All 24 selected papers are included in [references.bib](references.bib).

## Quick start

```sh
pip install typesafe-sdk
```

Set `TYPESAFE_API_KEY`, then follow our [minimal Python example](docs/quickstart.md) or the [official quick start](https://docs.typesafe.ai/introduction/quickstart). The example pins `jev-1.13.0` and shows Choice outputs; it was checked against the SDK interface, not executed against the paid API.

## Source audit

[![Checked source corpus](https://img.shields.io/endpoint?url=https%3A%2F%2Fawesomejev.github.io%2Fdata%2Fsource-badge.json&style=flat-square)](docs/source-audit.md)

The selected resources above and the larger [searchable source corpus](https://awesomejev.github.io/#corpus) serve different purposes. Corpus entries retain discovery provenance and distinguish editorial review, automated content screening, abstract checks, and metadata-only records. **Screening is not full-paper review or experimental reproduction.**

- [Methodology and counts](docs/source-audit.md)
- [Source ledgers](data/) · [Editorial audit sample](data/editorial-audit.json)
- [Maintenance workflow](docs/maintenance.md)

## Contributing

Maintained by [reacher-z](https://github.com/reacher-z).

Submit additions and corrections to **[reacher-z/Awesome-Jev](https://github.com/reacher-z/Awesome-Jev)**. Include the primary source, author or publisher, date/version, research topic, and what was actually checked. Code, data, limitations, and negative results are useful additions. See [CONTRIBUTING.md](CONTRIBUTING.md).

Organization and entry conventions were informed by [awesome-RLHF](https://github.com/opendilab/awesome-RLHF); this collection has its own scope and source-review policy.

## License

Original project content and code are [MIT licensed](LICENSE). Linked papers, datasets, models, and third-party assets retain their respective licenses.
