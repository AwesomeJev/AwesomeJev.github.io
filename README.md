<p align="center">
  <img src="assets/cover.svg" width="100%" alt="Awesome Jev — an independent field guide to typed decisions. Research, models, tools, and evidence." />
</p>

<p align="center">
  <a href="https://awesomejev.github.io"><img src="https://img.shields.io/badge/explore-the%20website-0081A7?style=flat-square&labelColor=07566B" alt="Explore the website" /></a>
  <a href="README.zh-CN.md"><img src="https://img.shields.io/badge/languages-EN%20%2F%20中文-00AFB9?style=flat-square&labelColor=07566B" alt="English and Chinese" /></a>
  <a href="docs/survey.md"><img src="https://img.shields.io/badge/read-the%20survey-FED9B7?style=flat-square&labelColor=07566B" alt="Read the survey" /></a>
  <a href="docs/source-audit.md"><img src="https://img.shields.io/endpoint?url=https%3A%2F%2Fawesomejev.github.io%2Fdata%2Fsource-badge.json&amp;style=flat-square" alt="Auditable content-screening count" /></a>
  <a href="https://github.com/AwesomeJev/AwesomeJev.github.io/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/AwesomeJev/AwesomeJev.github.io/ci.yml?branch=main&amp;style=flat-square&amp;label=checks&amp;color=00AFB9&amp;labelColor=07566B" alt="Repository checks" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-F07167?style=flat-square&labelColor=07566B" alt="MIT license" /></a>
</p>

<p align="center"><strong><a href="https://awesomejev.github.io">Explore the collection</a> · <a href="docs/survey.md">Read the survey</a> · <a href="README.zh-CN.md">中文</a> · <a href="CONTRIBUTING.md">Contribute</a></strong></p>

Jev makes a useful question concrete: **what changes when a model returns a decision your code can use directly?** Awesome Jev follows that question through research, developer tools, open experiments, and inspectable evaluations.

An independent community project by [AwesomeJev](https://github.com/AwesomeJev). Not affiliated with TypeSafe AI. Curated **2026-10-15**; model capabilities, aliases, prices, and leaderboard results are dated observations.

## Start here

| If you want to… | Begin with… |
| :--- | :--- |
| Understand the idea | [Introducing System One Models & Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev) → [our survey](docs/survey.md) |
| Explore the open ecosystem | **[Jev Decision Index](https://huggingface.co/spaces/multimodalart/jev-decision-index)** → [news and reproductions](https://multimodalart-jev-decision-index.static.hf.space/news.html) |
| Build a first integration | [Official quick start](https://docs.typesafe.ai/introduction/quickstart) → [Python SDK](https://github.com/typesafe-ai/typesafe-sdk-python) |
| Examine the evidence | [Direct research](#direct-research) → [benchmarks](#benchmarks-and-evaluation) → [evaluation protocol](docs/survey.md) |
| Trace the foundations | [Related research](#related-research) · [BibTeX](references.bib) |

**Browse:** [Model and interface](#model-and-interface) · [Direct research](#direct-research) · [Benchmarks](#benchmarks-and-evaluation) · [Tools](#developer-tools) · [Recipes](#practical-recipes) · [Foundations](#related-research) · [Source audit](#source-audit)

## Model and interface

TypeSafe describes Jev as a **System One model**: provide state and typed questions; receive bounded decisions and probabilities. The core interface exposes three primitives. [Official introduction](https://docs.typesafe.ai/introduction)

| Primitive | Useful for | Output |
| :--- | :--- | :--- |
| [Choice](https://docs.typesafe.ai/primitives/choice) | Routing and classification | A choice, option probabilities, and confidence; up to 255 options |
| [Score](https://docs.typesafe.ai/primitives/score) | Rubric judgments | A probability-weighted score over described levels, distribution, and confidence |
| [Noul](https://docs.typesafe.ai/primitives/noul) | A proposition's truth probability | A number in [0, 1]; no separate confidence field |

Schema validity, semantic correctness, and probability calibration are different properties. In particular, the API's [confidence](https://docs.typesafe.ai/confidence) is a statistic derived from the output distribution; it is not automatically a measured probability of correctness.

**Version note.** On 2026-10-15, `jev-latest` points to `jev-1.13.0`; `jev-preview` points to `jev-1.14.0`. Pin an explicit model ID when comparing results. Experimental [image inputs](https://docs.typesafe.ai/images) and the 1.14 [Box primitive](https://docs.typesafe.ai/primitives/box) require opt-in; keep them separate from default text capabilities. [Models](https://docs.typesafe.ai/models) · [Jev 1.13 limitations](https://docs.typesafe.ai/model-jaggedness/jev-1.13)

## Direct research

All entries below are **preprints**, linked to the versions reviewed. Their findings are author-reported; inclusion does not imply independent reproduction by this project.

- **[Evaluating and Benchmarking the System One Model Jev](https://arxiv.org/abs/2609.37647v1)** — Deußer, Sparrenberg & Sifa, Sep 2026. Broad classification and decision evaluation across 37 datasets. [Code](https://github.com/AppliedMachineLearning-Lab/jev-benchmarking)
- **[Typed Decision Models: An Early Evidence Audit and Evaluation Checklist](https://arxiv.org/abs/2609.32160v1)** — Tang & Zheng, Sep 2026. A map of early evidence and evaluation design; use it to discover primary studies.
- **[JEV-as-a-Judge: Accept When Confident, Escalate When Unsure](https://arxiv.org/abs/2609.26550v5)** — Li et al., revised Oct 2026. Confidence-gated judging and escalation.
- **[Decision Models vs. LLMs as Rubric Judges: Cheaper, Faster, and Wrong in the Same Places](https://arxiv.org/abs/2609.29769v3)** — Rao & Callison-Burch, revised Oct 2026. Rubric evaluation, correlated errors, and limits to cascading gains.
- **[JEV versus LLMs: Accuracy, Cost and Calibration on Seven Political Science Replications](https://arxiv.org/abs/2610.06625v2)** — Denney & DiGiuseppe, Oct 2026. Domain-specific replications and cost comparisons.
- **[Same Attack, Different Judge](https://arxiv.org/abs/2610.17820v1)** — Li et al., Oct 2026. Controlled adversarial comparison of Jev, LLM judges, and safety classifiers.

Read the [evidence comparison and open questions](docs/survey.md), or import [references.bib](references.bib).

<details>
<summary>More direct studies</summary>

Additional **arXiv preprints**, with reviewed versions pinned; findings remain author-reported.

- [this-that-model-1.0](https://arxiv.org/abs/2609.23886v1) · 2026-09-20 — Open typed-decision architecture with local inference and explicit probability readout.
- [Jev-Mem](https://arxiv.org/abs/2609.23986v1) · 2026-09-21 — Decision-based control for memory construction, retrieval, and agent reasoning.
- [PixelJev](https://arxiv.org/abs/2609.29283v1) · 2026-09-24 — Visual candidate scoring, adaptation, and calibration evaluated separately.
- [JevAdvBench](https://arxiv.org/abs/2609.31142v1) · 2026-09-25 — Adversarial request edits compared against clean decisions and repeated-call variation.
- [Beyond Calibration](https://arxiv.org/abs/2609.33209v1) · 2026-09-27 — Tests logical consistency across related probability questions.
- [System One Models for Agent Security Decisions](https://arxiv.org/abs/2609.33401v3) · revised 2026-10-03 — Studies confident security errors and selective automation under asymmetric risks.
- [Sys1Cal-v1](https://arxiv.org/abs/2609.35342v1) · 2026-09-28 — Constructed probability targets probe calibration across Jev primitives.
- [Chinese-Jev](https://arxiv.org/abs/2609.36965v1) · 2026-09-29 — Chinese decision training and evaluation across general and specialized domains.
- [Jeva](https://arxiv.org/abs/2610.18773v1) · 2026-10-13 — Null handling, option permutation, variable candidate sets, and reusable option representations.
- [System1-Arena](https://arxiv.org/abs/2610.21244v1) · 2026-10-15 — Matched decision requests and closed-loop environments for comparing decision and reasoning models.

</details>

## Benchmarks and evaluation

### Jev Decision Index

**[Decision Index](https://huggingface.co/spaces/multimodalart/jev-decision-index)** is a central discovery source for Jev-inspired models, open experiments, and comparative results. Its [methodology](https://multimodalart-jev-decision-index.static.hf.space/methodology.html), [news](https://multimodalart-jev-decision-index.static.hf.space/news.html), and [source files](https://huggingface.co/spaces/multimodalart/jev-decision-index/tree/main) are worth reading together.

Treat an open reproduction as its own implementation, not as released TypeSafe weights. The index's full score includes private tests; public availability of a leaderboard does not make its entire evaluation reproducible.

### Evaluation implementations

| Resource | Evidence and scope |
| :--- | :--- |
| [TypeSafe WorkflowEvals](https://github.com/typesafe-ai/WorkflowEvals) | Official runner, workflows, published runs, and scoring code. [Evaluation site](https://evals.typesafe.ai/) · [Datasets](https://huggingface.co/collections/typesafeAI/workflowevals) |
| [jev-benchmarking](https://github.com/AppliedMachineLearning-Lab/jev-benchmarking) | Harness accompanying the 37-dataset study above. |
| [PavelRavvich / jev-bench](https://github.com/PavelRavvich/jev-bench) | Public classification tasks, raw predictions, calibration, latency, cost, and cascade analysis. Small samples and differing confidence interfaces matter. |
| [AY Automate benchmark](https://www.ayautomate.com/blog/jev-vs-llm-benchmark) | Routing and injection detection; links code and raw calls. Read its sampling and reasoning settings alongside the results. |

Official WorkflowEvals uses a model-consensus reference. Agreement with that reference and accuracy against human labels answer different questions. Compare the same model versions, workload, access route, probability interface, and reasoning settings before interpreting a speed or cost ratio. [Evaluation methodology](https://evals.typesafe.ai/)

## Developer tools

### Open model experiments

Independent implementations help test design choices. Read each model card for its license, training data, evaluation setup, and access conditions; these are not TypeSafe's model weights.

| Model | Publisher | Declared license |
| :--- | :--- | :--- |
| [Laya](https://huggingface.co/convaiinnovations/laya) | Convai Innovations | Apache-2.0 |
| [Kev-4B](https://huggingface.co/jaredpalmer/kev-4b) | Jared Palmer | Apache-2.0 |
| [Bespoke Nimble 9B v3](https://huggingface.co/bespokelabs/Bespoke-Nimble-9B-v3) | Bespoke Labs | **CC BY-NC 4.0 — noncommercial** |
| [Intern-Decision-4B](https://huggingface.co/internlm/Intern-Decision-4B) | InternLM | Apache-2.0 |
| [Perplexity Decider v1.1 27B](https://huggingface.co/perplexity-ai/pplx-decider-v1.1-27b) | Perplexity | Apache-2.0; see access notes |
| [GLiNER2.5-Decide](https://huggingface.co/fastino/GLiNER2.5-Decide) | Fastino | Apache-2.0 |
| [d3](https://huggingface.co/vllm-sr/d3) | vLLM Semantic Router | Apache-2.0 |
| [Clef](https://huggingface.co/Cloudflare/clef) | Cloudflare | Apache-2.0 |

### SDKs and integrations

| Project | Purpose |
| :--- | :--- |
| [TypeSafe Python SDK](https://github.com/typesafe-ai/typesafe-sdk-python) | Official synchronous and asynchronous Python client. |
| [TypeSafe TypeScript SDK](https://github.com/typesafe-ai/typesafe-sdk-js) | Official JavaScript / TypeScript client. |
| [System One Adapter](https://github.com/typesafe-ai/system-one-adapter-python) | Put LLM baselines behind a comparable typed-question interface. |
| [Public examples](https://github.com/typesafe-ai/typesafe-public-examples) | Official example and cookbook code. |
| [Agent skills](https://github.com/typesafe-ai/skills) | Integration guidance for coding agents. |
| [n8n nodes](https://github.com/typesafe-ai/n8n-nodes-typesafe-ai) | TypeSafe integration for n8n workflows. |

### A first typed decision

Install `typesafe-sdk` and set `TYPESAFE_API_KEY` in your environment. This example follows the official SDK interface and pins the model. It requires API access and incurs usage charges; no live API call was made while preparing this collection.

```python
from typesafe_sdk import Choice, TypeSafeClient

with TypeSafeClient() as client:
    result = client.system_one(
        model="jev-1.13.0",
        state={"ticket": "I was charged twice. Please fix this."},
        questions={
            "category": Choice(
                instructions="What is this ticket about?",
                criteria={
                    "billing": "Charges, payments, or refunds",
                    "technical": "Bugs or technical failures",
                    "other": "None of the above",
                },
            )
        },
    )

answer = result.choices["category"]
print(answer.choice, answer.probabilities, answer.confidence)
```

For current setup and response types, follow the [SDK documentation](https://github.com/typesafe-ai/typesafe-sdk-python).

## Practical recipes

| Task | Starting point |
| :--- | :--- |
| Route uncertain cases | [Confidence-gated routing](https://docs.typesafe.ai/patterns/confidence-routing) |
| Judge several dimensions | [Composite scoring](https://docs.typesafe.ai/patterns/composite-scoring) |
| Check generated answers | [LLM guardrails](https://docs.typesafe.ai/cookbooks/llm_guardrails) · [Citation checking](https://docs.typesafe.ai/cookbooks/citation_check) |
| Filter retrieved passages | [RAG passage classification](https://docs.typesafe.ai/cookbooks/classifying_rag_passages) |
| Navigate a large taxonomy | [Hierarchical classification](https://docs.typesafe.ai/cookbooks/hierarchical_classification) |
| Select an extracted value | [Pre-parsed value extraction](https://docs.typesafe.ai/cookbooks/pre_parsed_value_extraction_cookbook) · [Dates](https://docs.typesafe.ai/cookbooks/date_extraction_cookbook) |

These are provider-authored recipes. Validate thresholds on held-out data and keep arithmetic, parsing, and business policy in code where possible.

## Related research

These works supply context and baselines. They do **not** establish Jev's architecture, training objective, or sampler implementation.

| Thread | Selected reading |
| :--- | :--- |
| Probability scoring | Gneiting & Raftery, **[Strictly Proper Scoring Rules, Prediction, and Estimation](https://doi.org/10.1198/016214506000001437)**, 2007 |
| Calibration | Guo et al., **[On Calibration of Modern Neural Networks](https://proceedings.mlr.press/v70/guo17a.html)**, 2017 |
| Selective prediction | Geifman & El-Yaniv, **[SelectiveNet](https://proceedings.mlr.press/v97/geifman19a.html)**, 2019 |
| LM self-assessment | Kadavath et al., **[Language Models (Mostly) Know What They Know](https://arxiv.org/abs/2207.05221)**, 2022 |
| Constrained LM programs | Beurer-Kellner et al., **[Prompting Is Programming](https://www.sri.inf.ethz.ch/publications/beurerkellner2023prompting)**, PLDI 2023 |
| Structured generation | Dong et al., **[XGrammar](https://arxiv.org/abs/2411.15100)**, 2024 · [Code](https://github.com/mlc-ai/xgrammar) |
| Composable pipelines | Khattab et al., **[DSPy](https://arxiv.org/abs/2310.03714)**, 2023 |
| Efficient execution | Zheng et al., **[SGLang](https://papers.nips.cc/paper_files/paper/2024/file/724be4472168f31ba1c9ac630f15dec8-Paper-Conference.pdf)**, NeurIPS 2024 · [Code](https://github.com/sgl-project/sglang) |

## Source audit

The concise collection above and the larger research corpus serve different purposes. The collection is editorially selected; corpus entries retain retrieval provenance, relevance signals, and verification depth. **Content screening is not full-paper review or experimental reproduction.** Failed fetches and metadata-only records are kept distinguishable from checked content.

See [the source-audit methodology](docs/source-audit.md), [source data](data/), and the searchable corpus on [the website](https://awesomejev.github.io/#corpus). Discovery does not imply endorsement; associated models retain their own licenses.

## Contribute

Good additions explain **what a resource contributes, which version was checked, and what evidence supports it**. Read [CONTRIBUTING.md](CONTRIBUTING.md); corrections and negative results are welcome.

Original project content and code are [MIT licensed](LICENSE). Linked publications, datasets, model weights, and third-party assets retain their respective licenses.
