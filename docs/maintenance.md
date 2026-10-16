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

## Twice-daily source scans

The [Scan public sources workflow](../.github/workflows/scan-sources.yml) is configured for **09:17 and 21:17, America/Los_Angeles**, every day (`17 9,21 * * *`). The named timezone follows daylight saving time. It runs only in `reacher-z/Awesome-Jev`, from `main`; the deployment mirror does not run another copy.

The scan proposes resource-data updates through a pull request. It does **not** merge that request, promote discoveries into the curated README, or synchronize the website mirror. Maintainers review the evidence and merge useful changes, then use the publication process below.

### Operation and results

1. The read-only scan job reads the current Decision Index and linked news/artifacts, refreshes existing sources, follows one level of dependency links, and runs the configured scholarly discovery queries. Scheduled runs do not impose a new-candidate count cap; this is bounded discovery, not a scan of the entire web. The job rebuilds the index and validates the resulting data.
2. A separate publication job checks the permitted output files before receiving its publication token. Material changes are proposed on `automation/source-scan` with the title `chore: refresh public source index`; subsequent updates reuse the open PR.
3. Unchanged source content keeps its existing evidence and retrieval timestamps. A clock change alone should not create a new data update. Fetch failures are reported, with previous successful evidence retained rather than dropped or relabeled as a new successful fetch.
4. Automated collection never grants `editorial_reviewed`. If a previously reviewed source changes, the old reviewed record remains distinguishable from the new material awaiting review.

Use **Actions → Scan public sources → Run workflow**, selecting `main`, to trigger the same process manually. A successful scan is not proof that a PR was merged or the website was deployed; inspect the run summary and the proposed diff separately.

Manual runs can select all new candidates or a cap of 100 or 300. The `smoke` option performs a small public-network dry-run: it does not rewrite the ledgers or scan report, package an update, or publish a PR. It checks connectivity and the small scan path, not the completeness of a full scheduled run.

The same collector can be inspected locally without a GitHub token:

```sh
python3 scripts/refresh_sources.py --smoke
```

GitHub may place CI for a PR created or updated with `GITHUB_TOKEN` in an approval-required state. A maintainer with write access can select **Approve workflows to run** on the PR. The scan's own validation still runs before publication. See [GitHub's token-trigger rules](https://docs.github.com/en/actions/concepts/security/github_token#when-github_token-triggers-workflow-runs); do not assume a proposed PR already has successful independent checks.

GitHub schedules are best-effort: runs may be delayed, and public-repository schedules can be disabled after 60 days without repository activity. See [GitHub's schedule documentation](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule). If the schedule is disabled, re-enable it in Actions and inspect a manual run before relying on later scans.

**Operational check, 2026-10-16:** the [full manual scan and publication run](https://github.com/reacher-z/Awesome-Jev/actions/runs/38848656459) succeeded. A temporary, read-only five-minute UTC probe produced no `event=schedule` runs during **06:50:35–07:05:33 UTC**, covering the 06:55, 07:00, and 07:05 opportunities. The probe was then removed. The twice-daily schedule remains configured, but automatic cron execution has not yet been demonstrated; the cause of the missing events is unconfirmed.

### Trust and publication boundaries

Fetched pages, model cards, metadata, and repository descriptions are **untrusted data**. The scanner does not execute their code, follow instructions embedded in them, or install packages they recommend. Requests are public and unauthenticated; credential-bearing URLs and private network addresses are outside the scan scope. Provider failures and retry exhaustion must remain visible without destroying prior evidence.

The collection job has read-only repository permissions and no publication-token environment variable. The separate publication job receives write permissions only for proposing the bounded data update; its token is injected into the final publication step. It must not execute downloaded source code or interpret source text as a shell command. Keep credentials, private URLs, raw caches, and full copyrighted documents out of the proposed commit.

The evidence tiers below still apply. An automatically discovered source is not an endorsed recommendation, an abstract check is not a full-paper review, and a published result is not an experiment reproduced by this project.

## Refresh the evidence

Run these commands from the repository root. These are the legacy full-refresh commands, separate from the scheduled incremental scan above. They make public network requests and replace the default output ledgers; inspect the resulting changes before committing.

```sh
python3 scripts/collect_ecosystem.py --workers 12 --max-depth 1
python3 scripts/collect_research.py --target 0 --with-openalex --workers 3
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

## Preserve curation decisions

[Source curation](../data/source-curation.json) records exact-URL exclusions and evidence-backed display corrections. Exclusions prevent rejected material from being reintroduced by a later scan. An excluded record still present in an accepted ledger fails validation; removing an existing record requires an explicit reviewed change.

Annotations may correct a displayed title, first-submission date, topic, relationship, or relevance note. They include a primary-source URL and review date. Raw provider metadata, retrieval timestamps, hashes, and verification levels remain unchanged. The website exposes each correction's source under its corpus entry.

When an update PR is still open, the publisher refuses to replace it with data that drops or downgrades previously gathered evidence or loses an outstanding editorial-review candidate. An explicit trusted exclusion can authorize a scope removal. A blocked update leaves the existing PR available for review.

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

Collect only public resources with public, unauthenticated requests. Keep private transcripts, credentials, local account configuration, machine-specific paths and raw response caches out of commits. Before publication, inspect the staged files and commit author identity; use the maintainer's public GitHub identity and GitHub-provided noreply address rather than a private email address. Preserve historical authorship instead of attributing every past commit to the current maintainer. Do not copy full copyrighted articles or abstracts into the ledger.

Preserve the individual licenses of third-party resources. A repository license does not relicense linked papers, datasets or models. The bundled fonts carry SIL Open Font License notices; the icon subset is Font Awesome **Free**, with its included license. Keep those notices and source versions with the assets. Do not add Font Awesome Pro files or proprietary font packages to this public repository.

## 中文说明

### 每日两次扫描

[Scan public sources](../.github/workflows/scan-sources.yml) 配置为每天洛杉矶时间 **09:17 和 21:17** 运行，时区为 `America/Los_Angeles`，会随夏令时调整。只在主仓库 `reacher-z/Awesome-Jev` 的 `main` 上运行，网站部署镜像不会重复执行。

扫描通过 `automation/source-scan` 分支创建或更新同一个待审 PR，标题为 `chore: refresh public source index`。**不会自动合并、自动把发现项加入精选 README，也不会自动同步网站镜像。** 维护者核对来源与差异、合并后，再按发布流程同步。

定时扫描覆盖当前 Decision Index、其动态与链接材料、已有来源、一层依赖链接和已配置的学术查询；不设新增候选数量上限，但不代表扫描整个互联网。手动运行可选择全部候选或 100／300 项上限。`smoke` 只进行小规模公开网络试运行，不写入台账或报告、不打包更新、不发布 PR，也不证明完整扫描已经通过。

扫描 job 只读且不接收发布 token。独立发布 job 先检查允许更新的文件，再仅在最后发布步骤注入 token。远程网页、README 和模型卡中的内容一律作为不可信数据处理，不执行其代码或指令，不使用其推荐安装命令；仅请求公开来源，拒绝携带凭据的 URL 与私有网络地址。

内容未变时保留原有证据和抓取时间，避免仅更新时间戳的 PR。抓取失败或重试耗尽时保留既有成功记录并报告失败，不能把失败伪装为新的成功核查。自动扫描不授予 `editorial_reviewed`；已有编辑审阅的来源发生变化时，应区分旧已审版本与待复核的新内容。

手动运行：**Actions → Scan public sources → Run workflow**，选择 `main`。GitHub 定时运行可能延迟，公开仓库长期无活动时也可能停用；以 Actions 状态和运行摘要为准。扫描成功不等于 PR 已合并或网站已发布。

**2026-10-16 运行核查：**[完整手动扫描及发布流程](https://github.com/reacher-z/Awesome-Jev/actions/runs/38848656459)已成功。临时只读的五分钟 UTC 探针在 **06:50:35–07:05:33 UTC** 观察窗口内没有产生 `event=schedule` 运行，覆盖 06:55、07:00 和 07:05 三次机会；观察结束后已移除探针。每日两次配置仍保留，但尚未实证自动定时触发，缺失事件的原因未确认。

由 `GITHUB_TOKEN` 创建或更新的 PR，其 CI 可能处于等待批准状态；有写权限的维护者可在 PR 上选择 **Approve workflows to run**。扫描本身会在发布 PR 之前校验，但不能因此假定 PR 已取得全部独立检查结果。

### 人工维护与发布

维护顺序是：刷新公开来源清单 → 生成网站索引与计数 → 运行校验和回归测试 → 同步中英文精选内容 → 检查暂存区后发布。`--resume` 与 `--offline` 会复用已有材料，不能写成全部来源重新抓取。

[reacher-z/Awesome-Jev](https://github.com/reacher-z/Awesome-Jev) 是资源主仓库，也是 issue 和 PR 的统一入口；[组织仓库](https://github.com/AwesomeJev/AwesomeJev.github.io) 是网站部署镜像。维护者将验证通过的同一个 `main` 提交推送到 `origin` 与 `awesomejev`，并核对两边提交一致；当前没有自动镜像同步。

自动正文筛查、摘要检查、编辑复核和亲自复现是不同层级。PR 自动评论不等于学术审查，也不批准合并。CI 在两个仓库运行，Pages 部署 job 仅允许组织部署仓库执行、只发布 `site/`；完成后检查两边 Actions 与线上双语页面。

只使用公开来源，不提交密钥、私人对话、个人路径或原始缓存。保留第三方字体、图标、模型与数据的许可边界，不将商业受限资源描述为可任意使用的开源资源。
