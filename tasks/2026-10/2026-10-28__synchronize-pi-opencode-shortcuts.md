# Task: Synchronize Pi and OpenCode shortcuts

**File:** `tasks/2026-10/2026-10-28__synchronize-pi-opencode-shortcuts.md`
**Created:** 2026-10-28
**Last Updated:** 2026-10-29
**Priority:** Now
**Status:** Active

**Goal:** Agree on and eventually verify a comfortable, consistent keyboard layout across Pi and OpenCode.
**Success Bar:** The human approves a cross-app shortcut map; each app's configuration implements the approved map without unacceptable typing or command conflicts; the human verifies the bindings in their terminal.
**Chosen Direction:** Human approved the shared layout documented in `docs/pi-opencode-shortcuts.md` and its application to both apps.
**Current State:** Human validated effort cycling and model cycling in both apps, and model selection with the former Ctrl+L binding. Trial configuration now assigns Ctrl+Shift+P to model selection in both apps and Ctrl+L / Alt+L to OpenCode agent cycling. F2/F3 remain palette/picker bindings. OpenCode thinking visibility produced no obvious feedback and remains unverified.
**Next Action:** Human tests Ctrl+Shift+P in both apps, especially that it is distinguished from Ctrl+P; verifies Ctrl+L / Alt+L agent cycling and F2/F3 in OpenCode; tests thinking visibility in a session with a thinking block.
**Blockers:** Interactive verification remains outstanding.

## Approved starting point

| Action | Candidate | Notes |
| --- | --- | --- |
| Cycle thinking effort / variant | Shift+Tab | Already Pi's reported default; displaces OpenCode agent cycling. |
| Cycle models | Ctrl+P and Alt+P | Pi's installed Windows defaults are forward and backward respectively; OpenCode configured to match. Confirm actual model sets. |
| Model selector | Ctrl+Shift+P | Trial in both apps; ensure terminal distinguishes Ctrl+Shift+P from Ctrl+P. |
| OpenCode agent cycle | Ctrl+L / Alt+L | Trial next / previous. |
| OpenCode command palette | F2 | Approved replacement; initial leader sequence did not work. Awaiting interactive verification. |
| OpenCode agent selection | F3 | Approved replacement; initial leader sequence did not work. Awaiting interactive verification. |
| Thinking visibility | Ctrl+T | Pi default; OpenCode configured, but interactive effect remains unverified. |

The human asked about WASD-like previous/next shortcuts. Shift+A and Shift+D normally produce uppercase letters in a text composer, so they are poor global candidates. Modified or leader-based navigation is possible if desired, subject to terminal behavior and conflicts.

## Evidence and coordination

- The human supplied Pi's shortcut list and indicated Pi configuration is `C:\Users\tanch\.pi\agent\keybindings.json`, with `/reload` and `/hotkeys` for applying and viewing bindings. These claims have not been independently verified here.
- OpenCode V2 documentation lists `model.list`, `model.cycle_recent`, `model.cycle_recent_reverse`, `variant.cycle`, `agent.list`, `agent.cycle`, `command.palette.show`, and `session.toggle.thinking` under `keybinds` in global `cli.json`: https://opencode.ai/v2/docs/cli/keybinds . OpenCode's recent model list may not match Pi's cycle set.
- Another Pi agent is collaborating through this task; it is not a subagent spawned by OpenCode. Record verification findings here.
- The human approved these specific external configuration changes. Preserve unrelated configuration and seek approval for changes beyond this layout.

## Verification before completion

Check both apps' active bindings and exact cycle direction and model set; exercise selection, effort, agent switching and command palette; test typing uppercase letters and common editor shortcuts; check the actual Windows terminal recognizes proposed combinations. Record what was actually tested and any remaining discrepancies. The Pi agent should report findings here for joint human review before implementation.
