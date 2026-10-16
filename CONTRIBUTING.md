# Contributing to Awesome Jev

Thank you for helping keep this field guide useful and inspectable. English and Chinese contributions are welcome.

The canonical collection is [reacher-z/Awesome-Jev](https://github.com/reacher-z/Awesome-Jev). Please open [issues](https://github.com/reacher-z/Awesome-Jev/issues) and [pull requests](https://github.com/reacher-z/Awesome-Jev/pulls) there. [AwesomeJev/AwesomeJev.github.io](https://github.com/AwesomeJev/AwesomeJev.github.io) mirrors the tested source for the [website](https://awesomejev.github.io); maintainers synchronize the two repositories when publishing.

For collector refreshes, evidence tiers, bilingual updates and deployment, see the [maintenance guide](docs/maintenance.md).

## Add a resource

Open an issue or pull request with:

- A canonical public URL, title, author or organization, and publication date.
- Its category: direct research, evaluation, model, tool, recipe, or foundation.
- A short explanation of its relevance to typed decisions.
- What you checked: metadata, abstract, documentation, code, or an executed experiment.
- The model, paper, dataset, or code version when it changes the claim.
- A material limitation, and a code or data link if available.

Prefer the original paper, model card, author repository, or provider documentation. Use secondary indexes to discover those sources. Distinguish Jev-inspired implementations from official TypeSafe artifacts. Identify preprints, provider-reported results, and independently run experiments.

## Evidence quality

Keep schema validity, task quality, calibration, and system efficiency separate. Numerical comparisons need a workload, denominator, baseline configuration, and date. A leaderboard using private tests is not fully reproducible merely because its results are public.

Do not count search results, mirror URLs, different versions of the same paper, or failed requests as independently reviewed sources. The research corpus includes automated content screening; use the recorded review level rather than describing every entry as editorially reviewed.

## Local development

The website is static HTML, CSS, and JavaScript:

```sh
python3 -m http.server 8000 --directory site
```

Open `http://localhost:8000`. Check both languages, search, category filters, the source corpus, narrow-screen layout, and keyboard navigation after UI changes.

Run the repository checks before a pull request:

```sh
python3 scripts/validate.py
```

## Publication hygiene

Submit only public source material and original summaries. Keep API keys, `.env` files, local caches, account configuration, private URLs, and proprietary packages outside the repository. Third-party assets must carry the appropriate license and attribution. Font Awesome Pro assets must not be committed to this public repository.

## 中文说明

欢迎补充论文、模型、工具、数据与负面结果。请提供原始链接、日期或版本、与类型化决策的关系，以及实际核查的内容范围。区分官方声明、论文作者报告、自动筛查与亲自复现；不要将不同镜像或同一论文的多个版本重复计数。修改资源描述时，请同步中英文。

请统一向[资源主仓库 reacher-z/Awesome-Jev](https://github.com/reacher-z/Awesome-Jev)提交 issue 与 PR；组织仓库负责部署网站。两边保留同一份通过校验的源码，由维护者发布时同步，并非自动同步。

来源刷新、校验与发布流程见[维护指南](docs/maintenance.md)。
