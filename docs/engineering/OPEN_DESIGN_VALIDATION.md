# Open Design Validation

Status: **PASS - G-01 environment and selection gate complete**
Initial daemon observation time: `2026-07-21T18:58:23+08:00`
Fresh MCP observation time: `2026-07-21T19:51:57+08:00`
Gate-scope correction time: `2026-07-21T21:08:02+08:00`

## Confirmed Selection

- The student selected the per-turn skill `frontend-design` in the Open Design composer.
- The student selected design system `default`, displayed by Open Design as `Neutral Modern`.
- The composer displayed the linked local directory as `ProjectB`.
- A student-provided screenshot in the conversation shows all three selections. The screenshot was not copied into the repository.

This is the actual v1 UI workflow choice, not an agent-selected default. ProjectB adds these overrides to Neutral Modern: card radius at most 8 px, `letter-spacing: 0`, compact workbench density, no marketing hero, a top horizontal four-stage timeline on desktop and mobile, and semantic status colors that are not the only state signal.

## Bundled Skill and Runtime Boundary

`frontend-design` did not need a separate download. Open Design 0.15.1 already ships the complete built-in workflow at `resources/open-design/skills/frontend-design/SKILL.md` with its Apache-2.0 `LICENSE.txt`; the selected `default` design system likewise ships `DESIGN.md`, tokens, components, manifests, and previews. Selecting the skill in the composer attaches that installed workflow to an Open Design turn. It does not install a new Codex skill.

The Open Design desktop daemon serves a different purpose: its MCP server proxies project and artifact operations to a running local Open Design instance, while an actual Open Design run injects the selected skill, design system, and craft references. The desktop application only needs to be running while MCP calls or an Open Design project/run are actively being used. Keeping it open without a project or run creates no additional evidence or project progress.

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

## Fresh Read-only MCP Evidence

In a fresh Codex task, the Open Design MCP dynamic daemon discovery succeeded. Only the three read-only discovery tools allowed by G-01 were called. Their observed results were:

```json
{
  "list_skills": {
    "skill_count": 162,
    "frontend-design": {
      "id": "frontend-design",
      "name": "frontend-design",
      "mode": "prototype",
      "surface": "web",
      "source": "built-in",
      "designSystemRequired": true,
      "hasBody": true
    }
  },
  "list_projects": {
    "projects": []
  },
  "get_active_context": {
    "active": false
  }
}
```

This closes the earlier stale-endpoint question and confirms that the installed MCP catalog exposes the selected `frontend-design` skill. The empty project list and inactive context are the truthful pre-implementation state, not an environment failure. The selected `default` / `Neutral Modern` contract is supported by the student-provided composer screenshot, the installed design-system package, and the direct local runtime evidence above.

## Deferred Open Design Workflow Evidence

An actual Open Design project/run is still required by the repository's UI workflow rule, but it is not part of the pre-implementation environment gate. After cold-start validation and explicit implementation approval, UI-01 must:

1. open Open Design for that task and create/use the real ProjectB design project;
2. run the approved UI brief with `frontend-design` and `default` / `Neutral Modern`;
3. record the project/context, selected identifiers, artifact, screenshots, and review findings in `docs/engineering/OPEN_DESIGN_RUN.md`;
4. treat generated artifact code as design evidence only until the UI task has produced and run its required failing test; do not copy generated code into production before the TDD red step.

G-01 passes because installation, MCP reachability, the complete bundled skill, and the student-selected design-system contract are all recorded. This PASS is not a formal Open Design run, generated artifact, UI implementation, or visual acceptance result.

## Alternatives Not Selected

- `shadcn`: retained only as a fallback; its compact 8 px component posture is useful, but its default monochrome treatment would require more status-color work.
- `design-brief`: not selected because it would introduce another design-system decision rather than apply the already confirmed UI direction.
- Catalog-only stubs such as `ui-ux-pro-max`: not selected because the local entry is not a complete bundled workflow.
- `web-design-guidelines`: reserved for post-implementation UI review, not used as the generation skill.

No Open Design prompt was sent, `start_run` was not called, no project or artifact was created, and no frontend or production file was created or modified during this validation step.
