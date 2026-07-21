# Open Design Validation

Status: **PARTIAL - G-01 remains pending**
Observation time: `2026-07-21T18:58:23+08:00`

## Confirmed Selection

- The student selected the per-turn skill `frontend-design` in the Open Design composer.
- The student selected design system `default`, displayed by Open Design as `Neutral Modern`.
- The composer displayed the linked local directory as `ProjectB`.
- A student-provided screenshot in the conversation shows all three selections. The screenshot was not copied into the repository.

This is the actual v1 UI workflow choice, not an agent-selected default. ProjectB adds these overrides to Neutral Modern: card radius at most 8 px, `letter-spacing: 0`, compact workbench density, no marketing hero, a top horizontal four-stage timeline on desktop and mobile, and semantic status colors that are not the only state signal.

## Local Runtime Evidence

The packaged desktop restarted onto Open Design `0.15.1`. Its daemon log reported a healthy ephemeral loopback endpoint. At the observation time, direct read-only requests to that live endpoint returned:

```json
{
  "health": {"ok": true, "version": "0.15.1"},
  "skill": {
    "id": "frontend-design",
    "mode": "prototype",
    "designSystemRequired": true
  },
  "designSystem": {
    "id": "default",
    "title": "Neutral Modern"
  }
}
```

The endpoint used for this check was an observed ephemeral port, not a value to persist in project or Codex configuration. Open Design changed the port after a desktop restart, as designed.

The desktop app config still stores global `skillId: null` and `designSystemId: "default"`. This does not contradict the screenshot: Open Design attaches skills to an individual composer turn, while the design system can also be the global/default selection. The config's recent linked directories includes ProjectB, but no Open Design project or artifact has yet been created for this gate.

## MCP Evidence Still Missing

The Open Design MCP process for the current Codex task started before the latest desktop daemon and cached the fallback `http://127.0.0.1:7456`. Its `list_skills`, `list_projects`, and `get_active_context` calls therefore still fail even though the new daemon is healthy on an ephemeral port.

The installed `od mcp --help` states that daemon resolution happens when the MCP process starts and that a running MCP server caches the URL; after a daemon restart, the MCP client must restart to discover the new port. The existing MCP registration must not be duplicated or replaced with an ephemeral port.

To close G-01, keep Open Design running, start a fresh Codex task so its MCP process restarts, and capture successful results from:

1. `list_skills` containing `frontend-design`;
2. `list_projects` or a truthful empty project list before project creation;
3. `get_active_context` for the actual Open Design project/context once created;
4. the Open Design version and selected `frontend-design` / `default` identifiers.

Until those MCP calls succeed, this file is selection and daemon evidence only. It is not a formal Open Design run, generated artifact, UI implementation, or G-01 PASS.

## Alternatives Not Selected

- `shadcn`: retained only as a fallback; its compact 8 px component posture is useful, but its default monochrome treatment would require more status-color work.
- `design-brief`: not selected because it would introduce another design-system decision rather than apply the already confirmed UI direction.
- Catalog-only stubs such as `ui-ux-pro-max`: not selected because the local entry is not a complete bundled workflow.
- `web-design-guidelines`: reserved for post-implementation UI review, not used as the generation skill.

No Open Design prompt was sent, no artifact was generated, and no frontend or production file was created or modified during this validation step.
