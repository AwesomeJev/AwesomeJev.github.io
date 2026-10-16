#!/usr/bin/env node
// Build ordinary HTML from the same curated data used by the browser.
// No remote requests, clock-based dates, dependencies, or crawler-specific output.
import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { resolve, dirname } from 'node:path';
import { resources, translations } from '../site/catalog.mjs';
import { renderResource, escapeHTML as esc } from '../site/resource-view.mjs';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const origin = 'https://awesomejev.github.io';
const repo = 'https://github.com/reacher-z/Awesome-Jev';
const contentDate = '2026-10-16'; // Update only when curated page content changes.
const guide = JSON.parse(await readFile(resolve(root, 'data/search-guide.json'), 'utf8'));
const expansion = JSON.parse(await readFile(resolve(root, 'data/expansion-progress-2026-10-16.json'), 'utf8'));
const discoveryLocalization = JSON.parse(await readFile(resolve(root, 'data/discovery-translations.zh-CN.json'), 'utf8'));
if (discoveryLocalization.schema_version !== 1 || discoveryLocalization.language !== 'zh-CN' ||
    !discoveryLocalization.translations || typeof discoveryLocalization.translations !== 'object' || Array.isArray(discoveryLocalization.translations)) {
  throw new Error('Invalid Chinese discovery translations.');
}
const discoveryTranslations = discoveryLocalization.translations;
const template = await readFile(resolve(root, 'templates/index.html'), 'utf8');
// Stable URLs for unchanged bytes; changed data cannot reuse an older browser cache entry.
const assetURLs = Object.fromEntries(await Promise.all(
  ['app.js', 'catalog.mjs', 'resource-view.mjs', 'styles.css'].map(async name => {
    const bytes = await readFile(resolve(root, 'site', name));
    const digest = createHash('sha256').update(bytes).digest('hex').slice(0, 12);
    return [name, `/${name}?v=${digest}`];
  }),
));
const importMap = {imports: {
  '/catalog.mjs': assetURLs['catalog.mjs'],
  '/resource-view.mjs': assetURLs['resource-view.mjs'],
}};
const papers = resources.filter(row => row.category === 'Papers');
const categoryOrder = ['Papers','Models','Datasets','Projects','Tools','Evaluations','Guides and evaluations','Guides','Research foundations','Foundations'];
const relationLabels = {direct:['Directly related','直接相关'],adjacent:['Related field','邻近领域'],background:['Research background','研究背景']};
const evidenceLabels = {editorial_reviewed:['Editorially reviewed','编辑复核'],content_screened:['Content screened','正文筛查'],abstract_checked:['Abstract checked','摘要检查']};
const categoryLabels = {Papers:'论文',Models:'模型',Datasets:'数据集',Projects:'项目',Tools:'工具',Evaluations:'评测','Guides and evaluations':'指南与评测',Guides:'指南','Research foundations':'基础研究',Foundations:'基础研究'};
if (!Array.isArray(expansion.additions) || !Number.isInteger(expansion.accepted_new_sources) || expansion.accepted_new_sources !== expansion.additions.length || !Number.isInteger(expansion.target_new_sources) || expansion.target_new_sources < 1) throw new Error('Invalid expansion report counts.');
for (const row of expansion.additions) {
  if (['title','url','category','description'].some(key=>typeof row[key]!=='string' || !row[key].trim()) || !Object.hasOwn(relationLabels,row.relation) || !Object.hasOwn(evidenceLabels,row.verification_level)) throw new Error('Invalid expansion source metadata or evidence tier.');
  // Exact source text binds a translation to the reviewed wording. A changed
  // limitation must be translated again instead of silently reusing stale text.
  const translated = discoveryTranslations[row.description];
  if (!Object.hasOwn(discoveryTranslations, row.description) || typeof translated !== 'string' || !/[\u3400-\u9fff]/u.test(translated)) {
    throw new Error('Missing Chinese discovery description translation. Update data/discovery-translations.zh-CN.json.');
  }
  const url = new URL(row.url);
  if (!['https:','http:'].includes(url.protocol) || url.username || url.password) throw new Error('Invalid expansion source URL.');
}
if (new Set(expansion.additions.map(row=>row.url)).size !== expansion.additions.length) throw new Error('Duplicate expansion source URL.');
const categoryRank = category => categoryOrder.includes(category) ? categoryOrder.indexOf(category) : categoryOrder.length;
const discoveries = [...expansion.additions].sort((a,b)=>categoryRank(a.category)-categoryRank(b.category) || a.category.localeCompare(b.category,'en') || a.title.localeCompare(b.title,'en') || a.url.localeCompare(b.url,'en'));
const discoveryCategories = [...new Set(discoveries.map(row=>row.category))];
const discoveryCounts = Object.fromEntries(discoveryCategories.map(category=>[category,discoveries.filter(row=>row.category===category).length]));
if (!expansion.by_category || Object.keys(expansion.by_category).length!==discoveryCategories.length || discoveryCategories.some(category=>expansion.by_category[category]!==discoveryCounts[category])) throw new Error('Expansion category counts do not match accepted sources.');
const discoveryDate = String(expansion.updated_at || expansion.completed_at || expansion.generated_at || contentDate).slice(0,10);
const outputs = new Map();
const route = (language, section = '') => `${language === 'zh' ? '/zh/' : '/'}${section ? section + '/' : ''}`;
const t = (language, key) => translations[language][key] ?? translations.en[key];
const json = value => JSON.stringify(value).replace(/</g, '\\u003c');
const schemaTag = value => `<script type="application/ld+json">${json(value)}</script>`;
const identity = [
  {'@type':'Organization','@id':origin+'/#organization',name:'AwesomeJev',url:origin+'/',sameAs:[repo,'https://github.com/AwesomeJev'],description:'Independent community research collection; not affiliated with TypeSafe AI.'},
  {'@type':'WebSite','@id':origin+'/#website',name:'AwesomeJev',alternateName:'Awesome Jev',url:origin+'/',inLanguage:['en','zh-CN'],publisher:{'@id':origin+'/#organization'}}
];
function pageSchema(language, section, title, description, list) {
  const url = origin + route(language, section);
  const page = {'@type':list ? 'CollectionPage' : 'WebPage','@id':url+'#page',url,name:title,description,inLanguage:language==='zh'?'zh-CN':'en',isPartOf:{'@id':origin+'/#website'}};
  if (list) page.mainEntity = {'@type':'ItemList',numberOfItems:list.length,itemListElement:list.map((row, i)=>({'@type':'ListItem',position:i+1,name:row.title,url:row.url}))};
  else page.mainEntity = {'@type':'Article',headline:title,inLanguage:page.inLanguage,dateModified:guide.updated,author:{'@id':origin+'/#organization'},publisher:{'@id':origin+'/#organization'},mainEntityOfPage:{'@id':page['@id']},citation:[...new Set(guide[language].sections.flatMap(s=>s.paragraphs.flatMap(p=>p.sources.map(source=>source.url))))]};
  const graph = [...identity, page];
  if (section) graph.push({'@type':'BreadcrumbList',itemListElement:[{'@type':'ListItem',position:1,name:'Awesome Jev',item:origin+route(language)},{'@type':'ListItem',position:2,name:title,item:url}]});
  return {'@context':'https://schema.org','@graph':graph};
}
function alternates(section) {
  return `<link rel="alternate" hreflang="en" href="${origin+route('en',section)}" />\n<link rel="alternate" hreflang="zh-CN" href="${origin+route('zh',section)}" />\n<link rel="alternate" hreflang="x-default" href="${origin+route('en',section)}" />`;
}
function localizeHTML(html, language) {
  html = html.replace(/<([a-z][a-z0-9]*)\b([^>]*\bdata-i18n="([^"]+)"[^>]*)>[\s\S]*?<\/\1\s*>/g, (all,tag,attrs,key)=>typeof t(language,key)==='string'?`<${tag}${attrs}>${t(language,key)}</${tag}>`:all);
  html = html.replace(/<([a-z][a-z0-9]*)\b([^>]*\bdata-i18n-(placeholder|aria)="([^"]+)"[^>]*)>/g, (all,tag,attrs,kind,key)=>{
    const name = kind === 'aria' ? 'aria-label' : 'placeholder';
    return `<${tag}${attrs.replace(new RegExp(`${name}="[^"]*"`), `${name}="${esc(t(language,key))}"`)}>`;
  });
  return html;
}
function home(language) {
  const title = language === 'zh' ? 'Awesome Jev — 论文、模型与工具' : 'Awesome Jev — Papers, models and tools';
  const description = t(language,'metaDescription');
  let html = template.replace('<html lang="en">',`<html lang="${language==='zh'?'zh-CN':'en'}">`);
  const values = {TITLE:esc(title),CANONICAL:origin+route(language),STRUCTURED_DATA:schemaTag(pageSchema(language,'',title,description,resources)),PAPERS_URL:route(language,'papers'),PAPERS_LABEL:language==='zh'?'论文目录':'Research papers',DISCOVERIES_URL:route(language,'discoveries'),DISCOVERIES_LABEL:language==='zh'?'新增资源':'New resources',RESOURCE_ROWS:resources.map(row=>renderResource(row,language,translations)).join('\n'),RESOURCE_COUNT:esc(t(language,'resourceCount')(resources.length,resources.length)),NOSCRIPT_NOTE:language==='zh'?'所有精选资源已列在本页。启用 JavaScript 后可使用搜索与筛选；也可浏览独立论文目录。':'All curated resources are listed on this page. Enable JavaScript to search and filter, or browse the dedicated papers directory.'};
  values.IMPORT_MAP = `<script type="importmap">${json(importMap)}</script>`;
  values.APP_MODULE_URL = esc(assetURLs['app.js']);
  values.STYLESHEET_URL = esc(assetURLs['styles.css']);
  for (const [key,value] of Object.entries(values)) html=html.replaceAll(`{{${key}}}`,value);
  html=localizeHTML(html,language)
    .replace(/(<meta\s+(?:name="description"|property="og:description"|name="twitter:description")\s+content=")[^"]*("\s*\/>)/g,`$1${esc(description)}$2`)
    .replace(/(<meta\s+(?:property="og:title"|name="twitter:title")\s+content=")[^"]*("\s*\/>)/g,`$1${esc(title)}$2`)
    .replace(/(<meta property="og:url" content=")[^"]+/,`$1${origin+route(language)}`)
    .replace(/(<meta property="og:locale" content=")[^"]+/,`$1${language==='zh'?'zh_CN':'en_US'}`)
    .replace(/(<meta property="og:locale:alternate" content=")[^"]+/,`$1${language==='zh'?'en_US':'zh_CN'}`)
    .replace(/(data-language="(en|zh)")/g,(_,attr,code)=>`${attr} aria-current="${code===language?'page':'false'}"`)
    .replace(/href="\/guide\/" data-document="survey"/,`href="${route(language,'guide')}" data-document="survey"`);
  if(language==='zh')html=html.replace('href="https://github.com/reacher-z/Awesome-Jev/blob/main/README.md" data-document="readme"','href="https://github.com/reacher-z/Awesome-Jev/blob/main/README.zh-CN.md" data-document="readme"');
  return html;
}
function shell(language, section, title, description, body, list) {
  const isZh=language==='zh', pageURL=origin+route(language,section);
  return `<!doctype html>
<html lang="${isZh?'zh-CN':'en'}"><head>
<meta charset="utf-8" /><meta name="viewport" content="width=device-width,initial-scale=1" />
<title>${esc(title)} | Awesome Jev</title><meta name="description" content="${esc(description)}" />
<meta name="robots" content="index,follow,max-image-preview:large" /><link rel="canonical" href="${pageURL}" />
${alternates(section)}
<meta property="og:type" content="${section==='guide'?'article':'website'}" /><meta property="og:site_name" content="AwesomeJev" />
<meta property="og:title" content="${esc(title)}" /><meta property="og:description" content="${esc(description)}" /><meta property="og:url" content="${pageURL}" />
<meta property="og:locale" content="${isZh?'zh_CN':'en_US'}" /><meta property="og:image" content="${origin}/assets/social.png" /><meta name="twitter:card" content="summary_large_image" />
<link rel="icon" href="/favicon.svg" type="image/svg+xml" /><link rel="stylesheet" href="${assetURLs['styles.css']}" />
${schemaTag(pageSchema(language,section,title,description,list))}
</head><body><a class="skip-link" href="#main">${isZh?'跳转到正文':'Skip to content'}</a><div class="page-shell">
<header class="masthead"><a class="wordmark" href="${route(language)}"><span class="brand-mark" aria-hidden="true">aj</span>AwesomeJev.</a>
<nav class="main-nav" aria-label="${isZh?'主导航':'Main navigation'}"><a href="${route(language)}">${isZh?'资源索引':'Resources'}</a><a href="${route(language,'papers')}">${isZh?'论文':'Papers'}</a><a href="${route(language,'discoveries')}">${isZh?'新增资源':'New resources'}</a><a href="${route(language,'guide')}">${isZh?'研究指南':'Research guide'}</a><a href="${repo}">GitHub</a></nav>
<div class="language-switch"><a href="${route('en',section)}" lang="en" hreflang="en" aria-current="${isZh?'false':'page'}">EN</a><span>/</span><a href="${route('zh',section)}" lang="zh-CN" hreflang="zh-CN" aria-current="${isZh?'page':'false'}">中文</a></div></header>
<main id="main" class="document-main"><nav class="breadcrumbs" aria-label="${isZh?'当前位置':'Breadcrumb'}"><a href="${route(language)}">Awesome Jev</a><span aria-hidden="true"> / </span><span>${esc(title)}</span></nav>
<h1>${esc(title)}</h1><p class="document-deck">${esc(description)}</p>${body}</main>
<footer class="document-footer"><p>${isZh?'独立社区项目，与 TypeSafe AI 无隶属关系。':'Independent community project. Not affiliated with TypeSafe AI.'}</p><p><a href="${repo}">GitHub</a> · <a href="/references.bib">BibTeX</a> · <a href="${repo}/blob/main/LICENSE">MIT</a> · <a href="https://github.com/reacher-z">reacher-z</a></p></footer>
</div></body></html>\n`;
}
function guidePage(language) {
  const doc=guide[language], isZh=language==='zh';
  const toc=`<nav class="document-toc" aria-label="${isZh?'本页目录':'On this page'}"><ol>${doc.sections.map(s=>`<li><a href="#${esc(s.id)}">${esc(s.title)}</a></li>`).join('')}</ol></nav>`;
  const body=`<p class="document-date">${isZh?'更新':'Updated'} <time datetime="${guide.updated}">${guide.updated}</time> · <a href="${repo}/blob/main/docs/${isZh?'survey.zh-CN.md':'survey.md'}">${isZh?'完整研究综述':'Full research survey'}</a></p><p>${esc(doc.intro)}</p>${toc}<div class="prose">${doc.sections.map(s=>`<section id="${esc(s.id)}"><h2>${esc(s.title)}</h2>${s.paragraphs.map(p=>`<p>${esc(p.text)}${p.sources.length?' <span class="source-links">'+p.sources.map(source=>`<a href="${esc(source.url)}" rel="noopener noreferrer">${esc(source.label)}</a>`).join(' · ')+'</span>':''}</p>`).join('')}</section>`).join('')}</div><p><a href="${route(language,'papers')}">${isZh?'继续阅读：精选论文与版本':'Continue reading: selected papers and versions'} →</a></p>`;
  return shell(language,'guide',doc.title,doc.description,body);
}
function papersPage(language) {
  const isZh=language==='zh', title=isZh?'Jev 与类型化决策模型论文':'Jev and typed decision model papers';
  const description=isZh?'按版本日期整理的精选论文：评测、校准、路由、鲁棒性与模型架构，附原文和引用。':'Selected papers on evaluation, calibration, routing, robustness and decision-model architectures, with versioned primary sources and citations.';
  const body=`<p>${isZh?'本目录收录直接相关的预印本。日期对应所列版本；简介基于论文与摘要核查，不代表实验已复现。基础文献与模型、工具另见首页。':'This directory selects directly relevant preprints. Dates identify the linked versions; summaries draw on paper and abstract checks, without claiming experimental reproduction. Foundations, models and tools are listed on the homepage.'}</p><p class="document-date">${isZh?'最近整理':'Last curated'} <time datetime="${contentDate}">${contentDate}</time> · ${papers.length} ${isZh?'篇论文':'papers'} · <a href="/references.bib">BibTeX</a> · <a href="/papers.json">JSON</a></p><p><a href="${route(language,'guide')}">${isZh?'先读研究指南：接口、概率与评测':'Start with the research guide: interfaces, probabilities and evaluation'} →</a></p><div class="resource-list">${papers.map(row=>renderResource(row,language,translations)).join('\n')}</div>`;
  return shell(language,'papers',title,description,body,papers);
}
function discoveriesPage(language) {
  const isZh=language==='zh', labelIndex=isZh?1:0;
  const title=isZh?'新增资源目录':'New resources';
  const description=isZh?'按类别浏览新收录的项目、模型、数据集、指南与研究论文。':'Explore recently added projects, models, datasets, guides and research papers by category.';
  const categoryLabel=category=>isZh?(categoryLabels[category] || category):category;
  const categoryId=category=>'discovery-category-'+discoveryCategories.indexOf(category);
  const toc=discoveryCategories.length?`<nav class="document-toc" aria-label="${isZh?'按分类浏览':'Browse by category'}"><ul class="discovery-category-list">${discoveryCategories.map(category=>`<li><a href="#${categoryId(category)}">${esc(categoryLabel(category))} (${discoveryCounts[category]})</a></li>`).join('')}</ul></nav>`:'';
  const cards=discoveryCategories.map(category=>`<section id="${categoryId(category)}"><h2>${esc(categoryLabel(category))} (${discoveryCounts[category]})</h2><div class="resource-list">${discoveries.filter(row=>row.category===category).map(row=>{
    const retrieved=typeof row.retrieved_at==='string'?row.retrieved_at.slice(0,10):'';
    return `<article class="resource-row" data-category="${esc(row.category)}" data-relation="${esc(row.relation)}" data-verification-level="${esc(row.verification_level)}"><div class="resource-kind"><span class="resource-category">${esc(categoryLabel(row.category))}</span><span class="resource-provenance">${esc(relationLabels[row.relation][labelIndex])}</span></div><div class="resource-heading"><h3 class="resource-title"><a href="${esc(row.url)}" target="_blank" rel="noopener noreferrer">${esc(row.title)}</a></h3><p class="resource-subtitle">${isZh?'证据：':'Evidence: '}${esc(evidenceLabels[row.verification_level][labelIndex])}${retrieved?` · ${isZh?'抓取于':'Retrieved'} <time datetime="${esc(retrieved)}">${esc(retrieved)}</time>`:''}</p></div><p class="resource-description">${esc(isZh?discoveryTranslations[row.description]:row.description)}</p><span class="resource-arrow" aria-hidden="true">↗</span></article>`;
  }).join('\n')}</div></section>`).join('\n');
  const baseline=typeof expansion.baseline_commit==='string' && /^[a-f0-9]{40}$/.test(expansion.baseline_commit)?` <a href="${repo}/commit/${expansion.baseline_commit}">${expansion.baseline_commit.slice(0,7)}</a>`:'';
  const body=`<p class="document-date"><strong>${discoveries.length.toLocaleString('en-US')}</strong> ${isZh?'项新增来源':'added sources'} · <time datetime="${discoveryDate}">${discoveryDate}</time> · <a href="/data/expansion-progress.json">${isZh?'下载 JSON':'Download JSON'}</a></p><p>${isZh?'条目标明与 Jev 直接相关、邻近领域或背景研究。正文筛查与摘要检查不代表全文评审、质量背书或实验复现。':'Entries distinguish direct Jev resources, related methods and research background. Source-page and abstract checks do not imply full-paper review, endorsement or experimental reproduction.'}</p>${toc}<details class="verification-legend"><summary>${isZh?'核查与计数方法':'Verification and counting method'}</summary><p>${isZh?'本目录相对冻结版本新增，排除旧链接、重复正文和论文题名。基线：':'This directory excludes prior URLs, repeated evidence and duplicate paper titles. Baseline:'}${baseline || (isZh?'见 JSON':'see JSON')}.</p><p><a href="${repo}/blob/main/docs/reviews/expansion-2026-10-16.md">${isZh?'查看本轮审阅记录':'Read the expansion review'}</a> · <a href="${repo}/blob/main/docs/source-audit.md">${isZh?'证据等级说明':'Evidence-level definitions'}</a></p></details><p><a href="${route(language)}#corpus">${isZh?'搜索完整来源库':'Search the complete source corpus'} →</a></p>${cards || `<p>${isZh?'本轮尚无已接受的新增来源。':'No new sources have been accepted in this expansion yet.'}</p>`}`;
  return shell(language,'discoveries',title,description,body,discoveries);
}
for (const language of ['en','zh']) {
  outputs.set(`site${route(language)}index.html`,home(language));
  outputs.set(`site${route(language,'guide')}index.html`,guidePage(language));
  outputs.set(`site${route(language,'papers')}index.html`,papersPage(language));
  outputs.set(`site${route(language,'discoveries')}index.html`,discoveriesPage(language));
}
outputs.set('site/sitemap.xml',`<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n${['','guide','papers','discoveries'].flatMap(section=>['en','zh'].map(language=>`  <url><loc>${origin+route(language,section)}</loc><lastmod>${section==='guide'?guide.updated:section==='discoveries'?discoveryDate:contentDate}</lastmod>${['en','zh'].map(other=>`<xhtml:link rel="alternate" hreflang="${other==='zh'?'zh-CN':'en'}" href="${origin+route(other,section)}" />`).join('')}</url>`)).join('\n')}\n</urlset>\n`);
outputs.set('site/data/expansion-progress.json',JSON.stringify(expansion,null,2)+'\n');
outputs.set('site/references.bib',await readFile(resolve(root,'references.bib'),'utf8'));
outputs.set('site/papers.json',JSON.stringify({title:'Awesome Jev research papers',url:origin+'/papers/',updated:contentDate,scope:'Curated direct preprints; findings remain author-reported. No experimental reproduction implied.',papers},null,2)+'\n');
outputs.set('site/llms.txt',`# Awesome Jev\n\n> Independent, bilingual collection of Jev and typed decision model research, models, datasets and tools. Not affiliated with TypeSafe AI.\n\n## Main pages\n\n- [Resource collection](${origin}/): curated primary sources and verification labels.\n- [Research guide](${origin}/guide/): source-backed answers about Jev, typed decisions, probabilities and evaluation.\n- [Papers](${origin}/papers/): versioned preprints; findings remain author-reported.\n- [New resources](${origin}/discoveries/): new direct resources, related work and background research with evidence labels.\n- [中文](${origin}/zh/): Chinese collection and guide.\n\n## Source formats\n\n- [Guide and curated resources in Markdown](${origin}/llms-full.txt)\n- [Paper metadata](${origin}/papers.json)\n- [Expansion report](${origin}/data/expansion-progress.json)\n- [BibTeX](${origin}/references.bib)\n- [Repository](${repo})\n- [Verification methodology](${repo}/blob/main/docs/source-audit.md)\n\nThis optional file is a reading aid, not an indexing or ranking mechanism. Respect source versions and distinguish vendor claims, preprint findings, and independently reproduced evidence.\n`);
outputs.set('site/llms-full.txt',`# Awesome Jev\n\nIndependent community project, not affiliated with TypeSafe AI.\nCanonical website: ${origin}/\nCurated snapshot: ${contentDate}. Findings are author-reported; no model experiments reproduced here.\n\n# ${guide.en.title}\n\n${guide.en.intro}\n\n${guide.en.sections.map(s=>`## ${s.title}\n\n${s.paragraphs.map(p=>(p.text+' '+p.sources.map(source=>`[${source.label}](${source.url})`).join(' · ')).trimEnd()).join('\n\n')}`).join('\n\n')}\n\n# Curated resources\n\n${resources.map(row=>`## ${row.title}\n\n${row.category} · ${row.by}\n\n${row.en}\n\nPrimary source: ${row.url}`).join('\n\n')}\n`);
const check=process.argv.includes('--check');
let stale=0;
for (const [name,content] of outputs) {
  if (/\{\{[A-Z_]+\}\}/.test(content)) throw new Error(`Unresolved template value in ${name}`);
  const path=resolve(root,name);
  if(check){if(await readFile(path,'utf8').catch(()=>null)!==content){console.error(`Stale generated page: ${name}`);stale++;}}
  else {await mkdir(dirname(path),{recursive:true});await writeFile(path,content);}
}
if(stale)process.exitCode=1;
else console.log(`${check?'Checked':'Built'} ${outputs.size} static outputs; ${resources.length} curated resources, ${papers.length} papers, ${discoveries.length} new sources, ${[...outputs.keys()].filter(name=>name.endsWith('.html')).length} HTML pages.`);
