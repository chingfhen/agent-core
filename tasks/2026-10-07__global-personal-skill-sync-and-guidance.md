# Task: Install Personal Skills and Guidance Globally

**File:** `tasks/2026-10-07__global-personal-skill-sync-and-guidance.md`
**Created:** 2026-10-07
**Last Updated:** 2026-10-08
**Priority:** Now
**Status:** Closed

**Goal:** Replace per-project Agent Core skill deployment with one machine-level sync that installs the owner's personal skills and global agent guidance for Pi, Codex, OpenCode, and Claude Code.

**Why:** Personal workflows should remain current across projects without stale project copies, repeated updates, local ownership metadata, or conflicts with project-specific skills. Mandatory routing is more reliable through each harness's native global guidance than through a startup skill.

**Success Bar:** A new Windows computer with Git, CMD, and Python 3.10+ can clone to `%USERPROFILE%\.agent-core`, run the dependency-free CMD installer, and then use `agent-core sync` as the sole normal update command. Sync safely publishes configured personal skills and complete global guidance while preserving unrelated content. Existing project-local installations have an explicit safe retirement command.

**Chosen Direction:** Implemented. `personal-skills.toml` is authoritative; real copies are published under `~/.agents/skills/`; Claude receives aliases under `~/.claude/skills/`; `global/AGENTS.md` is published to native Pi, Codex, OpenCode, and Claude guidance paths; ownership lives in `~/.agent-core-state/ownership.json`; old apply remains deprecated compatibility; `retire-local` performs exact migration cleanup.

**Current State:**

- `agent-core sync` refreshes the fixed clean checkout, crosses a fresh-process boundary, validates committed sources and every destination, stages and fingerprints copies, publishes skills/guidance/Claude aliases as one rollback-capable transaction, and writes ownership last.
- The CMD-first installer creates `%LOCALAPPDATA%\AgentCore\bin\agent-core.cmd` and updates the user PATH through `HKCU\Environment` without PowerShell, `setx`, `uv`, `pip`, elevation, or package downloads.
- Python 3.10 is the supported minimum. The Python 3.11 `tomllib` requirement was replaced with a strict parser for the manifest's intentionally narrow format.
- `agent-os-session` was replaced by concise automatically loaded `global/AGENTS.md`. The stale repository `knowledge-base` skill and local backend helpers were removed; guidance points to the canonical Google Drive workflow and adapter IDs.
- `agent-core retire-local --here` removes only fingerprint-matching old copies and exact legacy state/exclusion entries, refusing tracked or modified content before mutation.
- Repository docs now make global sync the only normal workflow and clearly distinguish Pi guidance under `~/.pi/agent/` from shared skills under `~/.agents/skills/`.

**Human Action:** After these changes are committed and pushed, this existing machine's installed launcher is still the pre-sync version. Run the one-time migration in CMD:

```cmd
git -C "%USERPROFILE%\.agent-core" pull --ff-only
"%USERPROFILE%\.agent-core\scripts\install-agent-core.cmd"
```

Open a new terminal if instructed, then run:

```cmd
agent-core sync
```

For any old project-local installation, enter that exact directory and run `agent-core retire-local --here` after confirming no local modifications should be preserved.

**Blockers:** None. The remaining commands are owner deployment and optional per-project migration, not repository implementation work.

**Verification:**

- Standard-library suite: 23 tests passed on Python 3.13.14 and Python 3.10.18.
- `python -m compileall -q agent_core tests scripts` passed.
- `git diff --check` passed.
- The CMD dispatcher was executed from Git Bash through `cmd.exe` with a synthetic helper and selected `python` successfully without PowerShell.
- Isolated sync tests created Windows directory junctions and proved first sync, repeat no-op, updates, recreation, additive removal, unowned/modified refusal, guidance states, alias recovery, all-target preflight, rollback, state publication failure, source tracking, legacy apply compatibility, and retirement safety.
- Pi 1.0.4 RPC `get_commands` discovered an isolated `~/.agents/skills/` skill exactly once with user scope.
- OpenCode 1.18.11 `debug skill` discovered a shared skill plus Claude junction exactly once at the shared path, clearing the duplicate-name blocker.
- Codex CLI 0.145.0 `debug prompt-input` exposed current `~/.agents/skills/` entries and an isolated global `AGENTS.md` marker.
- Claude alias identity is covered by filesystem tests and Claude Code 2.1.285's installed help confirms skills and `CLAUDE.md` customization. Model-level compliance with new guidance was not claimed or tested because no real user-global publication or paid model turn was performed.

**Docs Sync:** Synced

**Canonical Docs:** `README.md`, `AGENTS.md`, `docs/agent-core-operating-manual.md`, `docs/consumer-repo-enrollment.md`, and `docs/memory-pilot.md`.

**Implementation:** `agent_core/bootstrap.py`, `agent_core/sync.py`, `agent_core/manifest.py`, `agent_core/apply.py`, `agent_core/retire.py`, `scripts/install-agent-core.cmd`, `scripts/install_agent_core.py`, `personal-skills.toml`, `global/AGENTS.md`, `pyproject.toml`, `uv.lock`, and `tests/test_agent_core.py`.
