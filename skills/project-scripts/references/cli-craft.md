# CLI craftsmanship for personal project scripts

Read when creating or materially changing a personal script. Apply these as **design defaults, not a feature checklist**. The best utility is often small, boring, transparent, and robust. Do not inflate a five-line command into a framework.

## Choose the right implementation

- **Existing command/task-runner:** Prefer it when it already expresses the action, including its failure semantics, clearly.
- **Shell script:** Good for a short sequence of commands and light glue on a known shell/platform. Keep quoting explicit and propagate failures. Prefer a structured language when branching, parsing, portability, or data transformation grows.
- **Python:** A practical cross-platform default for nontrivial file operations, structured processing, and argument-driven CLIs. Prefer standard-library `argparse`, `pathlib`, `logging`, `subprocess`, and `json` where sufficient. Follow the workspace's `run-and-manage-python` workflow for execution; don't bypass it with system Python or ad hoc environments.
- **JavaScript/TypeScript/PowerShell/etc.:** Choose when the user's existing platform, dependencies, or APIs make them materially simpler. Avoid introducing a language solely to standardize the collection.

Use the fewest dependencies consistent with reliable behavior. Personal scripts can target other projects via arguments while remaining stored in the configured Project Scripts Root.

## Design the human-facing command

Make the contract easy to guess and inspect:

- Use a descriptive command name and short description. Support `--help`; explain required arguments and include one correct example, especially for non-obvious inputs.
- Prefer explicit `--input`, `--output`, `--root`, `--format`, or similar literal flags when they improve clarity. Use positional arguments when the meaning is unambiguous. Follow established conventions instead of inventing aliases for everything.
- Make input validation fail early, with a precise description of what was wrong and how to correct it. Avoid prompting in agent-driven or batch mode.
- Separate results from chatter: stdout carries the primary result (including machine-readable data); stderr carries warnings, progress and diagnostics. Support `--json` only when there is a real machine consumer, and keep it clean and stable if implemented.
- Use exit status `0` only for success, and nonzero for failure. Distinguish common failure modes only when consumers can use the distinction. Never silently convert partial failure into success.
- Use `--verbose` or equivalent for diagnostic depth when the operation warrants it; normal output should be a concise summary (what changed/checked, counts when useful, and where outputs went). Log meaningful actions, not every iteration. Do not create rotating log files or telemetry infrastructure by default.

A possible interface for a real script might look like:

```text
check-index --root <personal-kb> [--verbose]
  Check index links without modifying files.
  Exits 0 when valid, nonzero with broken-link details otherwise.
```

This is an illustration, **not** authorization or a request to create that script.

## Safety, reruns, and operational behavior

- Prefer read-only behavior unless the job requires mutation. For consequential changes, clearly show targets/anticipated changes; support `--dry-run` when it is genuinely useful, and ensure it has **no writes**.
- Require explicit target paths or identifiers for actions that could affect multiple repositories or accounts. Don't infer live targets from an unrelated current directory.
- Handle path spaces, Unicode, platform separators and absent files sensibly. Distinguish a missing required input from an empty valid input.
- Avoid leaking tokens, credentials, PII, or sensitive payloads in logs, CLI arguments that may appear in process lists, test fixtures, and saved output.
- Where repeat runs are normal, aim for idempotence or safe detection of already-completed work. For files, avoid partial output with temporary-file-plus-atomic-replace patterns when failure could corrupt the target; don't require transactional machinery for trivial read-only scripts.
- For external processes, propagate or accurately translate their exit codes, capture useful error context, and bound waits when hangs are plausible. Do not blindly retry non-idempotent work or suppress exceptions.
- Build commands with argument arrays, not interpolated shell strings, when possible. Be especially careful with untrusted filenames/paths and `shell=True`-style execution.
- Keep hidden filesystem/network effects out of imports, help handling and dry runs. Scripts shouldn't create directories or touch services simply to print `--help`.

## Testing and maintenance

Test at the **command boundary**, not only helper functions, when feasible:

1. `--help` produces a usable description and example, without side effects.
2. A representative valid input produces the promised result and success status.
3. Invalid input or a relevant failure returns nonzero with useful diagnostics.
4. Important mutation/failure scenarios leave data safe; dry-run and repeat-run behavior is truthful if supported.

Use lightweight fixtures and temporary directories. A tiny utility may need only a few focused tests; a data-mutating tool deserves more. Never execute a potentially destructive real-world scenario merely to validate the new code.

On maintenance: inspect existing callers and behavior first; preserve documented arguments and output contracts when possible. Improve or consolidate instead of producing `script_v2` clones. Update the root `INDEX.md` when the user-facing command changes. Avoid auto-generated indexes or redundant per-script manifests.

## Why these defaults

Reference material for the above principles:

- [Command Line Interface Guidelines](https://clig.dev/) — help, examples, stdout/stderr, exit codes, non-interactivity, safe flags.
- [Python `argparse` documentation](https://docs.python.org/3/library/argparse.html) — standard argument parsing, usage help, argument errors.
- [Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html) — shell as a small glue language, quoting, stderr and error handling.
- [The Twelve-Factor App: Logs](https://12factor.net/logs) — treat logs as streams managed by the caller rather than building logging infrastructure into every script.
- [OpenAI skill-creator](https://github.com/openai/codex/blob/main/codex-rs/skills/src/assets/samples/skill-creator/SKILL.md) — package executable resources when deterministic behavior actually improves repeatability; use progressive disclosure.
