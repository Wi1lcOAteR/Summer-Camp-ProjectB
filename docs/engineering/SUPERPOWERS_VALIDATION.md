# Superpowers Installation and Invocation Evidence

Status: **CACHE-ONLY / NOT CALLABLE**

Verification time: `2026-07-22T02:55:19+08:00` (Asia/Shanghai)

## Result

Superpowers 6.1.1 is present as a complete downloaded plugin bundle, but it is not installed/enabled in the Codex environment used by this project and none of its skills are callable in the current task. A cache directory is not installation evidence.

This distinction matters for the course gate: manually reading `writing-plans/SKILL.md` and producing a transparent fallback plan does not prove a formal `superpowers:writing-plans` invocation.

## Evidence Layers

| Layer | Evidence | Result |
| --- | --- | --- |
| Bundle | `C:\Users\22078\.codex\plugins\cache\openai-curated-remote\superpowers\6.1.1\.codex-plugin\plugin.json` reports `name=superpowers`, `version=6.1.1`, `license=MIT`, `skills=./skills/`; manifest SHA-256 is `42F44D5E17AFF909BD6F2A53795D516D8CA78CD9512C32C91F19CBBCCED68877` | PASS: complete cache payload exists |
| Core files | Fourteen skill directories and their `SKILL.md` files are present | PASS: payload contents are complete |
| Codex user config | `C:\Users\22078\.codex\config.toml` contains enabled bundled/runtime plugins, but has no `plugins."superpowers@..."` entry and no `openai-curated` / `openai-curated-remote` marketplace entry | FAIL: no installed/enabled state for Superpowers |
| CLI marketplace state | Codex CLI 0.144.4 returns `{"marketplaces":[]}` for `codex plugin marketplace list --json` and `{"installed":[],"available":[]}` for `codex plugin list --available --json` | FAIL for that CLI environment; its separate unauthenticated status is not used to infer the desktop account's authentication state |
| Current task catalog | The task's supplied available-skill list contains no `superpowers:*` entry | FAIL: no formal invocation is possible in this task |
| Official catalog | OpenAI's current `openai/plugins` marketplace is named `openai-curated` and lists `superpowers` as `AVAILABLE` for `CODEX`; repository HEAD observed as `11c74d6ba24d3a6d48f54a194cd00ef3beea18f9`, marketplace file SHA `dff3ad09da7efc35a6d3b905b1aa07795bc240b6` | PASS: an official install source exists |

`codex doctor` was also run read-only. It confirmed a consistent 0.144.4 CLI installation but no CLI credentials and limited network reachability. That diagnostic is specific to the standalone CLI process and does not override the desktop task's direct skill catalog or the user config evidence above.

## Detected Cache Skills

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

These names describe files in the cache, not skills available to the current agent.

## Official Loading Rule

OpenAI's [Plugins documentation](https://learn.chatgpt.com/docs/plugins) says plugins are installed from the desktop Plugins directory and that bundled skills become available in a **new chat or CLI session after installation**. The [Build plugins documentation](https://learn.chatgpt.com/docs/build-plugins) separately states that installed plugin on/off state is stored in `~/.codex/config.toml`; a cache path is only where the installed copy is loaded from.

The Superpowers bundle's own README gives the Codex App path: open **Plugins**, find **Superpowers** in the Coding section, select `+`, then use a new task. This agrees with the OpenAI loading rule.

## Required Human/App Action

1. In the Codex desktop app, open **Plugins** and inspect the **Installed** row.
2. Search for **Superpowers**. Install it with `+`, or re-enable/reinstall it if the UI shows a disabled or incomplete existing entry.
3. Start a **new Codex task** for ProjectB after installation; continuing this already-started task is not a valid refresh check.
4. Verify that the task's skill catalog exposes the Superpowers skills, especially `brainstorming` and `writing-plans`.
5. Formally invoke `writing-plans` to review the already-confirmed `SPEC.md` and existing fallback `PLAN.md`. Preserve the fallback provenance; record the formal invocation and any resulting diff rather than pretending it happened earlier.

Alternative course gate: obtain explicit course acceptance that the fully documented fallback plan satisfies the required `writing-plans` step. Project documentation alone cannot create that acceptance.

## Non-Actions

- No user-level Codex config, marketplace, plugin state, authentication or cache was changed.
- The cached plugin was not copied or vendored into the project.
- No formal Superpowers invocation is claimed.
- No cold start, worktree implementation, production source, Open Design run or deployment was started.
