export const escapeHTML = value => String(value ?? "").replace(/[&<>"']/g, char => ({"&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#39;"})[char]);
const icon = name => `<svg class="icon" aria-hidden="true"><use href="/assets/fontawesome/icons.svg#${name}"></use></svg>`;
const categoryIcons={Papers:"paper",Models:"foundation",Tools:"code",Datasets:"foundation",Evaluations:"evaluation",Guides:"guide",Foundations:"foundation"};
function localizedMetadata(value, language) {
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
        : "community")
  );
}
export function renderResource(resource, language, translations) {
 const t=key=>translations[language][key] ?? translations.en[key] ?? key;
 return `<article class="resource-row"><div class="resource-kind"><span class="resource-category">${icon(categoryIcons[resource.category])}${escapeHTML(t("filter" + resource.category))}</span><span class="resource-provenance">${escapeHTML(t(provenance(resource)))}</span></div><div class="resource-heading"><h3 class="resource-title"><a href="${escapeHTML(resource.url)}" target="_blank" rel="noopener noreferrer">${escapeHTML(resource.title)}</a></h3><p class="resource-subtitle">${escapeHTML(localizedMetadata(resource.by, language))}</p></div><p class="resource-description">${escapeHTML(resource[language])}</p><span class="resource-arrow" aria-hidden="true">${icon("external")}</span></article>`;
}
