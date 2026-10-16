# Jev and typed decision models

**A compact research survey · Evidence snapshot: 15 October 2026**

[English](survey.md) · [简体中文](survey.zh-CN.md) · [Resource index](../README.md) · [BibTeX](../references.bib)

Jev makes an interesting research question concrete: what changes when a model returns a decision that software can consume directly? This survey separates the interface, the evidence about a hosted model, and the systems that use its answers. It is a curated starting point, not an exhaustive review. We have checked sources, but have not reproduced their experiments.

## 1. The decision interface

TypeSafe introduced Jev on **15 September 2026**, describing a model architecture, parallel sampler, and Reinforcement Learning for Calibrated Decisions (RLCD). These are vendor descriptions; the launch article does not disclose enough to reconstruct the training method or architecture. “System One” is the product’s framing, not a demonstrated correspondence with human cognition. [Launch article](https://typesafe.ai/blog/introducing-system-one-models-and-jev)

A request pairs shared state with questions and caller-defined criteria. **Choice** returns an option and its distribution; **Score** returns an assessment over ordered rubric levels; **Noul** returns a yes-probability. The surrounding program determines how those answers affect routing, review, or execution. This puts the decision contract, its alternatives, and uncertainty directly in the application. [Question primitives](https://docs.typesafe.ai/primitives)

Version boundaries matter. On this snapshot, `jev-latest` resolves to stable **1.13.0**; `jev-preview` resolves to **1.14.0**, released **14 October**. Log the returned model ID and pin versions for comparisons. The studies below mainly concern 1.13; they cannot establish 1.14 performance. [Models](https://docs.typesafe.ai/models)

The current interface is also broader than the original text-oriented evaluations: images require explicit experimental opt-in, and **Box** localization requires 1.14. These capabilities need their own evidence. [Images](https://docs.typesafe.ai/images) · [Box](https://docs.typesafe.ai/primitives/box)

## 2. Reading the evidence

Different sources answer different questions:

| Evidence | What it can establish | What remains separate |
| --- | --- | --- |
| Official documentation | Supported contracts, version names, operational limits | Measured reliability on a new workload |
| Vendor evaluations | Performance under the vendor’s published design | Generalization beyond its references and tasks |
| External empirical papers | Observations under specified prompts, data, and comparators | Our own reproduction; causal explanations of internals |
| Surveys and open implementations | Research connections and inspectable alternative designs | Proof that Jev uses the same mechanisms |

Official **WorkflowEvals** now has public [workflow code](https://github.com/typesafe-ai/WorkflowEvals) and a [dataset collection](https://huggingface.co/collections/typesafeAI/workflowevals). Its references use model consensus, so agreement with them measures agreement with that reference procedure. Human-label accuracy is a different claim. Public artifacts make inspection possible; availability alone does not certify a result. [Evaluation design](https://typesafe.ai/blog/introducing-system-one-models-and-jev)

The community [**Jev Decision Index**](https://huggingface.co/spaces/multimodalart/jev-decision-index) is a central discovery resource for benchmarks and independent Jev-inspired implementations, not TypeSafe weights. Edition **0.3.2**, inspected at commit `5d09dd9`, combines public and unreleased private tests. Its full ranking therefore cannot be independently recomputed from public material alone. [Versioned methodology](https://huggingface.co/spaces/multimodalart/jev-decision-index/blob/5d09dd9cf226338c68fad22284c4982e6680af7d/data/methodology.json)

The six selected works below are **arXiv preprints**. Dates distinguish first publication from the version reviewed. Findings are author-reported; the audit paper maps evidence rather than adding another empirical replication.

| Work and reviewed version | Method, finding, and limitation |
| --- | --- |
| [Deußer et al. — broad benchmark](https://arxiv.org/abs/2609.37647v1) · 29 Sep · v1 | Tests 37 datasets against label-probability baselines; reports useful Choice calibration and task-dependent Noul thresholds. Single prompts, disabled baseline reasoning, and possible contamination limit interpretation. |
| [Tang & Zheng — evidence audit](https://arxiv.org/abs/2609.32160v1) · 26 Sep · v1 | Audits 28 early papers and proposes an evaluation checklist. Evidence does not isolate a general accuracy gain from typed readout; the corpus is an early snapshot. |
| [Li et al. — adversarial comparison](https://arxiv.org/abs/2610.17820v1) · 13 Oct · v1 | Compares judges under matched attacks across four tasks; robustness varies by task. English, single-turn experiments and one phishing corpus constrain generalization. |
| [Denney & DiGiuseppe — political science](https://arxiv.org/abs/2610.06625v2) · 5 Oct → 6 Oct · v2 | Replicates seven studies; accuracy is often competitive, while calibration and cost advantages depend on baselines. Historical comparisons and reconstructed prompts need separate interpretation. |
| [Li et al. — JEV-as-a-Judge](https://arxiv.org/abs/2609.26550v5) · 22 Sep → 9 Oct · v5 | Tests confidence-based escalation with frozen policies; some workloads support cheaper judging at comparable accuracy. Reference-free prose, adversarial style, and limited adjudication qualify the result. |
| [Rao & Callison-Burch — rubric judges](https://arxiv.org/abs/2609.29769v3) · 24 Sep → 13 Oct · v3 | Compares Jev, Decider, and LLM judges across nine panels; correlated errors restrict cascade gains. Default configurations and partly exploratory analyses leave room for different outcomes. |

These are different estimands, not entries in one leaderboard. A classification score, agreement with a rubric, resistance to a particular attack, and savings from a cascade should not be averaged into “Jev quality.”

## 3. Valid output, correct decision, useful uncertainty

**Schema validity** asks whether an answer belongs to the declared output space. **Accuracy** asks whether the selected answer is correct under the task’s labels. **Calibration** asks whether predicted probabilities match observed frequencies. A valid answer can be wrong; a calibrated model can still be insufficiently accurate for a particular decision.

TypeSafe’s Choice `confidence` is a derived statistic:

```text
confidence = (p_max − 1/n) / (1 − 1/n)
```

Here `n` is the number of options. It is not the selected option’s probability: with four options, `p_max = 0.7` gives confidence `0.6`. Noul has no separate returned confidence. Consequently, a confidence threshold is not automatically a promised accuracy. [Confidence documentation](https://docs.typesafe.ai/confidence)

For a policy that abstains, **coverage** is the fraction of cases accepted; **selective risk** is the average loss on those cases. Plotting risk against coverage exposes the tradeoff hidden by one threshold. A fallback must also correct the first model’s mistakes: confidence ranking alone cannot guarantee a good cascade. The reject-option literature supplies the relevant framework. [SelectiveNet](https://proceedings.mlr.press/v97/geifman19a.html)

## 4. Connections worth studying

**Probabilistic prediction.** Proper scoring rules evaluate whole predictive distributions, providing a foundation for Brier score and log loss. Calibration work shows why a highly accurate network still needs probability evaluation; language-model self-evaluation adds a relevant comparator. None establishes Jev’s training objective. [Gneiting & Raftery](https://doi.org/10.1198/016214506000001437) · [Guo et al.](https://proceedings.mlr.press/v70/guo17a.html) · [Kadavath et al.](https://arxiv.org/abs/2207.05221)

**Constrained generation.** LMQL and XGrammar show how generative systems can impose output constraints. They motivate comparisons that distinguish a typed API from the model producing its answers. [LMQL](https://www.sri.inf.ethz.ch/publications/beurerkellner2023prompting) · [XGrammar](https://arxiv.org/abs/2411.15100)

**Programmable inference.** DSPy studies optimization of model pipelines; SGLang studies their efficient execution. Both motivate controlling orchestration, caching, and serving conditions before attributing end-to-end improvements to one decision model. [DSPy](https://arxiv.org/abs/2310.03714) · [SGLang](https://arxiv.org/abs/2312.07104)

## 5. A proposed reproducible evaluation

**This is a research protocol, not an experiment executed by this project.**

1. **Define the decision.** Specify labels, ambiguity rules, error costs, and the acceptable human-review load. Separate human judgments, programmatically verifiable answers, and model-consensus references.
2. **Freeze the comparison.** Pin model versions, datasets, prompts, option descriptions, and preprocessing. Include label-logprob, constrained-generation, and task-specialist baselines where available. Report reasoning settings and unequal capabilities explicitly.
3. **Separate development from testing.** Select prompts, calibrators, and routing thresholds on development data. Preserve a held-out test set; group related examples to prevent leakage. Repeat a sample to measure response variability.
4. **Measure decisions and probabilities.** Report task-appropriate accuracy or F1, Brier score, log loss, calibration plots, and risk–coverage curves with uncertainty intervals. Break results down by language, label frequency, and task difficulty.
5. **Test the surrounding system.** Measure cost per successful workflow, latency distributions, retries, throughput, and fallback accuracy. Record region, concurrency, caching, and price date; evaluate attacks and input perturbations separately.
6. **Publish the trail.** Release permitted inputs, versioned templates, raw responses, manifests, and analysis scripts. Distinguish recomputing published numbers from issuing new model requests. Repeat after version changes before reusing thresholds.

The most useful next evidence would isolate model, interface, and workflow effects while tracking deployment shift. That requires matched comparisons and inspectable records, especially for new modalities and releases. Bibliographic metadata for the fourteen research references is maintained in [references.bib](../references.bib).
