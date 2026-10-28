# Pi and OpenCode Shortcut Contract

**Last Updated:** 2026-10-29

**Status:** Trial layout; terminal behavior requires user verification.

**Source Of Truth:** The intended shared personal keyboard layout and manual reconciliation procedure for Pi and OpenCode.

## Shared shortcuts

| Action | Shortcut | Pi | OpenCode |
| --- | --- | --- | --- |
| Cycle effort / model variant | Shift+Tab | Cycle thinking level | Cycle model variants |
| Next model | Ctrl+P | Cycle forward | Cycle recent models forward |
| Previous model | Alt+P | Cycle backward on Windows | Cycle recent models backward |
| Model picker | Ctrl+Shift+P | Model selector | Model list |
| Toggle thinking visibility | Ctrl+T | Toggle thinking blocks | Toggle thinking blocks |

Model availability, cycle order and available effort levels can differ between apps and providers. Matching shortcuts does not imply identical model lists or reasoning behavior.

OpenCode-specific controls: **Ctrl+L** cycles to the next agent and **Alt+L** to the previous agent; **F2** opens the command palette and **F3** opens the agent picker. Some keyboards require Fn for function keys. Ctrl+Shift+P can be intercepted by a terminal or reported as Ctrl+P; verify that it opens the model picker without triggering model cycling in both apps.

## Manual synchronization

This document defines the intended layout; it does not automatically synchronize settings. Agent Core sync does not publish or manage harness settings. When changing the layout, update this contract and reconcile each app's existing configuration while preserving unrelated user settings:

- Pi: `~/.pi/agent/keybindings.json`. The model picker is overridden; the remaining shared shortcuts match the installed Windows defaults absent other overrides or extensions. Use `/reload` and `/hotkeys` to check active bindings.
- OpenCode: `~/.config/opencode/cli.json` (or `$XDG_CONFIG_HOME/opencode/cli.json` when set), under `keybinds`. Valid changes reload in the TUI. See the [OpenCode keybind reference](https://opencode.ai/v2/docs/cli/keybinds) for command IDs and default bindings.

Before and after changes, inspect existing settings and extension bindings, verify key direction and model set, and test the shortcuts in the actual terminal and relevant UI contexts. Keep ordinary text input and unrelated commands usable. Resolve conflicts deliberately; terminal handling and provider capabilities may differ by platform.
