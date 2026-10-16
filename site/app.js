const translations = {
  en: {
    skip: "Skip to the collection",
    navLabel: "Main navigation",
    navIndex: "Resources",
    navStart: "Get started",
    metaDescription:
      "Papers, models, datasets, and tools for Jev and typed decision models.",
    heroEyebrow: "AN INDEPENDENT FIELD GUIDE",
    heroLine1: "Awesome Jev",
    heroLine2: "by design.",
    heroDescription:
      "Papers, models, datasets, and tools for typed decisions.",
    explore: "Explore the collection",
    figureTitle: "FROM CONTEXT TO CHOICE",
    figureInput: "“I was charged twice.<br>Could you help?”",
    figureCaption: "Illustrative output. Not a live call or a benchmark.",
    figureAria:
      "Illustrative probabilities: billing 84 percent, technical 11 percent, other 5 percent",
    pathsLabel: "Reading paths",
    pathResearch: "Read the research",
    pathResearchSub: "Early evidence, open questions",
    pathBuild: "Build with intention",
    pathBuildSub: "SDKs, patterns, working examples",
    pathEvaluate: "Inspect the evidence",
    pathEvaluateSub: "Methods, datasets, reproducibility",
    snapshot: "CURRENT SNAPSHOT",
    versionNote:
      "Stable: Jev 1.13 · Preview: Jev 1.14.",
    modelNotes: "Model notes ↗",
    collectionEyebrow: "THE CURATED INDEX",
    collectionTitle: "Resource index",
    collectionIntro:
      "Filter by type or search titles and descriptions.",
    filterLabel: "Filter resources",
    filterAll: "All",
    filterPapers: "Papers",
    filterModels: "Models",
    filterTools: "Tools",
    filterDatasets: "Datasets",
    filterGuides: "Guides",
    filterEvaluations: "Evaluations",
    filterFoundations: "Foundations",
    searchLabel: "Search resources",
    searchPlaceholder: "Find something useful…",
    sourceNote: "DIRECT LINKS · CLEAR PROVENANCE",
    emptyTitle: "No matches, yet.",
    emptyDescription: "Try a broader term, or explore the full collection.",
    resetFilters: "Clear search & filters",
    editorialNote:
      "Preprints report their authors’ findings; listing is not independent validation. Foundations provide context, not evidence of Jev’s internal architecture.",
    startEyebrow: "A SMALL, PRACTICAL START",
    startTitle: "One call.<br><em>Typed decisions.</em>",
    startDescription:
      "Give Jev the context and a bounded question. Keep the next action in your code.",
    fullQuickstart: "Read the official quickstart",
    startFootnote:
      "Requires your own API key. This page makes no model calls. Confidence is a routing signal, not a correctness guarantee.",
    copyCode: "Copy code",
    copied: "Copied",
    copyFailed: "Select code to copy",
    keyNote: "Set TYPESAFE_API_KEY in your environment, then run:",
    contributeEyebrow: "A LIVING COLLECTION",
    contributeTitle: "Good work belongs here.",
    contributeDescription:
      "Found a thoughtful paper, a useful tool, or a result worth reproducing? Help make the collection better.",
    contributeLink: "Contribute on GitHub",
    independent: "Independent project. Not affiliated with TypeSafe AI.",
    lastCurated: "Last curated · October 15, 2026",
    backTop: "Back to top",
    sourceLink: "Website source",
    official: "Official",
    preprint: "Preprint · author-reported",
    background: "Background literature",
    community: "Community resource",
    modelcard: "Publisher model card",
    readFurther: "Project links",
    readmeLink: "README",
    surveyLink: "Research survey",
    bibtexLink: "BibTeX",
    modelEvidence:
      "Model capabilities and licenses follow publisher cards. API compatibility does not establish equivalent behavior or accuracy.",
    resourceCount: (n, total) =>
      `${String(n).padStart(2, "0")} / ${total} RESOURCES`,
    indexEyebrow: "AN ECOSYSTEM WORTH EXPLORING",
    indexTitle: "Decision Index",
    indexDescription:
      "Explore decision models and community evaluations, including open Jev-inspired alternatives.",
    indexLink: "Open the Decision Index",
    indexCaveat:
      "Community-maintained. Full scores include private tests; public materials do not reproduce the entire ranking.",
    corpusEyebrow: "THE WIDER RESEARCH CORPUS",
    corpusTitle: "Follow the connections.",
    corpusIntro:
      "Mixed screening levels: editorial review, automated content screening, abstract checks, and metadata-only discovery. Inspect each entry’s label; inclusion is a research lead, not an endorsement.",
    corpusAudit: "Screening methodology",
    metadataCorrection: "Metadata checked against the primary source",
    primaryMetadata: "View the source used for this correction",
    verificationDepth: "Verification depth",
    verificationHint: "How to read the labels",
    levelEditorial: "Editorially reviewed",
    levelContent: "Content screened",
    levelAbstract: "Abstract checked",
    levelMetadata: "Metadata only",
    editorialDefinition:
      "Focused editorial inspection of core Decision Index sources. This label does not imply experimental reproduction.",
    contentDefinition:
      "A public README, model card, or page passed automated relevance and substance checks. An arXiv landing page is an abstract, not a full-paper review.",
    abstractDefinition:
      "An abstract was screened through Hugging Face Papers or reconstructed from OpenAlex metadata. Retrieval of the original publisher page is not implied.",
    metadataDefinition:
      "A source was discovered, but its content check did not pass. These entries are excluded from the checked-source total.",
    sourceCount: (n) =>
      `${n.toLocaleString("en-US")} ${n === 1 ? "source" : "sources"}`,
    corpusAuditCounts: (checked, metadata) =>
      `${checked.toLocaleString("en-US")} checked · ${metadata.toLocaleString("en-US")} metadata-only`,
    corpusSummary: "Browse the research corpus",
    corpusSearch: "Search the research corpus",
    corpusPlaceholder: "Search titles, topics, or sources…",
    corpusLoading: "Loading the source index…",
    corpusUnavailable:
      "The corpus is being assembled. Explore the curated collection above in the meantime.",
    corpusEmpty: "No sources match this search.",
    corpusMore: "Show more sources",
    corpusCount: (n) => `${n.toLocaleString("en-US")} indexed sources`,
    corpusResults: (n, total) =>
      `${n.toLocaleString("en-US")} of ${total.toLocaleString("en-US")} sources`,
    screened: "Content-screened",
    corpusToggle: "SEARCHABLE SOURCE REGISTER",
  },
  zh: {
    skip: "跳转至资源索引",
    navLabel: "主导航",
    navIndex: "资源索引",
    navStart: "开始使用",
    metaDescription:
      "汇集 Jev 与类型化决策模型相关的论文、模型、数据集和工具。",
    heroEyebrow: "一份独立的研究与实践指南",
    heroLine1: "Awesome Jev",
    heroLine2: "始于设计。",
    heroDescription:
      "类型化决策相关的论文、模型、数据集和工具。",
    explore: "探索精选资源",
    figureTitle: "从上下文到决策",
    figureInput: "“我被重复扣费了，<br>可以帮忙处理吗？”",
    figureCaption: "示意输出。并非实时调用或评测结果。",
    figureAria: "示意概率：账单问题 84%，技术问题 11%，其他 5%",
    pathsLabel: "阅读路径",
    pathResearch: "阅读研究",
    pathResearchSub: "早期证据与开放问题",
    pathBuild: "动手构建",
    pathBuildSub: "SDK、设计模式与代码示例",
    pathEvaluate: "检查证据",
    pathEvaluateSub: "方法、数据集与可复现性",
    snapshot: "当前版本快照",
    versionNote:
      "稳定版：Jev 1.13 · 预览版：Jev 1.14。",
    modelNotes: "模型说明 ↗",
    collectionEyebrow: "精选资源索引",
    collectionTitle: "资源索引",
    collectionIntro:
      "按类型筛选，或搜索标题与简介。",
    filterLabel: "筛选资源",
    filterAll: "全部",
    filterPapers: "论文",
    filterModels: "模型",
    filterTools: "工具",
    filterDatasets: "数据集",
    filterGuides: "指南",
    filterEvaluations: "评测",
    filterFoundations: "基础研究",
    searchLabel: "搜索资源",
    searchPlaceholder: "搜索论文、工具或主题…",
    sourceNote: "直达来源 · 标注出处",
    emptyTitle: "暂时没有匹配项。",
    emptyDescription: "试试更宽泛的关键词，或浏览完整资源库。",
    resetFilters: "清除搜索与筛选",
    editorialNote:
      "预印本呈现作者报告的结果，收录不代表我们已独立验证。基础文献提供研究背景，不代表 Jev 内部架构的证据。",
    startEyebrow: "从一个小例子开始",
    startTitle: "一次调用。<br><em>类型化决策。</em>",
    startDescription: "给出上下文与边界清晰的问题。让代码决定下一步行动。",
    fullQuickstart: "阅读官方快速入门",
    startFootnote:
      "需要你自己的 API key。本页面不会调用模型。置信度用于路由判断，并不保证答案正确。",
    copyCode: "复制代码",
    copied: "已复制",
    copyFailed: "请选择代码后复制",
    keyNote: "先在环境变量中设置 TYPESAFE_API_KEY，然后运行：",
    contributeEyebrow: "持续更新的资源库",
    contributeTitle: "让好工作被更多人看见。",
    contributeDescription:
      "发现了值得读的论文、实用的工具，或值得复现的结果？欢迎一起完善这份资源库。",
    contributeLink: "在 GitHub 上参与贡献",
    independent: "独立社区项目，与 TypeSafe AI 无隶属关系。",
    lastCurated: "最近整理 · 2026 年 10 月 15 日",
    backTop: "返回顶部",
    sourceLink: "网站源码",
    official: "官方资源",
    preprint: "预印本 · 作者报告",
    background: "背景文献",
    community: "社区资源",
    modelcard: "发布者模型卡",
    readFurther: "项目链接",
    readmeLink: "项目说明",
    surveyLink: "研究综述",
    bibtexLink: "BibTeX 文献",
    modelEvidence:
      "模型能力和许可依据发布者模型卡。API 兼容并不证明行为或准确率等同。",
    resourceCount: (n, total) =>
      `${String(n).padStart(2, "0")} / ${total} 项资源`,
    indexEyebrow: "探索决策模型生态",
    indexTitle: "Decision Index",
    indexDescription: "查看决策模型与社区评测，包括受 Jev 启发的开放模型。",
    indexLink: "打开 Decision Index",
    indexCaveat: "社区维护。完整分数包含私有测试，公开材料无法复现全部排名。",
    corpusEyebrow: "更广泛的研究语料",
    corpusTitle: "沿着线索，继续探索。",
    corpusIntro:
      "各来源核查深度不同：编辑审阅、自动内容筛查、摘要核查或仅元数据发现。请查看条目标注；收录代表研究线索，而非质量背书。",
    corpusAudit: "核查方法与范围",
    metadataCorrection: "元数据已按原始来源核对",
    primaryMetadata: "查看此次修正依据",
    verificationDepth: "核查深度",
    verificationHint: "如何理解来源标签",
    levelEditorial: "编辑审阅",
    levelContent: "内容筛查",
    levelAbstract: "摘要核查",
    levelMetadata: "仅元数据",
    editorialDefinition:
      "对 Decision Index 核心来源进行聚焦编辑审查，不代表已复现实验。",
    contentDefinition:
      "公开 README、模型卡或网页通过自动相关性与实质内容检查。arXiv 简介页仍只是摘要，不代表阅读全文。",
    abstractDefinition:
      "通过 Hugging Face Papers 获取摘要，或从 OpenAlex 元数据重建摘要并筛查；不表示已获取原始出版商页面。",
    metadataDefinition:
      "发现了来源，但内容检查未通过；这些条目不计入已核查来源总数。",
    sourceCount: (n) => `${n.toLocaleString("zh-CN")} 项来源`,
    corpusAuditCounts: (checked, metadata) =>
      `${checked.toLocaleString("zh-CN")} 项已核查 · ${metadata.toLocaleString("zh-CN")} 项仅元数据`,
    corpusSummary: "浏览研究来源库",
    corpusSearch: "搜索研究来源库",
    corpusPlaceholder: "搜索标题、主题或来源…",
    corpusLoading: "正在加载来源索引…",
    corpusUnavailable: "研究来源库正在整理中，可先浏览上方精选资源。",
    corpusEmpty: "没有匹配的来源。",
    corpusMore: "显示更多来源",
    corpusCount: (n) => `${n.toLocaleString("zh-CN")} 项索引来源`,
    corpusResults: (n, total) =>
      `${total.toLocaleString("zh-CN")} 项中匹配 ${n.toLocaleString("zh-CN")} 项`,
    screened: "已做内容筛查",
    corpusToggle: "可搜索的来源目录",
  },
};

// Descriptions are editorial summaries. Paper findings remain author-reported.
const resources = [
  {
    category: "Papers",
    title: "Type-Safe Is Not Error-Free: Typed Decision Models Follow the Option Name, Not the Definition Bound to It",
    by: "Sun, Xu, Shi & Yang · 2026-10-08 · v3",
    date: "2026-10-08",
    url: "https://arxiv.org/abs/2609.26758v3",
    en: "Tests conflicts between option names and definitions despite structurally valid outputs.",
    zh: "检验输出结构合法时，选项名称与定义之间的冲突。",
  },
  {
    category: "Papers",
    title: "AnyJev Technical Report",
    by: "Zhang et al. · 2026-09-30 · v1",
    date: "2026-09-30",
    url: "https://arxiv.org/abs/2610.00831v1",
    en: "Training-free decision readout with label-prior and option-order correction.",
    zh: "无需训练的决策读出，修正标签先验与选项顺序偏差。",
  },
  {
    category: "Papers",
    title: "LAVOIR: Teaching a Single-Pass Decision Encoder When and What to Ask with Amortized Value of Information",
    by: "Yilmaz, Tasdemir & Gozay · 2026-09-25 · v1",
    date: "2026-09-25",
    url: "https://arxiv.org/abs/2609.30706v1",
    en: "Estimates whether asking for missing information would improve a typed decision.",
    zh: "估计追问缺失信息是否有助于改进类型化决策。",
  },
  {
    category: "Papers",
    title: "General Decision Models: Benchmarking and Insights Beyond Jev",
    by: "Duan et al. · 2026-10-12 · v2",
    date: "2026-10-12",
    url: "https://arxiv.org/abs/2610.03935v2",
    en: "Bilingual decision evaluation and reliability when local decisions compose into larger systems.",
    zh: "双语决策评估，以及局部决策组合成更大系统时的可靠性。",
  },
  {
    category: "Papers",
    title: "JevAgentHarness: Benchmarking, Deploying and Training Decision Models That Share Control with LLMs",
    by: "Zhu et al. · 2026-10-15 · v1",
    date: "2026-10-15",
    url: "https://arxiv.org/abs/2610.21412v1",
    en: "Studies fitted confidence thresholds for sharing agent control with decision models.",
    zh: "研究通过拟合置信度阈值，让决策模型参与 agent 控制。",
  },
  {
    "category": "Datasets",
    "title": "evalsafe-invoice-processing",
    "by": "TypeSafe · WorkflowEvals",
    "provenance": "official",
    "url": "https://huggingface.co/datasets/typesafeAI/evalsafe-invoice-processing",
    "en": "Official dataset for the invoice-processing workflow evaluation.",
    "zh": "官方发票处理工作流评测数据集。"
  },
  {
    "category": "Datasets",
    "title": "evalsafe-customer-service",
    "by": "TypeSafe · WorkflowEvals",
    "provenance": "official",
    "url": "https://huggingface.co/datasets/typesafeAI/evalsafe-customer-service",
    "en": "Official dataset for the customer-service workflow evaluation.",
    "zh": "官方客户服务工作流评测数据集。"
  },
  {
    "category": "Datasets",
    "title": "evalsafe-security-incidents",
    "by": "TypeSafe · WorkflowEvals",
    "provenance": "official",
    "url": "https://huggingface.co/datasets/typesafeAI/evalsafe-security-incidents",
    "en": "Official dataset for the security-incident workflow evaluation.",
    "zh": "官方安全事件工作流评测数据集。"
  },
  {
    "category": "Datasets",
    "title": "evalsafe-agent-trace-observability",
    "by": "TypeSafe · WorkflowEvals",
    "provenance": "official",
    "url": "https://huggingface.co/datasets/typesafeAI/evalsafe-agent-trace-observability",
    "en": "Official evaluation dataset for the agent-trace observability workflow.",
    "zh": "官方 agent 轨迹观测工作流评测数据集。"
  },
  {
    "category": "Datasets",
    "title": "Bekko System One Dataset v0",
    "by": "hotchpotch · Training mixture",
    "provenance": "community",
    "url": "https://huggingface.co/datasets/hotchpotch/bekko-system-one-dataset-v0",
    "en": "A community training mixture for System One-style decision models. Read the card for its composition and usage conditions.",
    "zh": "面向 System One 风格决策模型的社区训练混合数据；组成与使用条件见数据卡。"
  },
  {
    "category": "Datasets",
    "title": "Bespoke Nimble 9B v3 — Decision Index runs",
    "by": "Bespoke Labs · Evaluation archive",
    "provenance": "community",
    "url": "https://huggingface.co/datasets/bespokelabs/bespoke-nimble-9b-v3-decision-index",
    "en": "An archive of Decision Index evaluation runs for Bespoke Nimble 9B v3.",
    "zh": "Bespoke Nimble 9B v3 在 Decision Index 上的评测运行归档。"
  },
  {
    category: "Papers",
    title: "this-that-model-1.0",
    by: "Cheng et al. · 2026-09-20 · v1",
    date: "2026-09-20",
    url: "https://arxiv.org/abs/2609.23886v1",
    en: "An open typed-decision model using hidden-state readout. The abstract reports a small external comparison.",
    zh: "采用隐藏状态读出的开放类型化决策模型。摘要报告了一项小规模外部比较。",
  },
  {
    category: "Papers",
    title: "Jev-Mem: System-One-Controlled Agentic Memory",
    by: "Jiang et al. · 2026-09-21 · v1",
    date: "2026-09-21",
    url: "https://arxiv.org/abs/2609.23986v1",
    en: "Studies Jev as a controller for agent memory. Reported outcomes concern the complete memory workflow.",
    zh: "研究以 Jev 控制 agent 记忆；报告结果衡量完整记忆工作流。",
  },
  {
    category: "Papers",
    title: "From Text Decisions to Pixels",
    by: "Zhou et al. · 2026-09-24 · v1",
    date: "2026-09-24",
    url: "https://arxiv.org/abs/2609.29283v1",
    en: "A Jev-style visual-choice study separating adaptation gains, candidate-readout validity, and calibration limits.",
    zh: "Jev 风格视觉选择模型研究，区分适配收益、候选读出有效性与校准局限。",
  },
  {
    category: "Papers",
    title: "JevAdvBench",
    by: "Hu et al. · 2026-09-25 · v1",
    date: "2026-09-25",
    url: "https://arxiv.org/abs/2609.31142v1",
    en: "A black-box adversarial benchmark. A changed decision is not necessarily an incorrect decision.",
    zh: "黑盒对抗评测基准。决策发生变化，并不必然代表决策错误。",
  },
  {
    category: "Papers",
    title:
      "Beyond Calibration: Do Typed Decisions Obey the Probability Axioms?",
    by: "Li et al. · 2026-09-27 · v1",
    date: "2026-09-27",
    url: "https://arxiv.org/abs/2609.33209v1",
    en: "Tests coherence between logically related probabilities, separately from accuracy and calibration.",
    zh: "检验逻辑相关命题的概率一致性，与准确率和校准分别考察。",
  },
  {
    category: "Papers",
    title: "System One Models for Agent Security Decisions",
    by: "Liu · 2026-10-03 · v3",
    date: "2026-10-03",
    url: "https://arxiv.org/abs/2609.33401v3",
    en: "Examines reliability, group-specific confident errors, and selective automation in security decisions.",
    zh: "研究安全决策中的可靠性、不同群体的高置信错误与选择性自动化。",
  },
  {
    category: "Papers",
    title: "Sys1Cal-v1: A Dataset for Probability Calibration",
    by: "Porcedda · 2026-09-28 · v1",
    date: "2026-09-28",
    url: "https://arxiv.org/abs/2609.35342v1",
    en: "A controlled calibration study using constructed probabilities. Interpretations of latent uncertainty remain hypotheses.",
    zh: "使用构造概率进行受控校准测试；对潜在不确定性的解释仍属研究假说。",
  },
  {
    category: "Papers",
    title: "Chinese-Jev: Bringing System One Models to Chinese-Language Tasks",
    by: "Wang et al. · 2026-09-29 · v1",
    date: "2026-09-29",
    url: "https://arxiv.org/abs/2609.36965v1",
    en: "A Chinese typed-decision model and proposed benchmark; domain-specific training calls for independent validation.",
    zh: "面向中文的类型化决策模型与新基准；领域专用训练的效果仍需独立验证。",
  },
  {
    category: "Papers",
    title: "Jeva: System One Models from First Principles",
    by: "Li & Wang · 2026-10-13 · v1",
    date: "2026-10-13",
    url: "https://arxiv.org/abs/2610.18773v1",
    en: "A decision-model architecture exploring null handling, option permutations, scaling, and caching. Its design is Jeva’s, not Jev’s disclosed internals.",
    zh: "探索空答案、选项排列、规模扩展与缓存的决策架构。这是 Jeva 的设计，并非 Jev 已披露的内部实现。",
  },
  {
    category: "Papers",
    title: "System1-Arena: Which Decisions Can Be Left to System 1?",
    by: "Chen et al. · 2026-10-15 · v1",
    date: "2026-10-15",
    url: "https://arxiv.org/abs/2610.21244v1",
    en: "A benchmark spanning matched requests and closed-loop tasks. Experiments have not been reproduced here.",
    zh: "涵盖匹配请求与闭环任务的基准；本项目尚未复现其实验。",
  },
  {
    category: "Models",
    title: "Laya",
    by: "convaiinnovations · Apache-2.0",
    provenance: "modelcard",
    url: "https://huggingface.co/convaiinnovations/laya",
    en: "An encoder-based decision family with English, multilingual, and workflow-specific checkpoints.",
    zh: "基于编码器的决策模型家族，包含英语、多语言与工作流专用检查点。",
  },
  {
    category: "Models",
    title: "Kev-4B",
    by: "Jared Palmer · Apache-2.0",
    provenance: "modelcard",
    url: "https://huggingface.co/jaredpalmer/kev-4b",
    en: "A Qwen3.5-4B-Base LoRA adapter and pointer head for decisions over documents and typed questions.",
    zh: "基于 Qwen3.5-4B-Base 的 LoRA 适配器与指针头，面向文档与类型化问题的决策。",
  },
  {
    category: "Models",
    title: "Bespoke Nimble 9B v3",
    by: "Bespoke Labs · CC BY-NC 4.0",
    provenance: "modelcard",
    url: "https://huggingface.co/bespokelabs/Bespoke-Nimble-9B-v3",
    en: "A Qwen3.5-9B LoRA adapter returning candidate probabilities. Released under a noncommercial license.",
    zh: "返回候选项概率的 Qwen3.5-9B LoRA 适配器；采用非商业用途许可。",
  },
  {
    category: "Models",
    title: "Intern-Decision-4B",
    by: "InternLM · Apache-2.0",
    provenance: "modelcard",
    url: "https://huggingface.co/internlm/Intern-Decision-4B",
    en: "A decision-tuned Qwen checkpoint with a structured inference wrapper and image support.",
    zh: "经过决策微调的 Qwen 检查点，提供结构化推理封装并支持图片输入。",
  },
  {
    category: "Models",
    title: "Perplexity Decider v1.1 27B",
    by: "Perplexity · Apache-2.0",
    provenance: "modelcard",
    url: "https://huggingface.co/perplexity-ai/pplx-decider-v1.1-27b",
    en: "A separate decision readout and saved calibration temperature. Follow the card’s attention-mode and access notes.",
    zh: "采用独立决策读出与已保存的校准温度；需注意模型卡中的注意力模式及访问说明。",
  },
  {
    category: "Models",
    title: "GLiNER2.5-Decide",
    by: "Fastino · Apache-2.0",
    provenance: "modelcard",
    url: "https://huggingface.co/fastino/GLiNER2.5-Decide",
    en: "A 340M English classifier with runtime label sets and single-label or multi-label decisions.",
    zh: "340M 英语分类模型，支持调用时指定标签集合，以及单标签和多标签决策。",
  },
  {
    category: "Models",
    title: "d3",
    by: "vLLM Semantic Router · Apache-2.0",
    provenance: "modelcard",
    url: "https://huggingface.co/vllm-sr/d3",
    en: "A text, image, and video decision model with Choice, Yes/No, and Score outputs.",
    zh: "支持文本、图片与视频的决策模型，提供 Choice、Yes/No 与 Score 输出。",
  },
  {
    category: "Models",
    title: "Clef",
    by: "Cloudflare · Apache-2.0",
    provenance: "modelcard",
    url: "https://huggingface.co/Cloudflare/clef",
    en: "A multimodal model with a joint schema head, returning probabilities over allowed answers.",
    zh: "使用联合 schema 预测头的多模态模型，返回允许答案集合上的概率。",
  },
  {
    category: "Papers",
    title: "Evaluating and Benchmarking the System One Model Jev",
    by: "Deußer et al. · 2026-09-29 · v1",
    date: "2026-09-29",
    url: "https://arxiv.org/abs/2609.37647v1",
    en: "An early benchmark study of Jev. Read the task selection and evaluation setup alongside its reported results.",
    zh: "Jev 的早期基准研究。阅读报告结果时，同时检查任务选择与评测设置。",
  },
  {
    category: "Papers",
    title:
      "Typed Decision Models: An Early Evidence Audit and Evaluation Checklist",
    by: "Tang & Zheng · 2026-09-26 · v1",
    date: "2026-09-26",
    url: "https://arxiv.org/abs/2609.32160v1",
    en: "An evidence audit and a checklist for evaluating typed decision models.",
    zh: "围绕类型化决策模型的证据审查与评估清单。",
  },
  {
    category: "Papers",
    title: "Same Attack, Different Judge",
    by: "Li et al. · 2026-10-13 · v1",
    date: "2026-10-13",
    url: "https://arxiv.org/abs/2610.17820v1",
    en: "A controlled adversarial comparison of Jev, LLM judges, and purpose-built safety classifiers.",
    zh: "对 Jev、LLM 评判模型与专用安全分类器进行受控对抗比较。",
  },
  {
    category: "Papers",
    title:
      "JEV versus LLMs: Accuracy, Cost and Calibration on Seven Political Science Replications",
    by: "Denney & DiGiuseppe · 2026-10-06 · v2",
    date: "2026-10-06",
    url: "https://arxiv.org/abs/2610.06625v2",
    en: "Studies accuracy, cost, and calibration in seven political-science replication tasks.",
    zh: "在七项政治学复现任务中考察准确率、成本与校准。",
  },
  {
    category: "Papers",
    title: "JEV-as-a-Judge: Accept When Confident, Escalate When Unsure",
    by: "Li et al. · 2026-10-09 · v5",
    date: "2026-10-09",
    url: "https://arxiv.org/abs/2609.26550v5",
    en: "Studies confidence-based escalation from Jev to a reasoning judge, including limits under distribution shift.",
    zh: "研究基于置信度从 Jev 升级到推理评判模型的方法，以及分布变化下的局限。",
  },
  {
    category: "Papers",
    title: "Decision Models vs. LLMs as Rubric Judges",
    by: "Rao & Callison-Burch · 2026-10-13 · v3",
    date: "2026-10-13",
    url: "https://arxiv.org/abs/2609.29769v3",
    en: "Compares rubric judges and examines correlated errors that can limit cascade improvements.",
    zh: "比较评分准则评判模型，考察相关错误如何限制级联系统的收益。",
  },
  {
    category: "Tools",
    title: "TypeSafe Python SDK",
    by: "Python · MIT",
    url: "https://github.com/typesafe-ai/typesafe-sdk-python",
    en: "The official sync and async client for typed Jev questions and answers.",
    zh: "官方 Python 同步与异步客户端，支持类型化问题和答案。",
  },
  {
    category: "Tools",
    title: "TypeSafe JavaScript SDK",
    by: "TypeScript / JavaScript · MIT",
    url: "https://github.com/typesafe-ai/typesafe-sdk-js",
    en: "The official JavaScript client with answer types inferred from your questions.",
    zh: "官方 JavaScript 客户端，可根据问题推导答案类型。",
  },
  {
    category: "Tools",
    title: "System One Adapter",
    by: "Python · MIT",
    url: "https://github.com/typesafe-ai/system-one-adapter-python",
    en: "Compare LLMs through the same question interface, with probability outputs and request diagnostics.",
    zh: "用相同问题接口比较 LLM，支持概率输出与请求诊断。",
  },
  {
    category: "Tools",
    title: "TypeSafe Agent Skills",
    by: "Coding agents · MIT",
    url: "https://github.com/typesafe-ai/skills",
    en: "Official guidance for coding agents building with the System One API.",
    zh: "帮助编码 agent 使用 System One API 的官方技能。",
  },
  {
    category: "Tools",
    title: "TypeSafe Public Examples",
    by: "Cookbooks & demos · MIT",
    url: "https://github.com/typesafe-ai/typesafe-public-examples",
    en: "Source code accompanying official documentation, demos, and cookbooks.",
    zh: "官方文档、演示与实践教程配套源代码。",
  },
  {
    category: "Tools",
    title: "TypeSafe for n8n",
    by: "Workflow integration · MIT",
    url: "https://github.com/typesafe-ai/n8n-nodes-typesafe-ai",
    en: "TypeSafe-maintained nodes for adding typed decisions to n8n workflows.",
    zh: "由 TypeSafe 维护的 n8n 节点，用于将类型化决策加入工作流。",
  },
  {
    category: "Guides",
    title: "Introducing System One Models & Jev",
    by: "TypeSafe · September 15, 2026",
    url: "https://typesafe.ai/blog/introducing-system-one-models-and-jev",
    en: "The launch article. A primary source for the provider’s design claims and their stated caveats.",
    zh: "发布文章：了解厂商设计主张及其限定条件的一手来源。",
  },
  {
    category: "Guides",
    title: "Primitives: Choice, Score, Noul",
    by: "API concepts",
    url: "https://docs.typesafe.ai/primitives",
    en: "Choose between categorical decisions, ordered ratings, and yes/no probabilities.",
    zh: "了解闭集选择、有序评分与是非概率三类决策原语。",
  },
  {
    category: "Guides",
    title: "Confidence",
    by: "Probability & routing",
    url: "https://docs.typesafe.ai/confidence",
    en: "How confidence is derived from a distribution, and how it differs from probability.",
    zh: "解释置信度的计算方式，以及它与概率的区别。",
  },
  {
    category: "Guides",
    title: "Jev 1.13 Jaggedness",
    by: "Limitations · reviewed October 2, 2026",
    url: "https://docs.typesafe.ai/model-jaggedness/jev-1.13",
    en: "Documented limitations: numeric precision, long irrelevant context, adversarial inputs, and option-order sensitivity.",
    zh: "已知局限：数值精度、无关长上下文、对抗输入与选项顺序敏感性。",
  },
  {
    category: "Guides",
    title: "Guardrails for LLMs",
    by: "Official cookbook",
    url: "https://docs.typesafe.ai/cookbooks/llm_guardrails",
    en: "Combine narrow risk questions with application rules for passing, reviewing, or blocking content.",
    zh: "用多个风险问题配合应用规则，对内容放行、复核或拦截。",
  },
  {
    category: "Guides",
    title: "Double-checking Citations",
    by: "Official cookbook",
    url: "https://docs.typesafe.ai/cookbooks/citation_check",
    en: "Check whether a citation’s source context supports a claim.",
    zh: "检查引文的来源上下文是否支持相关主张。",
  },
  {
    category: "Guides",
    title: "Hierarchical Classification",
    by: "Official cookbook",
    url: "https://docs.typesafe.ai/cookbooks/hierarchical_classification",
    en: "Use Choice probabilities to explore deep classification trees.",
    zh: "使用 Choice 概率探索多层分类树。",
  },
  {
    category: "Evaluations",
    title: "Jev Decision Index",
    by: "Hugging Face · community",
    provenance: "community",
    url: "https://huggingface.co/spaces/multimodalart/jev-decision-index",
    en: "A community index of decision models and evaluations. Full rankings include private tests.",
    zh: "决策模型与评测的社区索引；完整排名包含私有测试。",
  },
  {
    category: "Evaluations",
    title: "Workflow Evals",
    by: "Interactive evaluation explorer",
    url: "https://evals.typesafe.ai/",
    en: "Inspect four structured workflows. Scores measure agreement with model-generated references.",
    zh: "查看四类结构化工作流。分数衡量与模型生成参考结果的一致性。",
  },
  {
    category: "Evaluations",
    title: "WorkflowEvals — Code",
    by: "Python · Apache-2.0",
    url: "https://github.com/typesafe-ai/WorkflowEvals",
    en: "The official evaluation runner, workflow definitions, scoring, and plotting tools.",
    zh: "官方评测运行器、工作流定义、评分与绘图工具。",
  },
  {
    category: "Evaluations",
    title: "WorkflowEvals — Datasets",
    by: "Hugging Face · four datasets",
    url: "https://huggingface.co/collections/typesafeAI/workflowevals",
    en: "Published cases, model-generated references, and recorded runs for inspecting reproducibility.",
    zh: "公开案例、模型生成的参考标签与运行记录，便于检查可复现性。",
  },
  {
    category: "Foundations",
    title: "Strictly Proper Scoring Rules, Prediction, and Estimation",
    by: "Gneiting & Raftery · JASA 2007 · Author PDF",
    url: "https://sites.stat.washington.edu/people/raftery/Research/PDF/Gneiting2007jasa.pdf",
    en: "A foundation for evaluating and incentivizing honest probabilistic predictions.",
    zh: "评估概率预测与鼓励诚实概率表达的理论基础。",
  },
  {
    category: "Foundations",
    title: "On Calibration of Modern Neural Networks",
    by: "Guo et al. · ICML 2017",
    url: "https://proceedings.mlr.press/v70/guo17a.html",
    en: "A practical reference for calibration and temperature scaling.",
    zh: "概率校准与温度缩放的经典参考。",
  },
  {
    category: "Foundations",
    title: "SelectiveNet",
    by: "Geifman & El-Yaniv · ICML 2019",
    url: "https://proceedings.mlr.press/v97/geifman19a.html",
    en: "Studies prediction with a reject option and the trade-off between coverage and risk.",
    zh: "研究带拒绝选项的预测，以及覆盖率与风险之间的关系。",
  },
  {
    category: "Foundations",
    title: "Language Models (Mostly) Know What They Know",
    by: "Kadavath et al. · 2022",
    url: "https://arxiv.org/abs/2207.05221",
    en: "An investigation of language models’ self-evaluation and uncertainty.",
    zh: "研究语言模型的自我评估与不确定性。",
  },
  {
    category: "Foundations",
    title: "LMQL — Prompting Is Programming",
    by: "Beurer-Kellner et al. · PLDI 2023",
    url: "https://www.sri.inf.ethz.ch/publications/beurerkellner2023prompting",
    en: "A programming-language approach to constrained language-model interaction.",
    zh: "以编程语言方式组织受约束的语言模型交互。",
  },
  {
    category: "Foundations",
    title: "XGrammar",
    by: "Dong et al. · 2024",
    url: "https://arxiv.org/abs/2411.15100",
    en: "Efficient grammar-constrained generation: a useful comparison point for typed outputs.",
    zh: "高效语法约束生成，为理解类型化输出提供比较背景。",
  },
  {
    category: "Foundations",
    title: "DSPy",
    by: "Khattab et al. · 2023",
    url: "https://arxiv.org/abs/2310.03714",
    en: "Declarative language-model programs and pipeline optimization.",
    zh: "声明式语言模型程序与流水线优化。",
  },
  {
    category: "Foundations",
    title: "SGLang",
    by: "Zheng et al. · NeurIPS 2024",
    url: "https://arxiv.org/abs/2312.07104",
    en: "Efficient execution of structured language-model programs.",
    zh: "结构化语言模型程序的高效执行。",
  },
];

const categoryOrder = ["Papers", "Models", "Tools", "Datasets", "Evaluations", "Guides", "Foundations"];
resources.sort((a, b) => {
  const categoryDifference = categoryOrder.indexOf(a.category) - categoryOrder.indexOf(b.category);
  if (categoryDifference) return categoryDifference;
  if (a.category !== "Papers") return 0;
  const dateDifference = (b.date || "").localeCompare(a.date || "");
  if (dateDifference) return dateDifference;
  const paperId = resource => resource.url.match(/\d{4}\.\d{4,5}/)?.[0] || "";
  return paperId(b).localeCompare(paperId(a), "en", { numeric: true });
});

let language = "en";
let activeFilter = "All";
let corpusSources = [];
let corpusCounts = {};
let corpusLoaded = false;
let corpusLimit = 24;
let copyTimer;
const $ = (selector) => document.querySelector(selector);
const icon = (name) =>
  `<svg class="icon" aria-hidden="true"><use href="./assets/fontawesome/icons.svg#${name}"></use></svg>`;
const categoryIcons = {
  All: "filter",
  Models: "foundation",
  Papers: "paper",
  Tools: "code",
  Datasets: "foundation",
  Guides: "guide",
  Evaluations: "evaluation",
  Foundations: "foundation",
};
function renderCopyButton(key = "copyCode") {
  $("#copy-code").innerHTML =
    icon(key === "copied" ? "check" : "copy") +
    "<span>" +
    escapeHTML(t(key)) +
    "</span>";
}
const escapeHTML = (value) =>
  String(value ?? "").replace(
    /[&<>"']/g,
    (char) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[
        char
      ],
  );
const safeURL = (value) => {
  try {
    const url = new URL(value);
    return /^https?:$/.test(url.protocol) ? url.href : "";
  } catch {
    return "";
  }
};
function t(key) {
  return translations[language][key] ?? translations.en[key] ?? key;
}
function localizedMetadata(value) {
  if (language !== "zh") return value;
  const labels = {
    "Official cookbook": "官方实践教程",
    "API concepts": "API 概念",
    "Probability & routing": "概率与路由",
    "Limitations · reviewed October 2, 2026":
      "已知局限 · 2026 年 10 月 2 日审阅",
    "Interactive evaluation explorer": "交互式评测浏览器",
    "Workflow integration": "工作流集成",
    "four datasets": "四个数据集",
    "Coding agents": "编码 agent",
    "Cookbooks & demos": "教程与演示",
    "Hugging Face · community": "Hugging Face · 社区",
    "TypeSafe · September 15, 2026": "TypeSafe · 2026 年 9 月 15 日",
    "Author PDF": "作者提供的 PDF",
    "Training mixture": "训练混合数据",
    "Evaluation archive": "评测运行归档",
  };
  return Object.entries(labels).reduce(
    (text, [source, translated]) => text.replace(source, translated),
    value,
  );
}
function provenance(resource) {
  return (
    resource.provenance ||
    (resource.category === "Papers"
      ? "preprint"
      : resource.category === "Foundations"
        ? "background"
        : "official")
  );
}
function renderResources() {
  const query = $("#resource-search").value.trim().toLocaleLowerCase();
  const filtered = resources.filter(
    (resource) =>
      (activeFilter === "All" || resource.category === activeFilter) &&
      `${resource.title} ${resource.by} ${resource.en} ${resource.zh} ${resource.category}`
        .toLocaleLowerCase()
        .includes(query),
  );
  $("#resource-list").innerHTML = filtered
    .map(
      (resource) =>
        `<article class="resource-row"><div class="resource-kind"><span class="resource-category">${icon(categoryIcons[resource.category])}${escapeHTML(t("filter" + resource.category))}</span><span class="resource-provenance">${escapeHTML(t(provenance(resource)))}</span></div><div class="resource-heading"><h3 class="resource-title"><a href="${escapeHTML(resource.url)}" target="_blank" rel="noopener noreferrer">${escapeHTML(resource.title)}</a></h3><p class="resource-subtitle">${escapeHTML(localizedMetadata(resource.by))}</p></div><p class="resource-description">${escapeHTML(resource[language])}</p><span class="resource-arrow" aria-hidden="true">${icon("external")}</span></article>`,
    )
    .join("");
  $("#result-count").textContent = t("resourceCount")(
    filtered.length,
    resources.length,
  );
  $("#empty-state").hidden = filtered.length !== 0;
  $("#model-evidence").hidden = activeFilter !== "Models";
}
function selectFilter(filter) {
  activeFilter = filter;
  document.querySelectorAll("[data-filter]").forEach((button) => {
    const selected = button.dataset.filter === filter;
    button.classList.toggle("active", selected);
    button.setAttribute("aria-pressed", String(selected));
  });
  renderResources();
}
function setLanguage(next) {
  language = next;
  document.documentElement.lang = language === "zh" ? "zh" : "en";
  document.title =
    language === "zh"
      ? "Awesome Jev — 论文、模型与工具"
      : "Awesome Jev — Papers, models and tools";
  for (const selector of [
    'meta[name="description"]',
    'meta[property="og:description"]',
    'meta[name="twitter:description"]',
  ]) {
    document.querySelector(selector).content = t("metaDescription");
  }
  for (const selector of [
    'meta[property="og:title"]',
    'meta[name="twitter:title"]',
  ]) {
    document.querySelector(selector).content = document.title;
  }
  document.querySelector('meta[property="og:locale"]').content =
    language === "zh" ? "zh_CN" : "en_US";
  document.querySelector('meta[property="og:locale:alternate"]').content =
    language === "zh" ? "en_US" : "zh_CN";
  document.querySelectorAll("[data-i18n]").forEach((element) => {
    element.innerHTML = t(element.dataset.i18n);
  });
  document.querySelectorAll("[data-i18n-placeholder]").forEach((element) => {
    element.placeholder = t(element.dataset.i18nPlaceholder);
  });
  document.querySelectorAll("[data-i18n-aria]").forEach((element) => {
    element.setAttribute("aria-label", t(element.dataset.i18nAria));
  });
  document
    .querySelectorAll("[data-language]")
    .forEach((button) =>
      button.setAttribute(
        "aria-pressed",
        String(button.dataset.language === language),
      ),
    );
  document.querySelectorAll("[data-filter]").forEach((button) => {
    button.innerHTML =
      icon(categoryIcons[button.dataset.filter]) +
      "<span>" +
      escapeHTML(t("filter" + button.dataset.filter)) +
      "</span>";
  });
  const repository =
    "https://github.com/reacher-z/Awesome-Jev/blob/main/";
  document.querySelector('[data-document="readme"]').href =
    repository + (language === "zh" ? "README.zh-CN.md" : "README.md");
  document.querySelector('[data-document="survey"]').href =
    repository +
    (language === "zh" ? "docs/survey.zh-CN.md" : "docs/survey.md");
  try {
    const pageURL = new URL(window.location.href);
    if (language === "zh") pageURL.searchParams.set("lang", "zh");
    else pageURL.searchParams.delete("lang");
    window.history.replaceState(null, "", pageURL);
  } catch {
    /* Language switching still works in restricted previews. */
  }
  renderCopyButton();
  clearTimeout(copyTimer);
  $("#copy-status").textContent = "";
  renderResources();
  renderCorpus();
}
document
  .querySelectorAll("[data-language]")
  .forEach((button) =>
    button.addEventListener("click", () =>
      setLanguage(button.dataset.language),
    ),
  );
document
  .querySelectorAll("[data-filter]")
  .forEach((button) =>
    button.addEventListener("click", () => selectFilter(button.dataset.filter)),
  );
document.querySelectorAll("[data-filter-link]").forEach((link) =>
  link.addEventListener("click", () => {
    $("#resource-search").value = "";
    selectFilter(link.dataset.filterLink);
  }),
);
$("#resource-search").addEventListener("input", renderResources);
document
  .querySelectorAll("form[role=search]")
  .forEach((form) =>
    form.addEventListener("submit", (event) => event.preventDefault()),
  );
$("#reset-filters").addEventListener("click", () => {
  $("#resource-search").value = "";
  selectFilter("All");
  $("#resource-search").focus();
});
document.addEventListener("keydown", (event) => {
  if (
    event.key === "/" &&
    !event.ctrlKey &&
    !event.metaKey &&
    !event.altKey &&
    !/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName) &&
    !document.activeElement.isContentEditable
  ) {
    event.preventDefault();
    $("#resource-search").focus();
    $("#resource-search").scrollIntoView({ block: "center" });
  }
});
$("#copy-code").addEventListener("click", async () => {
  const code = $("#quickstart-code").textContent;
  try {
    if (!navigator.clipboard) throw new Error("Clipboard unavailable");
    await navigator.clipboard.writeText(code);
    renderCopyButton("copied");
    $("#copy-status").textContent = t("copied");
  } catch {
    const range = document.createRange();
    range.selectNodeContents($("#quickstart-code"));
    const selection = window.getSelection();
    selection.removeAllRanges();
    selection.addRange(range);
    renderCopyButton("copyFailed");
    $("#copy-status").textContent = t("copyFailed");
  }
  clearTimeout(copyTimer);
  copyTimer = setTimeout(() => {
    renderCopyButton();
  }, 3000);
});

function normalizeSource(source) {
  const description =
    source.description || source.summary || source.abstract || "";
  return {
    title: source.title || source.name || "",
    url: safeURL(source.url || source.link || source.source_url),
    description:
      typeof description === "string" ? description : description.en || "",
    zh:
      source.description_zh ||
      source.summary_zh ||
      (typeof description === "object" ? description.zh : "") ||
      "",
    category: source.category || source.type || source.kind || "",
    year: source.year || "",
    status: source.status || source.review_status || source.screening || "",
    relation: source.relation || "",
    verification: source.verification_level || "",
    tags: [source.topic, ...(Array.isArray(source.tags) ? source.tags : [])].filter(Boolean).join(" "),
    curation: source.curation && safeURL(source.curation.evidence_url) ? {
      url: safeURL(source.curation.evidence_url),
      note: typeof source.curation.note === "string" ? source.curation.note : "",
      date: typeof source.curation.reviewed_at === "string" ? source.curation.reviewed_at.slice(0, 10) : "",
    } : null,
    by: source.authors || source.provider || source.source || "",
  };
}
function corpusMetadata(source) {
  const levels = {
    editorial_reviewed: "levelEditorial",
    content_screened: "levelContent",
    abstract_checked: "levelAbstract",
    metadata_only: "levelMetadata",
  };
  const relationLabels = {
    direct: ["Direct", "直接相关"],
    adjacent: ["Related", "邻近领域"],
    background: ["Background", "基础背景"],
  };
  const categoryLabels = {
    Datasets: "数据集",
    "Guides and evaluations": "指南与评测",
    Models: "模型",
    Papers: "论文",
    Projects: "项目",
    "Research foundations": "基础研究",
  };
  const category =
    language === "zh"
      ? categoryLabels[source.category] || source.category
      : source.category;
  const level = levels[source.verification]
    ? t(levels[source.verification])
    : source.status || source.verification;
  const relation =
    relationLabels[source.relation]?.[language === "zh" ? 1 : 0] ||
    source.relation;
  return [category, source.year, level, relation].filter(Boolean).join(" · ");
}
function curationDisclosure(source) {
  if (!source.curation) return "";
  const { url, note, date } = source.curation;
  return `<details class="corpus-curation"><summary>${escapeHTML(t("metadataCorrection"))}</summary><p>${escapeHTML(note)}</p><a href="${escapeHTML(url)}" target="_blank" rel="noopener noreferrer">${escapeHTML(t("primaryMetadata"))}${date ? ` · ${escapeHTML(date)}` : ""}</a></details>`;
}
function renderCorpus() {
  if (!$("#corpus-list")) return;
  if (!corpusLoaded) {
    $("#corpus-status").textContent = t("corpusLoading");
    return;
  }
  $("#corpus-count").textContent = corpusSources.length
    ? t("corpusCount")(corpusSources.length)
    : "";
  $("#corpus-audit-counts").textContent =
    Number.isFinite(corpusCounts.checked_sources) &&
    Number.isFinite(corpusCounts.metadata_only)
      ? t("corpusAuditCounts")(
          corpusCounts.checked_sources,
          corpusCounts.metadata_only,
        )
      : "";
  document.querySelectorAll("[data-count-key]").forEach((element) => {
    const count = corpusCounts[element.dataset.countKey];
    element.textContent = Number.isFinite(count)
      ? t("sourceCount")(count)
      : "—";
  });
  const query = $("#corpus-search").value.trim().toLocaleLowerCase();
  const filtered = corpusSources.filter((source) =>
    `${source.title} ${source.description} ${source.zh} ${source.category} ${source.tags} ${source.by} ${source.status} ${source.relation} ${source.verification} ${corpusMetadata(source)}`
      .toLocaleLowerCase()
      .includes(query),
  );
  $("#corpus-status").textContent = corpusSources.length
    ? t("corpusResults")(filtered.length, corpusSources.length)
    : t("corpusUnavailable");
  $("#corpus-list").innerHTML = filtered
    .slice(0, corpusLimit)
    .map(
      (source) =>
        `<article class="corpus-row"><div><h3><a href="${escapeHTML(source.url)}" target="_blank" rel="noopener noreferrer">${escapeHTML(source.title)}</a></h3><p>${escapeHTML(language === "zh" && source.zh ? source.zh : source.description)}</p>${curationDisclosure(source)}</div><div class="corpus-entry-meta" data-verification="${escapeHTML(source.verification)}">${escapeHTML(corpusMetadata(source))}<span aria-hidden="true">${icon("external")}</span></div></article>`,
    )
    .join("");
  if (corpusSources.length && !filtered.length)
    $("#corpus-list").innerHTML =
      `<p class="corpus-empty">${escapeHTML(t("corpusEmpty"))}</p>`;
  $("#corpus-more").hidden = filtered.length <= corpusLimit;
}
if ($("#corpus-search")) {
  $("#corpus-search").addEventListener("input", () => {
    corpusLimit = 24;
    renderCorpus();
  });
  $("#corpus-more").addEventListener("click", () => {
    corpusLimit += 24;
    renderCorpus();
  });
  fetch("./data/source-index.json")
    .then((response) => {
      if (!response.ok) throw new Error("Source index not available");
      return response.json();
    })
    .then((data) => {
      corpusCounts = !Array.isArray(data) && data.counts ? data.counts : {};
      const sources = Array.isArray(data)
        ? data
        : data.sources || data.resources || data.entries || [];
      corpusSources = sources
        .map(normalizeSource)
        .filter((source) => source.title && source.url);
    })
    .catch(() => {})
    .finally(() => {
      corpusLoaded = true;
      renderCorpus();
    });
}
const requestedLanguage = new URLSearchParams(window.location.search).get(
  "lang",
);
setLanguage(
  requestedLanguage && requestedLanguage.toLowerCase().startsWith("zh")
    ? "zh"
    : "en",
);
