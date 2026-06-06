<!--
TEMPLATE: cli-tool. Copy the fenced block to AGENTS.md and fill it in.
Replace <…>. Delete any line that doesn't change agent behavior. Keep it under ~150 lines.
Use EXACT commands you verified — never guess. <!-- comments don't belong in the final file. -->
-->

```md
# AGENTS.md

<name> is a command-line tool that <one-sentence purpose>. See README.md for usage docs.

## Working style
- Preserve the smallest behavior-preserving change.
- Do NOT change flag names, subcommands, exit codes, or output format unless the task requires it.
- If a request implies a breaking CLI change, surface it before coding.

## Repository map
- `<src dir>/` — application code (entrypoint: `<entrypoint>`)
- `<tests dir>/` — tests
- `<docs dir>/` — user-facing docs

## Setup & commands
- Install: `<install cmd>`
- Run: `<run cmd, e.g. uv run acme --help>`
- Lint: `<lint cmd>`   ·   Test: `<test cmd>`

## Coding conventions
- <non-default style/naming rules>
- Add a regression test for any parsing or output change.

## Safety & constraints
- NEVER commit secrets, tokens, or sample credentials.
- Keep `<docs dir>/` examples accurate and runnable.
- Do not change release/packaging config without approval.

## Verification (definition of done)
All must pass before done: `<lint cmd>` and `<test cmd>`.
"Done" = behavior covered by a test; `--help`/docs updated if the CLI surface changed.

## Known failure modes
- Inventing unsupported flags/subcommands.
- Changing human-readable output that tests or docs depend on.
```
