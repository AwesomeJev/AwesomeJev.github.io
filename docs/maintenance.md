# Maintaining Awesome Jev

[Contributing](../CONTRIBUTING.md) · [Source audit](source-audit.md) · [Source ledgers](../data/README.md)

The site has two layers: an editorial selection in [site/app.js](../site/app.js), and a searchable source index generated from the public ledgers. A new scanned source does not automatically belong in the editorial selection.

## Repository roles

| Destination | Purpose |
| --- | --- |
| [reacher-z/Awesome-Jev](https://github.com/reacher-z/Awesome-Jev) | Main resource collection and the destination for issues and pull requests. |
| [awesomejev.github.io](https://awesomejev.github.io) | Published website. |
| [AwesomeJev/AwesomeJev.github.io](https://github.com/AwesomeJev/AwesomeJev.github.io) | Deployment mirror serving GitHub Pages. |

Keep both repositories on the same tested source snapshot. Synchronization is a maintainer action; there is no automatic repository-mirroring workflow.

## Refresh the evidence

Run these commands from the repository root. Collector options below were checked against their actual `--help` output. Collection makes public network requests and replaces the default output ledgers; inspect the resulting changes before committing.

```sh
python3 scripts/collect_ecosystem.py --workers 12 --max-depth 1
python3 scripts/collect_research.py --target 0 --with-openalex --workers 8
python3 scripts/build_source_index.py
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

The ecosystem collector writes `data/ecosystem-sources.jsonl`, its summary, and a separate exclusion ledger. `--resume` reuses previously retrieved dependency records and rechecks their relevance; it is not a fresh network retrieval of every dependency. Use the normal command for a new retrieval snapshot.

The research collector writes `data/research-sources.jsonl`. `--target 0` keeps all qualifying distinct results rather than imposing a numerical target. `--with-openalex` supplements Hugging Face discovery with older scholarly work. Raw API responses are cached in the operating system's temporary area, outside this repository. To repeat screening against the existing cache:

```sh
python3 scripts/collect_research.py --offline --target 0 --with-openalex
```

The index builder deduplicates the ledgers and regenerates `site/data/source-index.json`, `data/source-counts.json`, and `site/data/source-badge.json`. Do not edit their counts by hand. To check that the generated index is current without rewriting it:

```sh
python3 scripts/build_source_index.py --check
```

Retain document identifiers when normalizing URLs: OpenReview's `id` and CiteSeer's `doi` are content identifiers, not tracking parameters. Preserve retrieval dates and hashes; reusing cached content must not become a claim that it was fetched again.

## Keep the verification tiers precise

| Recorded tier | What it means |
| --- | --- |
| `metadata_only` | Discovered or identified, without a successful substantive content check. Excluded from checked counts. |
| `abstract_checked` | Original abstract screened through Hugging Face or reconstructed from OpenAlex metadata. Neither full-paper review nor necessarily a fetched publisher page. |
| `content_screened` | Retrieved README, model card, dataset card or web-page text passed explicit automated relevance rules. An abstract landing page is not a full paper. |
| `editorial_reviewed` | A documented, focused editorial review of the source. It does not by itself mean experimental reproduction. |

Checked-source totals measure distinct documents under these rules. They do not measure independent studies or manually read papers. Preserve the distinction between provider claims, paper-reported results, and experiments actually run by this project. Record direct, adjacent and background relationships separately.

## Maintain the editorial collection

For a promoted resource, read the original source, pin the relevant version, state its purpose and a material limitation, and verify any license or access label. Synchronize its English and Chinese descriptions across `README.md`, `README.zh-CN.md`, and `site/app.js`. Add scholarly metadata to `references.bib`; update survey or audit prose only when the new evidence changes it.

Review the site locally after interface changes:

```sh
python3 -m http.server 8000 --directory site
```

Check both languages, search, category filters, source-tier labels, keyboard focus and a narrow viewport. The curated cards and large source browser serve different purposes; do not silently promote the entire scanned corpus into an endorsed reading list.

## Review and publish

[Repository CI](../.github/workflows/ci.yml) checks repository integrity in both repositories. Send proposed changes to the [main collection](https://github.com/reacher-z/Awesome-Jev). The [automated PR review](../.github/workflows/pr-review.yml) comments on bounded patches and provenance fields. It is deterministic assistance, not human scholarly review, verification of linked claims, or approval to merge. Keep its privileged workflow restricted to trusted base-branch logic: it must not check out or execute pull-request code.

After merging and testing `main`, maintainers publish the same commit to both remotes. In the maintainer checkout, `origin` points to `reacher-z/Awesome-Jev` and `awesomejev` points to `AwesomeJev/AwesomeJev.github.io`; confirm those destinations before using these commands:

```sh
git push origin main
git push awesomejev main
```

Configure Pages in the deployment repository to use GitHub Actions. The [Pages workflow](../.github/workflows/pages.yml) responds to a push to `main` or a manual dispatch, but its deployment job explicitly runs only when `github.repository` is `AwesomeJev/AwesomeJev.github.io`. It validates the publication and uploads only `site/`. Verify that both remote `main` branches identify the same commit, inspect CI in both repositories, and inspect the deployment result and live bilingual views. A local preview or a successful validation run is not evidence that deployment completed.

## Public-source and license boundaries

Collect only public resources with public, unauthenticated requests. Keep private transcripts, credentials, local account configuration, machine-specific paths and raw response caches out of commits. Before publication, inspect the staged files and commit author identity; use the project's shared public identity rather than a private email address. Do not copy full copyrighted articles or abstracts into the ledger.

Preserve the individual licenses of third-party resources. A repository license does not relicense linked papers, datasets or models. The bundled DM Sans, Instrument Serif and IBM Plex Mono fonts carry SIL Open Font License notices; the icon subset is Font Awesome **Free**, with its included license. Keep those notices and source versions with the assets. Do not add Font Awesome Pro files or proprietary font packages to this public repository.

## 中文说明

维护顺序是：刷新公开来源清单 → 生成网站索引与计数 → 运行校验和回归测试 → 同步中英文精选内容 → 检查暂存区后发布。`--resume` 与 `--offline` 会复用已有材料，不能写成全部来源重新抓取。

[reacher-z/Awesome-Jev](https://github.com/reacher-z/Awesome-Jev) 是资源主仓库，也是 issue 和 PR 的统一入口；[组织仓库](https://github.com/AwesomeJev/AwesomeJev.github.io) 是网站部署镜像。维护者将验证通过的同一个 `main` 提交推送到 `origin` 与 `awesomejev`，并核对两边提交一致；当前没有自动镜像同步。

自动正文筛查、摘要检查、编辑复核和亲自复现是不同层级。PR 自动评论不等于学术审查，也不批准合并。CI 在两个仓库运行，Pages 部署 job 仅允许组织部署仓库执行、只发布 `site/`；完成后检查两边 Actions 与线上双语页面。

只使用公开来源，不提交密钥、私人对话、个人路径或原始缓存。保留第三方字体、图标、模型与数据的许可边界，不将商业受限资源描述为可任意使用的开源资源。
