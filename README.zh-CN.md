# Awesome Jev

[![Website](https://img.shields.io/badge/website-awesomejev.github.io-087E8B?style=flat-square&labelColor=374151)](https://awesomejev.github.io/zh/) [![Checks](https://img.shields.io/github/actions/workflow/status/reacher-z/Awesome-Jev/ci.yml?branch=main&style=flat-square&label=checks&color=087E8B&labelColor=374151)](https://github.com/reacher-z/Awesome-Jev/actions/workflows/ci.yml) [![License](https://img.shields.io/badge/license-MIT-6B7280?style=flat-square&labelColor=374151)](LICENSE)

围绕 **Jev 与类型化决策模型**，整理研究论文、模型、数据集、评测工具与实践指南。

**[主仓库](https://github.com/reacher-z/Awesome-Jev)** · [网站](https://awesomejev.github.io/zh/) · [论文目录](https://awesomejev.github.io/zh/papers/) · [研究指南](https://awesomejev.github.io/zh/guide/) · [新增资源](https://awesomejev.github.io/zh/discoveries/) · [English](README.md) · [综述](docs/survey.zh-CN.md) · [BibTeX](references.bib) · [参与贡献](CONTRIBUTING.md)

独立社区项目，与 TypeSafe AI 无隶属关系。最近整理：**2026-10-16**。网站从 [AwesomeJev.github.io](https://github.com/AwesomeJev/AwesomeJev.github.io) 仓库发布。

[新增资源目录](https://awesomejev.github.io/zh/discoveries/)补充了数百项项目、数据集、模型卡、指南和研究论文，并标明核查等级与相关性。[扩展审阅与计数方法](docs/expansion-2026-10-16.md)可供复查；摘要检查不等于全文评审。

## 目录

- [概览与官方资源](#概览与官方资源)
- [论文](#论文)
  - [评测与基准](#评测与基准)
  - [概率校准与一致性](#概率校准与一致性)
  - [评判与选择性自动化](#评判与选择性自动化)
  - [鲁棒性与安全](#鲁棒性与安全)
  - [架构、记忆与多模态](#架构记忆与多模态)
- [模型](#模型)
- [基准与评测工具](#基准与评测工具)
- [数据集](#数据集)
- [SDK 与集成](#sdk-与集成)
- [实践指南](#实践指南)
- [基础与相关研究](#基础与相关研究)
- [快速开始](#快速开始)
- [来源核查](#来源核查)
- [参与贡献](#参与贡献)
- [许可](#许可)

## 概览与官方资源

TypeSafe 的 Jev 接收状态与类型化问题，为应用代码返回决策和概率。输出格式合法、语义正确和概率校准是不同的性质。

- [Introducing System One Models & Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev) — 发布文章与厂商主张。
- [官方文档](https://docs.typesafe.ai/introduction) · [API](https://docs.typesafe.ai/api) · [模型与版本](https://docs.typesafe.ai/models)。
- [Choice](https://docs.typesafe.ai/primitives/choice) — 在最多 255 个选项中选择，返回概率分布与置信度。
- [Score](https://docs.typesafe.ai/primitives/score) — 在文字描述的有序等级上返回概率加权位置。
- [Noul](https://docs.typesafe.ai/primitives/noul) — 返回“是”的概率，没有独立的 confidence 字段。
- [置信度说明](https://docs.typesafe.ai/confidence) · [Jev 1.13 已知局限](https://docs.typesafe.ai/model-jaggedness/jev-1.13)。
- [实验性图片输入](https://docs.typesafe.ai/images) · [Box](https://docs.typesafe.ai/primitives/box) — 需显式开启；Box 要求 Jev 1.14。

截至 **2026-10-15**，`jev-latest` 指向 `jev-1.13.0`，`jev-preview` 指向 `jev-1.14.0`。评测时应固定版本。概念区别与评估协议见[综述](docs/survey.zh-CN.md)。

## 论文

下列 32 项直接研究均为 **arXiv 预印本**。日期对应已核查并链接的版本，不一定是首次提交日期。结果由作者报告，本项目没有复现实验。标题中的速度或成本主张保留作者原文。[参考文献](references.bib) · [证据比较](docs/survey.zh-CN.md)

### 评测与基准

- **[System1-Arena: Which Decisions Can Be Left to System 1?](https://arxiv.org/abs/2610.21244v1)** — Chen et al. *2026-10-15, arXiv v1*. 以匹配请求与闭环任务比较决策模型和推理模型。
- **[Reading Right, Acting Wrong: Diagnosing Decision Failures of System One Models in Agent Loops](https://arxiv.org/abs/2610.18579v1)** — Li, Krishnan & Padman. *2026-10-13, arXiv v1*. 将事实探针与行动选择配对，诊断决策失败。
- **[General Decision Models: Benchmarking and Insights Beyond Jev](https://arxiv.org/abs/2610.03935v2)** — Duan et al. *2026-10-12, arXiv v2*. 双语决策评估与多步骤系统中的可靠性。 [训练与推理代码](https://github.com/amazingljy1206/SII-Decision)。
- **[JEV versus LLMs: Accuracy, Cost and Calibration on Seven Political Science Replications](https://arxiv.org/abs/2610.06625v2)** — Denney & DiGiuseppe. *2026-10-06, arXiv v2*. 七项领域复现，比较准确率、成本与校准。
- **[Evaluating and Benchmarking the System One Model Jev](https://arxiv.org/abs/2609.37647v1)** — Deußer, Sparrenberg & Sifa. *2026-09-29, arXiv v1*. 覆盖 37 个数据集的分类与决策评测。 [代码](https://github.com/AppliedMachineLearning-Lab/jev-benchmarking).
- **[Typed Decision Models: An Early Evidence Audit and Evaluation Checklist](https://arxiv.org/abs/2609.32160v1)** — Tang & Zheng. *2026-09-26, arXiv v1*. 类型化决策的早期证据梳理与评估清单。

### 概率校准与一致性

- **[AnyJev Technical Report](https://arxiv.org/abs/2610.00831v1)** — Zhang et al. *2026-09-30, arXiv v1*. 无需训练的概率读出，修正标签先验与选项顺序偏差。 [代码](https://github.com/nokia-applied-research/AnyJev)。
- **[Jev thinks “I don’t know”, but doesn’t say it: Introducing Sys1Cal-v1 Dataset for Probability Calibration](https://arxiv.org/abs/2609.35342v1)** — Porcedda. *2026-09-28, arXiv v1*. 以构造概率目标进行受控校准测试。
- **[Beyond Calibration: Do a Typed-Decision Model’s Probabilities Obey the Probability Axioms?](https://arxiv.org/abs/2609.33209v1)** — Li, He & Li. *2026-09-27, arXiv v1*. 检验逻辑相关问题之间的概率一致性。

### 评判与选择性自动化

- **[JevAgentHarness: Benchmarking, Deploying and Training Decision Models That Share Control with LLMs](https://arxiv.org/abs/2610.21412v1)** — Zhu et al. *2026-10-15, arXiv v1*. 为各类选择拟合阈值，让决策模型与 LLM 共享 agent 控制。 [代码](https://github.com/JevAgentHarness/JevAgentHarness)。
- **[Decision Models vs. LLMs as Rubric Judges: Cheaper, Faster, and Wrong in the Same Places](https://arxiv.org/abs/2609.29769v3)** — Rao & Callison-Burch. *2026-10-13, arXiv v3*. 评分准则评判、相关错误与级联收益的局限。
- **[JevCascade: Readout Stability and Inference-Time Compute Allocation for Prefill-Only Decision Models](https://arxiv.org/abs/2610.07716v2)** — Li & Chen. *2026-10-10, arXiv v2*. 研究候选集合干预与置信度级联；排序稳定性并不等同概率校准。 [代码与数据](https://github.com/rlisml/jev-cascade)。
- **[JEV-as-a-Judge: Accept When Confident, Escalate When Unsure](https://arxiv.org/abs/2609.26550v5)** — Li, Miao, Krishnan & Padman. *2026-10-09, arXiv v5*. 基于置信度从 Jev 升级到推理评判模型。
- **[LAVOIR: Teaching a Single-Pass Decision Encoder When and What to Ask with Amortized Value of Information](https://arxiv.org/abs/2609.30706v1)** — Yilmaz, Tasdemir & Gozay. *2026-09-25, arXiv v1*. 在给出决策概率的同时估计追问缺失信息的价值。 [代码](https://github.com/moganai/lavoir)。
- **[REFLEX with Jev for Efficient Selective Control in LLM Agents](https://arxiv.org/abs/2609.26532v1)** — Wu & Lim. *2026-09-22, arXiv v1*. 以置信度控制 Jev 与 LLM 回退；收益取决于候选动作与基线路由。

### 鲁棒性与安全

- **[DecisionRobust: Benchmarking Robustness for JEV Style Decision Models Across Text and Vision](https://arxiv.org/abs/2610.19118v1)** — Lan et al. *2026-10-13, arXiv v1*. 结合标签有效性检查与留出模型，评估文本和视觉攻击。 [代码](https://github.com/Yifan-Lan/DecisionRobust) · [基准站点](https://yifan-lan.github.io/DecisionRobust/)。
- **[Same Attack, Different Judge: A First Controlled Adversarial Comparison of Jev, LLM Judges, and Purpose-Built Safety Classifiers](https://arxiv.org/abs/2610.17820v1)** — Li, Huang, Zhang & Liu. *2026-10-13, arXiv v1*. 对决策模型与安全分类器进行受控对抗比较。
- **[Type-Safe Is Not Error-Free: Typed Decision Models Follow the Option Name, Not the Definition Bound to It](https://arxiv.org/abs/2609.26758v3)** — Sun, Xu, Shi & Yang. *2026-10-08, arXiv v3*. 检验结构合法的输出是否仍会服从选项名称而非定义。
- **[Evaluating System One Models for Agent Security Decisions: Reliability, Calibration, and Selective Automation](https://arxiv.org/abs/2609.33401v3)** — Liu. *2026-10-03, arXiv v3*. 考察非对称风险下的高置信安全错误与选择性自动化。
- **[JevAdvBench: A Benchmark and Black-Box Attacks for Reinforcement Learning for Calibrated Decisions Models](https://arxiv.org/abs/2609.31142v1)** — Hu et al. *2026-09-25, arXiv v1*. 将对抗输入变化与干净输入、重复调用的自然波动对照。

### 架构、记忆与多模态

- **[Jeva: System One Models from First Principles](https://arxiv.org/abs/2610.18773v1)** — Li & Wang. *2026-10-13, arXiv v1*. 空答案、选项排列、可变候选集与缓存机制。
- **[VideoJev: System One Model for Video Understanding and Interaction](https://arxiv.org/abs/2610.18615v1)** — Zhu et al. *2026-10-13, arXiv v1*. 以时间区间和候选分数表达视频决策，通过缓存与联合推理复用视觉计算。 [项目页](https://mcg-nju.github.io/VideoJev/)。
- **[Releasing the Inner Jev: A Simple Recipe for Open Decision Models](https://arxiv.org/abs/2610.17205v1)** — Geuter, Cheng & Alvarez-Melis. *2026-10-12, arXiv v1*. 答案字母概率读出与监督式 LoRA 基线；评测包含模型生成的标签。 [服务代码](https://github.com/j-geuter/jeff-serve) · [OpenDecisions](https://huggingface.co/datasets/jgeuter/OpenDecisions)。
- **[SanSi: A Looped Typed Decision Model for System 1.5 Thinking](https://arxiv.org/abs/2610.07730v2)** — Gan, Lee & Kang. *2026-10-10, arXiv v2*. 通过隐状态循环计算决策，以额外计算成本换取准确率。 [训练与主要评测代码](https://github.com/minnesotanlp/Sansi)覆盖论文的部分实验。
- **[MetaEncoder: Exploring the Limit of Bi-Encoders for Multimodal System One Decision Making with Natural Language Interface](https://arxiv.org/abs/2610.11316v1)** — Cheng et al. *2026-10-08, arXiv v1*. 通过自然语言接口实现多模态决策与检索的双编码器方法。 [评测代码](https://github.com/facebook/meta-encoder-eval)。
- **[JevSpawn: Adaptive Agentic Inference through Compositional Action Spaces](https://arxiv.org/abs/2610.00437v1)** — Su & Huang. *2026-09-30, arXiv v1*. 组合有限行动字段，利用交互反馈探索候选路径。 [代码](https://github.com/Hoyant-Su/JevSpawn)。
- **[Bongard: Training Machine Intuition](https://arxiv.org/abs/2609.39111v1)** — Ding, Jin & Ji. *2026-09-30, arXiv v1*. 共享证据编码与候选概率读出，结合表征学习和行动结果反馈训练。 [模型权重](https://huggingface.co/AgentBull/bongard-mini)。
- **[Chinese-Jev: Bringing System One Model to Chinese-Language Tasks](https://arxiv.org/abs/2609.36965v1)** — Wang et al. *2026-09-29, arXiv v1*. 中文决策模型训练与领域评测。
- **[Mnemon: Raw Records, Fast Judgments, Slow Thoughts](https://arxiv.org/abs/2609.36059v1)** — Wang. *2026-09-28, arXiv v1*. 保留原始记忆记录，将 Jev 相关性判断与 LLM 检索规划、回答生成分开。 [代码与运行记录](https://github.com/Grivn/mnemon-memory-agent)。
- **[From Text Decisions to Pixels: An Study of Jev-Style Visual Choice Model](https://arxiv.org/abs/2609.29283v1)** — Zhou, Yang & Zhao. *2026-09-24, arXiv v1*. 视觉选择模型，分别考察适配与校准。
- **[Jev-Mem: System-One-Controlled Agentic Memory for Efficient AI Agents](https://arxiv.org/abs/2609.23986v1)** — Jiang, Li & Li. *2026-09-21, arXiv v1*. 以决策模型控制 agent 记忆构建与检索。
- **[this-that-model-1.0: A typed decision model that decides in 30 ms, for a millionth of a cent](https://arxiv.org/abs/2609.23886v1)** — Cheng, Dai & Sun. *2026-09-20, arXiv v1*. 采用隐藏状态概率读出的类型化决策架构。

## 模型

这些是独立实现，并非 TypeSafe 发布的模型权重。许可依据所链接的模型卡。API 兼容并不表示行为或准确率等同。

| 模型 | 发布者 | 声明许可 | 范围 |
| :--- | :--- | :--- | :--- |
| [Laya](https://huggingface.co/convaiinnovations/laya) | Convai Innovations | Apache-2.0 | 基于编码器的英语、多语言与工作流专用检查点。 |
| [Kev-4B](https://huggingface.co/jaredpalmer/kev-4b) | Jared Palmer | Apache-2.0 | Qwen3.5-4B-Base LoRA 适配器与指针头。 |
| [Bespoke Nimble 9B v3](https://huggingface.co/bespokelabs/Bespoke-Nimble-9B-v3) | Bespoke Labs | **CC BY-NC 4.0** | Qwen3.5-9B 适配器；非商业用途许可。 |
| [Intern-Decision-4B](https://huggingface.co/internlm/Intern-Decision-4B) | InternLM | Apache-2.0 | 经过决策微调的 Qwen 检查点，支持图片输入。 |
| [Perplexity Decider v1.1 27B](https://huggingface.co/perplexity-ai/pplx-decider-v1.1-27b) | Perplexity | Apache-2.0 | 独立决策读出；需查看注意力模式与访问说明。 |
| [GLiNER2.5-Decide](https://huggingface.co/fastino/GLiNER2.5-Decide) | Fastino | Apache-2.0 | 支持调用时指定标签集合的英语分类器，可输出多标签。 |
| [d3](https://huggingface.co/vllm-sr/d3) | vLLM Semantic Router | Apache-2.0 | 文本、图片与视频决策。 |
| [Clef](https://huggingface.co/Cloudflare/clef) | Cloudflare | Apache-2.0 | 采用联合 schema 预测头的多模态决策模型。 |

## 基准与评测工具

- **[Jev Decision Index](https://huggingface.co/spaces/multimodalart/jev-decision-index)** — 决策模型与比较评测的社区索引。[方法](https://multimodalart-jev-decision-index.static.hf.space/methodology.html) · [动态](https://multimodalart-jev-decision-index.static.hf.space/news.html) · [源文件](https://huggingface.co/spaces/multimodalart/jev-decision-index/tree/main)。完整分数包含私有测试，公开榜单不等于完整可复现材料。
- **[TypeSafe WorkflowEvals](https://github.com/typesafe-ai/WorkflowEvals)** — 官方工作流定义、运行器、已记录结果与评分代码。[交互结果](https://evals.typesafe.ai/) · [数据集合集](https://huggingface.co/collections/typesafeAI/workflowevals)。参考答案采用模型共识，并非独立建立的人工金标准。
- **[jev-benchmarking](https://github.com/AppliedMachineLearning-Lab/jev-benchmarking)** — Deußer 等人 37 数据集研究的配套代码。[论文](https://arxiv.org/abs/2609.37647v1)。
- **[PavelRavvich / jev-bench](https://github.com/PavelRavvich/jev-bench)** — 分类、原始预测、校准、延迟、成本与级联分析；比较前需核对采样和置信度定义。
- **[AY Automate benchmark](https://www.ayautomate.com/blog/jev-vs-llm-benchmark)** — 路由与注入检测实验，附代码和原始调用；结果由评测作者报告。

比较时记录模型版本、数据划分、概率接口、推理设置、访问路径、延迟分布及失败处理方式。参见[评估协议](docs/survey.zh-CN.md)。

## 数据集

TypeSafe 的四个数据集提供工作流案例、模型生成的参考标签与已发布运行记录。以下数量是所核查快照的案例数，不是独立人工标注数。另两项分别为训练混合数据和评测运行归档；不能直接当作独立测试基准，应先核对来源。

| 数据集 | 发布者 | 内容 |
| :--- | :--- | :--- |
| [Invoice Processing](https://huggingface.co/datasets/typesafeAI/evalsafe-invoice-processing) | TypeSafe | 150 个案例；发票动作、逐题参考标签与运行记录。 |
| [Customer Service](https://huggingface.co/datasets/typesafeAI/evalsafe-customer-service) | TypeSafe | 204 个案例；客服路由与动作选择。 |
| [Agent Trace Observability](https://huggingface.co/datasets/typesafeAI/evalsafe-agent-trace-observability) | TypeSafe | 111 个案例；针对 agent 运行轨迹的复核决策。 |
| [Security Incidents](https://huggingface.co/datasets/typesafeAI/evalsafe-security-incidents) | TypeSafe | 240 个案例；安全告警分诊与处置。 |
| [Bekko System One dataset v0](https://huggingface.co/datasets/hotchpotch/bekko-system-one-dataset-v0) | hotchpotch | 决策模型训练混合数据；需检查各组成来源和划分方式。 |
| [Bespoke Nimble v3 Decision Index archive](https://huggingface.co/datasets/bespokelabs/bespoke-nimble-9b-v3-decision-index) | Bespoke Labs | 已发布评测运行归档与推理材料，并非独立测试集。 |

## SDK 与集成

| 项目 | 维护方 | 用途 |
| :--- | :--- | :--- |
| [Python SDK](https://github.com/typesafe-ai/typesafe-sdk-python) | TypeSafe | 官方 Python 同步与异步客户端。 |
| [JavaScript / TypeScript SDK](https://github.com/typesafe-ai/typesafe-sdk-js) | TypeSafe | 官方客户端，支持答案类型推导。 |
| [System One Adapter](https://github.com/typesafe-ai/system-one-adapter-python) | TypeSafe | 用可比较的类型化问题接口评估 LLM 基线。 |
| [Public examples](https://github.com/typesafe-ai/typesafe-public-examples) | TypeSafe | 文档、演示与实践教程配套代码。 |
| [Agent skills](https://github.com/typesafe-ai/skills) | TypeSafe | 面向编码 agent 的集成指引。 |
| [n8n nodes](https://github.com/typesafe-ai/n8n-nodes-typesafe-ai) | TypeSafe | n8n 工作流节点。 |

## 实践指南

以下是厂商编写的实践教程；应使用自身任务的独立测试样例验证阈值。

- [置信度路由](https://docs.typesafe.ai/patterns/confidence-routing) — 将不确定案例转交其他系统或人工。
- [组合评分](https://docs.typesafe.ai/patterns/composite-scoring) — 在代码中按权重组合独立判断。
- [LLM 护栏](https://docs.typesafe.ai/cookbooks/llm_guardrails) · [引用核查](https://docs.typesafe.ai/cookbooks/citation_check) — 对照标准与来源检查生成内容。
- [RAG 段落分类](https://docs.typesafe.ai/cookbooks/classifying_rag_passages) — 筛选检索上下文。
- [层级分类](https://docs.typesafe.ai/cookbooks/hierarchical_classification) — 遍历大型标签树。
- [预解析值选择](https://docs.typesafe.ai/cookbooks/pre_parsed_value_extraction_cookbook) · [日期抽取](https://docs.typesafe.ai/cookbooks/date_extraction_cookbook) — 选择有限候选值，在代码中完成规范化与计算。

## 基础与相关研究

以下文献提供背景与比较方法，**不能据此推断 Jev 的内部架构、训练目标或采样器实现**。

| 主题 | 文献 | 链接 |
| :--- | :--- | :--- |
| 严格适当评分规则 | Gneiting & Raftery, *Strictly Proper Scoring Rules, Prediction, and Estimation*. JASA, 2007. | [论文](https://sites.stat.washington.edu/people/raftery/Research/PDF/Gneiting2007jasa.pdf) · [DOI](https://doi.org/10.1198/016214506000001437) |
| 校准 | Guo et al., *On Calibration of Modern Neural Networks*. ICML, 2017. | [论文](https://proceedings.mlr.press/v70/guo17a.html) |
| 选择性预测 | Geifman & El-Yaniv, *SelectiveNet*. ICML, 2019. | [论文](https://proceedings.mlr.press/v97/geifman19a.html) |
| 语言模型自我评估 | Kadavath et al., *Language Models (Mostly) Know What They Know*. 2022. | [论文](https://arxiv.org/abs/2207.05221) |
| 受约束的语言模型程序 | Beurer-Kellner et al., *Prompting Is Programming: A Query Language for Large Language Models*. PLDI, 2023. | [论文](https://www.sri.inf.ethz.ch/publications/beurerkellner2023prompting) |
| 结构化生成 | Dong et al., *XGrammar*. 2024. | [论文](https://arxiv.org/abs/2411.15100) · [代码](https://github.com/mlc-ai/xgrammar) |
| 可组合流水线 | Khattab et al., *DSPy*. 2023. | [论文](https://arxiv.org/abs/2310.03714) |
| 高效执行 | Zheng et al., *SGLang*. NeurIPS, 2024. | [论文](https://papers.nips.cc/paper_files/paper/2024/file/724be4472168f31ba1c9ac630f15dec8-Paper-Conference.pdf) · [代码](https://github.com/sgl-project/sglang) |

40 篇精选论文均收录于 [references.bib](references.bib)。核查范围与局限见[本次论文精选记录](docs/reviews/papers-2026-10-16.md)。

## 快速开始

```sh
pip install typesafe-sdk
```

设置 `TYPESAFE_API_KEY` 后，参照[最小 Python 示例](docs/quickstart.zh-CN.md)或[官方快速开始](https://docs.typesafe.ai/introduction/quickstart)。示例固定 `jev-1.13.0` 并展示 Choice 输出；已核对 SDK 接口，没有调用付费 API。

## 来源核查

[![Checked source corpus](https://img.shields.io/endpoint?url=https%3A%2F%2Fawesomejev.github.io%2Fdata%2Fsource-badge.json&style=flat-square)](docs/source-audit.md)

上面的精选资源与更大的[可搜索来源库](https://awesomejev.github.io/zh/#corpus)用途不同。来源库保留发现路径，并区分编辑审阅、自动内容筛查、摘要核查与仅元数据记录。**筛查不等于阅读全文或复现实验。**

- [方法与数量口径](docs/source-audit.md)
- [来源台账](data/) · [编辑抽样核查](data/editorial-audit.json)
- [维护流程](docs/maintenance.md)

公开来源扫描配置为每天洛杉矶时间 **09:17 和 21:17** 运行，更新通过可审查的 PR 提出；合并与网站同步仍由维护者执行。[时间安排与操作说明](docs/maintenance.md#twice-daily-source-scans)。

## 参与贡献

维护者：[reacher-z](https://github.com/reacher-z)。

请向 **[reacher-z/Awesome-Jev](https://github.com/reacher-z/Awesome-Jev)** 提交补充与纠错，提供一手来源、作者或发布者、日期／版本、研究主题，以及实际核查内容。欢迎补充代码、数据、局限与负面结果。流程见 [CONTRIBUTING.md](CONTRIBUTING.md)。

目录与条目组织参考了 [awesome-RLHF](https://github.com/opendilab/awesome-RLHF)，本项目保留独立的主题范围与来源核查规则。

## 许可

原创内容与代码采用 [MIT 许可](LICENSE)。外链论文、数据集、模型和第三方素材保留各自许可。
