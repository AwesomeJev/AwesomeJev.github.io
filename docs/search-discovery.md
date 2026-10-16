# Search discovery and AI-search readiness

Guidance checked against official documentation on **2026-10-16**. These changes make content easier to discover and inspect; they do not guarantee crawling, indexing, rankings, or citations in an AI answer. Search visibility and account-level settings must be checked separately from a successful deployment.

## Authoring and building the public pages

Edit the shared sources, then rebuild from the repository root:

```sh
node scripts/build_site.mjs
node scripts/build_site.mjs --check
```

The first command generates the public files. `--check` makes no changes and fails if a generated file is missing or differs from its source. The build uses local files only; it does not fetch sources or refresh verification dates.

| Content | Source to edit |
| --- | --- |
| Curated entries and interface translations | [site/catalog.mjs](../site/catalog.mjs) |
| Chinese discovery descriptions | [data/discovery-translations.zh-CN.json](../data/discovery-translations.zh-CN.json) |
| Homepage layout | [templates/index.html](../templates/index.html) |
| Shared resource-row rendering | [site/resource-view.mjs](../site/resource-view.mjs) |
| English and Chinese guide text and citations | [data/search-guide.json](../data/search-guide.json) |
| Bibliography | [references.bib](../references.bib) |
| Page generation, metadata, and sitemap rules | [scripts/build_site.mjs](../scripts/build_site.mjs) |

`site/app.js` enhances the browser interface; the resource catalog now belongs in `site/catalog.mjs`. Do not maintain a second copy of the entries in the application script.

The build adds content-hash URLs for the entry script, its imported modules and CSS. The homepage import map keeps browser-rendered entries consistent with its static HTML when the shared catalog changes; authors do not need to bump query versions by hand.

The Chinese discoveries page translates the resource descriptions as well as the navigation. Its translations are bound to the exact English summary, and missing or outdated mappings stop the build. Preserve the same source links, evidence tiers and limitations in both languages. Google determines page language from visible content; translating the navigation alone does not make the main content Chinese. [Google multilingual-site guidance](https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites)

Do not hand-edit the eight generated HTML pages: `/`, `/zh/`, `/guide/`, `/zh/guide/`, `/papers/`, `/zh/papers/`, `/discoveries/`, and `/zh/discoveries/`. The build also owns `site/sitemap.xml`, `site/references.bib`, `site/papers.json`, `site/llms.txt`, `site/llms-full.txt`, and the published `site/data/expansion-progress.json` copy. Change their source files or generator, rebuild, and include both source and output changes in the same review. Update the generator's `contentDate` or the guide's `updated` date only when the corresponding substantive content changes; a no-op scan does not justify a new date.

## Public content and crawlability

Serve the curated resource entries and guide text in the initial HTML, with normal links. JavaScript can enhance filtering and search. Google can render JavaScript, but recommends pre-rendering where useful because other crawlers may not execute it. Do not describe client-rendered content as inherently unindexable by Google. [Google JavaScript SEO guidance](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics)

The public guide is authored in [data/search-guide.json](../data/search-guide.json), with parallel English and Chinese content and paragraph-level source links. Keep those citations visible in the generated guide pages. Maintain the distinction between provider descriptions, author-reported studies, source screening, and experiments actually reproduced by this project.

Use stable language URLs, such as `/` and `/zh/`, and `/guide/` and `/zh/guide/`. Each translated page should serve its own language without requiring a button click, use a self-consistent canonical URL, and list reciprocal `hreflang` alternatives including itself. Keep the language switch usable as ordinary links. [Google localized-page guidance](https://developers.google.com/search/docs/specialty/international/localized-versions)

Keep an accurate XML sitemap at the site root, referenced by `robots.txt`. Include canonical first-party pages that should be searchable; external papers in the resource collection do not belong in this site's sitemap. Update `lastmod` when the page's substantive content changes, not whenever a collector or build runs. Google and Bing ignore the optional `priority` and `changefreq` fields. [Google sitemap guidance](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap) · [Bing sitemap guidance](https://blogs.bing.com/webmaster/2025/7/Keeping-Content-Discoverable-with-Sitemaps-in-AI-Powered-Search/)

Do not generate thousands of near-empty pages from the broad source corpus just to increase indexable URL counts. Curated explanations, transparent evidence notes, and useful navigation provide more value than mechanically repeating titles and links. [Google generative-AI optimization guidance](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)

## Structured data and answer-oriented writing

Structured data must describe what readers can actually see. A resource collection can use ordinary website/collection/list semantics; the explanatory guide can describe its real title, author or maintainer, language, sources, and update date. Do not invent reviews, ratings, qualifications, or evidence that the project did not produce. Valid markup is not a guarantee of a rich result. [Google structured-data policies](https://developers.google.com/search/docs/appearance/structured-data/sd-policies)

Question headings are useful when they answer readers' real questions. They do not imply special search eligibility. Google's FAQ rich-result feature was retired in May 2026; do not promise FAQ rich results from this guide. [Google documentation updates](https://developers.google.com/search/updates)

Google explicitly says it does not use `llms.txt` to improve visibility or ranking. Such a file may be maintained as an optional navigation aid for other tools, but it is not an indexing requirement or an AEO shortcut. There is no special structured-data type required for Google's generative search features. [Google AI optimization guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)

## Google: what an owner should check

Pages must meet ordinary Search requirements and be indexed with snippet eligibility to appear as supporting links in AI Overviews or AI Mode. The site's generative-AI inclusion control must also permit participation, as described below. [Google AI-feature requirements](https://developers.google.com/search/docs/appearance/ai-features)

The Search Console **Settings → Search generative AI** control defaults to inclusion; a child property can inherit a parent's setting. Check the effective setting rather than assuming a new manual opt-in is always necessary. This control is separate from ordinary Search inclusion and from AI-training controls. The project's inherited effective setting was confirmed in Search Console as **Current control: Include** on 2026-10-16. [Search generative AI control](https://support.google.com/webmasters/answer/16908024)

An owner can verify the exact `https://awesomejev.github.io/` URL-prefix property, inspect a live URL, submit the sitemap, and monitor indexing and search performance. Use the owner's actual verification file or tag; never add a placeholder verification token and call the site verified. Account verification and a submitted sitemap do not themselves prove indexing. [Search Console ownership verification](https://support.google.com/webmasters/answer/9008080) · [Google sitemap submission](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap#submit-sitemap)

**Observed project status, 2026-10-16:** Google Search Console ownership verification succeeded using the site's HTML verification file, and the inherited effective Search generative AI control is **Include**. Keep the verification file publicly accessible; do not record the owner's account name or email in this repository.

- The homepage's live test reported **URL is available to Google** and **Page can be indexed**.
- Each of the six canonical HTML pages—`/`, `/zh/`, `/guide/`, `/zh/guide/`, `/papers/`, and `/zh/papers/`—was submitted once and received **Indexing requested** confirmation and the message that the URL was added to a priority crawl queue. These are confirmed requests, not confirmed index inclusion; do not submit the same pages repeatedly to try to advance their queue position.
- The six-page `https://awesomejev.github.io/sitemap.xml` was submitted and the submission was acknowledged. Its Sitemaps report still showed **Couldn't fetch**, type **Unknown**, and **0 discovered pages** at the latest check. A separate live inspection of that exact URL succeeded: **Crawl allowed? Yes**, **Page fetch Successful**, inspected as **Google Inspection Tool smartphone**. A successful live fetch does not establish successful sitemap processing or invalidate the report's unresolved failure. Recheck processing later; no site-side defect has been established from these observations.

**Follow-up confirmed on 2026-10-16:** URL Inspection for the canonical homepage `https://awesomejev.github.io/` now reports **URL is on Google** and **Page is indexed**. This is index-inclusion evidence for the homepage only, not confirmation for the other five pages, a ranking position, or an AI-answer citation. The sitemap report still showed its earlier retrieval failure when rechecked; the two observations are recorded separately.

Ownership verification, an inclusive AI control, successful live tests, and queued requests do not establish indexing or appearance in an AI answer. Record subsequent processing results separately instead of replacing these observations with an assumption of success.

## Bing and IndexNow

For normal discovery, retain crawlable internal links and a root sitemap referenced in `robots.txt`. Bing Webmaster Tools can verify sitemap processing and indexing through an owner account. Accurate modification dates matter; a fresh build timestamp is not evidence that page content changed. [Bing sitemap guidance](https://blogs.bing.com/webmaster/2025/7/Keeping-Content-Discoverable-with-Sitemaps-in-AI-Powered-Search/)

IndexNow is an optional change-notification protocol. It requires a valid key and a UTF-8 verification file on the same host as the submitted URLs. A root-level key file covers the host; a key hosted in a subdirectory covers only the corresponding URL prefix. Submit only this site's added, changed, or removed page URLs, not the external source URLs collected in its ledgers. A `200` response means receipt, and `202` means key verification is pending; neither guarantees crawling or indexing. [IndexNow protocol](https://www.indexnow.org/documentation) · [Bing's IndexNow setup](https://www.bing.com/indexnow/IndexNowView/IndexNowGetStartedView)

**GitHub Pages compatibility is an implementation inference:** GitHub Pages serves static repository files, so it can serve the required verification file. A separate post-deployment process could then submit changed first-party URLs. This does not mean GitHub Pages automatically enables IndexNow for this site. Verify the key file is live before making any submission. [GitHub Pages hosting](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages) · [IndexNow verification](https://www.indexnow.org/documentation)

**Observed project status, 2026-10-16:** Bing Webmaster Tools verification is blocked at the owner's passkey interaction and is not confirmed. IndexNow received one POST containing the six canonical page URLs: `/`, `/zh/`, `/guide/`, `/zh/guide/`, `/papers/`, and `/zh/papers/`. The response was **HTTP 202: key validation pending**. This confirms receipt pending key validation, not completed verification, crawling, or indexing. No automatic retry was made.

**Later release receipt, 2026-10-16:** after publishing `67edcc3`, one additional POST notified IndexNow of the four changed HTML pages (`/`, `/zh/`, `/papers/`, `/zh/papers/`). It returned **HTTP 200**, confirming successful receipt. This supersedes the earlier pending-validation status for this later notification, but does not prove indexing or Bing Webmaster Tools account verification. The two unchanged guide pages were not resubmitted.

For future content changes, [scripts/submit_indexnow.py](../scripts/submit_indexnow.py) defaults to a local dry run with no network requests:

```sh
python3 scripts/submit_indexnow.py
```

After deploying actual changes, select the changed canonical pages with repeatable `--url` arguments. Inspect that selection without `--submit` first. The explicit submission command verifies the live proof file and selected pages, then sends one POST:

```sh
python3 scripts/submit_indexnow.py --url https://awesomejev.github.io/guide/
python3 scripts/submit_indexnow.py --submit --url https://awesomejev.github.io/guide/
```

These are maintenance examples, not a request to resubmit an unchanged page. Omitting `--url` selects all current sitemap pages; use an explicit changed-page selection for subsequent releases. Record the actual response each time; do not use repeated notices to bypass pending validation or rate limits.

## OpenAI search crawlers

`OAI-SearchBot` is the relevant crawler for discovery in ChatGPT search. OpenAI recommends allowing it in `robots.txt` and not blocking its published IP ranges at the hosting layer. `GPTBot` has a separate training purpose, and its setting is independent. `ChatGPT-User` is for user-triggered visits, not the search-index control. Do not conflate these agents or change a training preference merely to enable search discovery. [Official OpenAI crawler documentation](https://developers.openai.com/api/docs/bots)

An unrestricted public `User-agent: *` rule already permits compliant search crawlers unless a more specific rule overrides it. A public HTTP response and a permissive robots file establish accessibility, not that OpenAI or another service has indexed or selected the page.

## Release checks

- Run `node scripts/build_site.mjs --check` after generating pages; source changes and generated outputs must agree.
- Inspect the fetched HTML without JavaScript: important headings, explanations, resource links, and citations should be present.
- Confirm each language page returns HTTP 200 with the intended language, title, canonical, and reciprocal alternatives.
- Check sitemap URLs, actual modification dates, and the live `robots.txt` response.
- Check JSON-LD against visible content and avoid unsupported claims about search features.
- Keep publication, search-engine submission, index inclusion, and observed traffic as separate statuses.

## 中文说明

优先把精选资源、指南正文和引用直接写入静态 HTML，让 JavaScript 只增强搜索与筛选。英文和中文使用独立可访问的 URL、相符的 canonical 和互相指向的 `hreflang`；sitemap 只列本站规范页面，更新时间应对应内容实质变化。

维护时修改 `site/catalog.mjs` 中的共享资源与翻译、`templates/index.html` 首页模板、`data/search-guide.json` 双语指南或根目录 `references.bib`，再执行 `node scripts/build_site.mjs`，并用 `node scripts/build_site.mjs --check` 检查一致性。不要直接编辑八个生成页面、sitemap、站点引用副本、论文 JSON 或 `llms` 文件；`site/app.js` 只负责浏览器交互，不再保存另一份资源目录。

这些措施改善可抓取性，不保证收录、排名或 AI 引用。Google 明确表示 `llms.txt` 不提升其排名；问答式正文也不意味着 FAQ 富结果。Search Console 的生成式 AI 控制默认包含，但子属性可能继承上级设置。截至 2026-10-16，Google 站点所有权已通过 HTML 文件验证，控制界面也已确认继承后的有效设置为 **Current control: Include**。保留公开验证文件，不在仓库记录账号姓名或邮箱。

Google 首页实时测试显示可访问、可索引；六个规范 HTML 页面 `/`、`/zh/`、`/guide/`、`/zh/guide/`、`/papers/`、`/zh/papers/` 均各提交一次，并分别收到 **Indexing requested** 确认，已加入优先抓取队列，不代表已收录。六页 sitemap 已提交并收到提交确认，但最近一次 Sitemaps 报表仍显示 **Couldn't fetch／Unknown／发现 0 页**。对同一个 sitemap URL 的独立实时测试则显示允许抓取、抓取成功，由 Google Inspection Tool smartphone 执行。实时测试成功不等于 sitemap 已处理成功，也不能覆盖报表的未解决状态；后续需复查，当前观察尚未确立本站存在需修复的缺陷。

Bing 验证停在所有者的通行密钥交互步骤，尚未确认完成。IndexNow 已通过一次 POST 提交上述六个规范页面 URL，返回 **HTTP 202，密钥验证待完成**；这不代表已验证、已抓取或已收录，没有自动重试。脚本默认 dry run，不发网络请求；未来部署实质变更后，用 `--url` 选择变更页面，核对预览，再显式使用 `--submit` 发送一次通知。不要重复提交未变化页面，也不要提交外站论文链接。OpenAI 搜索使用 `OAI-SearchBot`，与用于训练的 `GPTBot` 相互独立。所有外部验证、提交和收录状态都应以实际结果记录，不能由本地文件推断。

**后续确认（2026-10-16）：** Google URL 检查现已明确显示规范首页 `https://awesomejev.github.io/` 为 **URL is on Google／Page is indexed**。这一确认只适用于首页，不代表另外五页、排名或 AI 回答引用已经确认；sitemap 报表复查仍保留此前的读取失败状态，两者分开记录。

**后续通知（2026-10-16）：** 发布 `67edcc3` 后，仅将四个实际改变的 HTML 页面（`/`、`/zh/`、`/papers/`、`/zh/papers/`）通过一次 IndexNow POST 通知，返回 **HTTP 200**，确认已接收。未改变的两篇指南没有重复提交；这一回执仍不代表已收录或 Bing 站长账号验证完成。

## Expansion release follow-up

On 2026-10-16, release `f8194d4` published the English and Chinese `/discoveries/` directories with 655 verified-depth additions and expanded the sitemap to eight canonical pages. One IndexNow POST for the eight changed pages returned **HTTP 200**, confirming receipt, not index inclusion.

The Google URL Inspection request for `https://awesomejev.github.io/discoveries/` returned **Quota Exceeded** and was not accepted. The Chinese directory was not submitted after that service limit. Retry only after the quota resets; do not switch accounts or repeatedly submit to try to bypass the limit. The new directories remain reachable through ordinary internal links and the sitemap. This does not alter the earlier confirmed indexing of the homepage or turn the two new directories into confirmed indexed pages.

**中文：** `f8194d4` 已发布包含655项新增来源的中英文目录，sitemap扩为八页；八个更新页面通过一次IndexNow通知返回HTTP 200。Google对英文新增目录的手动索引请求返回“Quota Exceeded”，未受理；因此未再提交中文目录。待服务配额重置后再申请，保持普通站内链接与sitemap发现入口；首页已收录的确认不等于这两个新目录也已收录。

**Subsequent release receipt, 2026-10-16:** `d640802` added 58 sources and four curated promotions; `00e33fe` added six direct preprints and Chinese descriptions for all 719 discovery entries. After both releases were live, one IndexNow POST notified only the four substantively changed pages: `/`, `/zh/`, `/discoveries/`, and `/zh/discoveries/`. The response was **HTTP 200**. The unchanged paper and guide pages were not submitted again. This records notification receipt, not indexing or a completed Bing account verification; no further Google indexing request was made while its quota limit remained unresolved.

**后续通知（2026-10-16）：** `d640802` 新增58项来源，`00e33fe` 再增6篇直接相关预印本，并补齐719项新增资源的中文简介。确认上线后，仅将两次发布中实质变化的四页（首页、中文首页、两种语言的新增目录）通过一次 IndexNow POST 通知，返回 **HTTP 200**。未重复提交内容未变的论文和指南页；这一结果仍只表示接收通知，不代表收录或 Bing 账号验证完成。Google 配额问题未解决期间未再申请索引。

**Implementation and guide release, 2026-10-16:** after `d022f30` deployed, one IndexNow POST for eight substantively changed canonical pages returned **HTTP 200**. Both homepages and paper directories gained three curated studies, both guides gained the table/evidence diagnostic section, and both discovery directories gained two implementation repositories and more specific summaries. Live checks confirmed 78 curated entries, 35 selected papers, 43 bibliography entries, and 721 discoveries in each language. This is a publication and notification record; it adds no new claim about Google indexing or Bing account verification.

**实现与指南更新（2026-10-16）：** `d022f30` 部署后，八个正文均有实质变化的规范页面通过一次 IndexNow 通知返回 **HTTP 200**。线上已核对78项精选、35篇精选论文、43条书目及每种语言721项新增资源；首页、论文目录、指南和新增目录均有对应内容更新。此处记录发布与通知结果，不新增 Google 收录或 Bing 账号验证成功的主张。

**Confidence and tool-verification release, 2026-10-16:** `714c006` published six direct papers and four author-linked artifacts, bringing the reviewed expansion to 731 sources and the curated collection to 84 entries, including 41 papers and 49 bibliography entries. One IndexNow POST for the eight substantively changed canonical pages returned **HTTP 200** after deployment. A separate read-only Search Console check still showed `/sitemap.xml` as **Unknown / Couldn't fetch / 0 discovered pages**, with no last-read value. No further sitemap or manual indexing submission was made during that check; the earlier homepage indexing confirmation and the unresolved sitemap report remain separate observations.

**置信度与工具核验更新（2026-10-16）：** `714c006` 已发布6篇直接论文和4项作者配套资源，累计731项新增来源、84项精选（41篇论文、49条书目）。部署后八个实质变化页面通过一次 IndexNow 通知返回 **HTTP 200**。另行只读复查 Search Console 时，sitemap 仍为 **Unknown／Couldn't fetch／发现0页**，最后读取时间为空；该次复查没有重复提交 sitemap 或手动索引请求，不能把之前首页已收录的确认解释为 sitemap 已处理成功。

**Domain-study release, 2026-10-16:** `ca36ed7` added eight papers and six whole companion resources, reaching 745 discoveries, 92 curated entries, 49 selected direct papers and 57 bibliography entries. After successful deployment and live bilingual checks, one IndexNow POST for all eight substantively changed canonical pages returned **HTTP 200**. Updates include domain studies, their release limitations, the proposed confidence-transfer protocol and the newly verified model-note date. This receipt does not establish indexing, ranking or AI-answer inclusion; the previously recorded Search Console sitemap status was not rechecked or replaced in this release.

**领域研究更新（2026-10-16）：** `ca36ed7` 新增8篇论文与6项完整配套资源，达到745项新增、92项精选、49篇直接论文和57条书目。部署与双语线上核对通过后，八个实质变化页面通过一次 IndexNow 通知返回 **HTTP 200**。新增领域研究、发布范围说明和建议的置信度迁移流程，模型说明核验日期也已更新。通知回执不等于收录、排名或AI引用；本次没有重查或改写此前的 Search Console sitemap 状态。

**Ordinal-scale and visual research release, 2026-10-16:** `6cfb02d` added three direct preprints and two whole author artifacts, reaching 750 discoveries, 95 curated resources, 52 selected direct papers and 60 bibliography entries. Both repositories passed CI and the website deployment succeeded; one live check confirmed all eight HTML pages and seven supporting artifacts matched the published commit. After that check, one IndexNow POST for the eight substantively changed pages returned **HTTP 200**. The bilingual guide gained an ordinal-label diagnostic and the repository survey distinguishes three efficiency denominators. This records publication and notification receipt, not new search indexing, ranking or AI citations. No Google or Bing account action was attempted for this release.

**有序量表与视觉研究更新（2026-10-16）：** `6cfb02d` 新增3篇直接论文和2项完整作者资源，累计750项新增来源、95项精选、52篇直接论文及60条书目。两个仓库CI与网站部署成功，线上八个HTML页面和七项配套文件均与提交字节一致。核对后，对八个实质变化页面发送一次 IndexNow 通知，返回 **HTTP 200**。双语指南补充有序标签诊断，仓库综述新增三类效率指标的分母对照。此处确认发布与通知，不新增收录、排名或AI引用主张；本轮未操作 Google 或 Bing 账号。

**Companion and reproduction-guide release, 2026-10-16:** `225dc54` published two distinct companion resources, reaching 752 discoveries and 97 curated entries; the 52 selected direct papers and 60 bibliography entries were unchanged. Thirteen existing companion links and one navigation-only author site were added to the README without increasing source counts. Both guides gained a reproduction-scope section. After both repository checks, Pages deployment and one 15-target live parity check succeeded, one IndexNow POST for the six substantively changed pages (`/`, `/zh/`, `/guide/`, `/zh/guide/`, `/discoveries/`, `/zh/discoveries/`) returned **HTTP 200**. The unchanged paper pages were not submitted. This is receipt of a change notification, not evidence of new indexing or AI citations; no Google or Bing account action was performed.

**配套材料与复现指南更新（2026-10-16）：** `225dc54` 发布两项独立配套资源，累计752项新增来源、97项精选；直接论文52篇、书目60条保持不变。README补齐13个既有配套链接及一个仅用于导航的作者论文站，未重复计数；双语指南新增复现范围说明。双仓检查、部署及15项线上一致性核验通过后，仅对首页、指南、新增目录的中英文六页发送一次 IndexNow 通知，返回 **HTTP 200**。内容未变的论文页没有再次提交；此回执不证明新收录或AI引用，本轮未操作 Google 或 Bing 账号。

**Security-measurement release, 2026-10-16:** `bb24adb` added one JevAdvBench implementation, reaching 753 discoveries, and promoted the already-known Just Ask Jev paper into the curated selection without counting it as a new source. The collection now has 99 curated resources, 53 selected papers and 61 bibliography entries. Both guides gained a comparison of attack outcomes and denominators. Both repository checks and Pages deployment succeeded; one 15-target live check matched all eight HTML pages and seven supporting artifacts to the exact commit. A single IndexNow POST for the eight substantively changed canonical pages returned **HTTP 200**. This confirms notification receipt, not new index inclusion, ranking or AI citations. No Google or Bing account operation was attempted.

**安全评测指标更新（2026-10-16）：** `bb24adb` 新增一个JevAdvBench代码项目，扩展资源达到753项；将原已收录的Just Ask Jev补入精选，不重复计作新来源。当前为99项精选、53篇精选论文、61条书目，双语指南新增攻击结果与分母对照。双仓检查、Pages部署和15项目标的线上字节核对均通过；八个实质变化页面经一次 IndexNow 通知返回 **HTTP 200**。此处只确认接收通知，不证明新增收录、排名或AI引用；本轮未操作 Google 或 Bing 账号。

**Classifier and language comparison release, 2026-10-16:** `9f81b37` promoted three already-known papers and added one distinct Turkish decision checkpoint, reaching 103 curated resources, 56 selected papers, 64 bibliography entries and 754 discoveries. The bilingual guide now separates task-label access, readout/fine-tuning conditions and language-label provenance. Five display annotations preserve the underlying source evidence. After successful deployment, one 17-target live check matched all eight HTML pages and supporting data/modules to the exact commit. One IndexNow POST for the eight substantively changed canonical pages returned **HTTP 200**. This is notification receipt, not indexing or AI-answer inclusion; no Google or Bing account action was performed.

**分类器与语言比较更新（2026-10-16）：** `9f81b37` 将三篇既有论文补入精选，并新增一个独立土耳其语决策检查点，累计103项精选、56篇论文、64条书目及754项新增来源。双语指南区分任务标签、读出／微调与语言标签来源；五项展示注释保留原证据。成功部署后17项目标的线上字节核对通过，八个实质变化页面经一次 IndexNow 通知返回 **HTTP 200**。此回执不代表收录或AI引用，本轮未操作 Google 或 Bing 账号。

### Pages artifact names during retries

The original [deployment run](https://github.com/AwesomeJev/AwesomeJev.github.io/actions/runs/38907985608) uploaded its artifact, but the deployment step reported no matching artifact. A same-run retry uploaded a second artifact with the same name and failed on multiple matches. A [fresh manual run](https://github.com/AwesomeJev/AwesomeJev.github.io/actions/runs/38908553219) successfully deployed the same `9f81b37` commit; the site content was unchanged during recovery.

The single-job workflow now supplies the same `github-pages-${{ github.run_id }}-${{ github.run_attempt }}` value to the upload action’s `name` and the deployment action’s `artifact_name`. The run identifier remains stable on a retry while the attempt increases, so the deployment step selects only that attempt’s upload. This addresses the observed naming collision; it does not guarantee immediate artifact metadata visibility. If upload and deployment are later split into separately retried jobs, pass the upload’s chosen name through a job output. [Pinned action inputs and context evidence](../data/pages-artifact-name-review-2026-10-16.json).

**中文：** 原部署先因未找到已上传文件失败，同一运行重试又上传了同名文件，随后因匹配到两份而失败；新建运行已成功部署同一提交。现将上传与部署的文件名统一包含运行编号和重试次数，避免旧尝试的文件重名。此改动处理重名问题，不承诺消除平台元数据延迟；若以后拆分上传和部署作业，应传递实际上传名称。
