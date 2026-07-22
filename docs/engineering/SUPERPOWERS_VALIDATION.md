# Superpowers Installation and Invocation Evidence

Status: **INSTALLED + ENABLED / CURRENT TASK NOT RELOADED**

Verification time: `2026-07-22T20:16:26+08:00` (Asia/Shanghai)

## Result

The student has now installed and enabled the official curated Superpowers plugin. `config.toml` records the plugin source and enabled state; that source's current cached installation contains one Superpowers snapshot, whose manifest and all fourteen bundled skill files are present. The plugin installation layer therefore passes.

The current ProjectB task was started before that state was loaded. Its supplied skill catalog still contains no `superpowers:*` entry, so this task cannot formally invoke `brainstorming` or `writing-plans`. OpenAI's loading rule requires a new chat/task or CLI session after installation.

This distinction matters for the course gate: manually reading `writing-plans/SKILL.md` and producing a transparent fallback plan does not prove a formal `superpowers:writing-plans` invocation.

## Evidence Layers

| Layer | Evidence | Result |
| --- | --- | --- |
| Installed bundle | `C:\Users\22078\.codex\plugins\cache\openai-api-curated\superpowers\11c74d6b\.codex-plugin\plugin.json` reports `name=superpowers`, manifest `version=5.1.3`, `license=MIT`, and `skills=./skills/`; manifest SHA-256 is `CE06DE063CABC2C41FFCE239AEB5CB941FCAB0C98DDDEDE927AA06E854D40AED` | PASS: the selected installed snapshot is complete |
| Core files | The selected snapshot contains fourteen skill directories and every directory contains `SKILL.md` | PASS: installed payload contents are complete |
| Codex user config | `C:\Users\22078\.codex\config.toml` contains `[plugins."superpowers@openai-api-curated"]` with `enabled = true`; the file was last changed at `2026-07-22T20:11:10+08:00` | PASS: installed/enabled state exists |
| Earlier cache | The older `openai-curated-remote\superpowers\6.1.1` payload remains on disk, but belongs to a different cache source from the enabled `openai-api-curated` plugin | Informational only; it is not used as current installation evidence |
| CLI marketplace state | Codex CLI 0.144.4 still returns `{"marketplaces":[]}` and `{"installed":[],"available":[]}` | Inconclusive for the desktop installation; this separately unauthenticated CLI state does not override direct desktop config/cache evidence |
| Current task catalog | The task's supplied available-skill list contains no `superpowers:*` entry | FAIL at the session-loading layer: no formal invocation is possible in this already-running task |
| Official catalog | OpenAI's current `openai/plugins` marketplace is named `openai-curated` and lists `superpowers` as `AVAILABLE` for `CODEX`; repository HEAD observed as `11c74d6ba24d3a6d48f54a194cd00ef3beea18f9`, marketplace file SHA `dff3ad09da7efc35a6d3b905b1aa07795bc240b6` | PASS: an official install source exists |

`codex doctor` was also run read-only. It confirmed a consistent 0.144.4 CLI installation but no CLI credentials and limited network reachability. That diagnostic is specific to the standalone CLI process and does not override the desktop task's direct skill catalog or the user config evidence above.

## Detected Installed Skills

1. `brainstorming`
2. `dispatching-parallel-agents`
3. `executing-plans`
4. `finishing-a-development-branch`
5. `receiving-code-review`
6. `requesting-code-review`
7. `subagent-driven-development`
8. `systematic-debugging`
9. `test-driven-development`
10. `using-git-worktrees`
11. `using-superpowers`
12. `verification-before-completion`
13. `writing-plans`
14. `writing-skills`

These names are present in the enabled plugin's installed snapshot. They are not yet skills available to this already-running agent because its task catalog predates the installation.

## Official Loading Rule

OpenAI's [Plugins documentation](https://learn.chatgpt.com/docs/plugins) says plugins are installed from the desktop Plugins directory and that bundled skills become available in a **new chat or CLI session after installation**. The [Build plugins documentation](https://learn.chatgpt.com/docs/build-plugins) separately states that installed plugin on/off state is stored in `~/.codex/config.toml`; a cache path is only where the installed copy is loaded from.

The Superpowers bundle's own README gives the Codex App path: open **Plugins**, find **Superpowers** in the Coding section, select `+`, then use a new task. This agrees with the OpenAI loading rule.

## Required Human/App Action

1. Start a **new Codex task** for ProjectB. Continuing or resuming this pre-installation task is not a valid refresh check.
2. In that new task, verify that the skill catalog exposes the Superpowers skills, especially `brainstorming` and `writing-plans`.
3. Formally invoke `writing-plans` to review the already-confirmed `SPEC.md` and existing fallback `PLAN.md`. Preserve the fallback provenance; record the formal invocation and any resulting diff rather than pretending it happened earlier.
4. Only if a genuinely new task still lacks the skills, restart the desktop app, confirm Superpowers remains enabled in **Plugins -> Installed**, and then create another new task. Do not reinstall or copy skill files merely because this old task is stale.

Alternative course gate: obtain explicit course acceptance that the fully documented fallback plan satisfies the required `writing-plans` step. Project documentation alone cannot create that acceptance.

## Non-Actions

- The student changed the user-level plugin state before this verification; this diagnostic did not modify config, marketplace, authentication or cache state.
- The cached plugin was not copied or vendored into the project.
- No formal Superpowers invocation is claimed.
- No cold start, worktree implementation, production source, Open Design run or deployment was started.
