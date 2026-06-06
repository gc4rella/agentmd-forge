# AGENTS.md

AgentMD Forge is a portable skill repo for generating high-signal `AGENTS.md` files. Keep this file
as the canonical agent contract; `CLAUDE.md` should stay a pointer to it.

## Setup & Commands
- There is no package manager, build step, or third-party dependency for this repo.
- Validate a generated or edited AGENTS file:
  `python3 skills/agentmd-forge/scripts/validate_agents_md.py <AGENTS.md> --repo .`
- Validate this skill after any skill change:
  `python3 /Users/giuseppe/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/agentmd-forge`
- Optional flowchart rendering, only when graphviz is installed:
  `dot -Tsvg file.dot -o file.svg`

## Repository Map
- `skills/agentmd-forge/SKILL.md` - the only skill entrypoint and tight workflow core.
- `skills/agentmd-forge/reference.md` - supporting tables, section catalog, and detailed guidance.
- `skills/agentmd-forge/EXAMPLE.md` - worked AGENTS.md example.
- `skills/agentmd-forge/templates/` - archetype templates used when drafting.
- `skills/agentmd-forge/scripts/validate_agents_md.py` - stdlib-only validator; the only executable.
- `skills/agentmd-forge/agents/openai.yaml` - agent metadata/config for the skill.
- `CLAUDE.md` - compatibility pointer; keep it as `@AGENTS.md` unless explicitly asked otherwise.

## Skill Conventions
- This repo ships exactly one skill: `agentmd-forge`.
- The skill folder name must match the `name` in `skills/agentmd-forge/SKILL.md`.
- `SKILL.md` YAML frontmatter must contain only `name` and `description`.
- The `description` must start with "Use when", state triggers only, and not summarize the workflow.
- Keep `SKILL.md` tight, roughly under 200 lines; move catalogs, tables, and examples into sibling
  reference files.
- Reference supporting files by relative path so the skill works from any skills directory.
- Keep templates plain Markdown with placeholders clearly marked; do not add frontmatter unless a
  user explicitly asks for machine-readable metadata.

## Editing Rules
- Use verified repo signals for commands and paths. Do not add guessed package-manager, test, lint,
  or build commands.
- Preserve portability. Do not introduce dependencies, generated artifacts, or local machine state
  unless the task explicitly requires them.
- Do not duplicate README install prose here; link or keep only behavior-changing instructions.
- When editing validator behavior, keep it stdlib-only and compatible with Python 3.8+.
- When editing `SKILL.md`, keep the core workflow concise and move expanded rationale to
  `skills/agentmd-forge/reference.md`.

## Safety & Constraints
- NEVER commit secrets, credentials, `.env` contents, tokens, or private keys anywhere in this repo.
- Do not read from or quote excluded secret files while deriving AGENTS.md guidance.
- Treat ignored assistant/editor state directories, including Codex, Claude local, Cursor, and
  Continue state, as local-only artifacts.
- Preserve reusable checked-in config exceptions such as `!.aider.conf.yml` in `.gitignore`.
- Do not replace `CLAUDE.md` with duplicated instructions; keep `AGENTS.md` canonical.

## Verification
- For changes to `AGENTS.md`, run:
  `python3 skills/agentmd-forge/scripts/validate_agents_md.py AGENTS.md --repo .`
- For any AGENTS.md this skill produces, run the validator against that file; it must exit 0 before
  handoff.
- For changes under `skills/agentmd-forge/`, run:
  `python3 /Users/giuseppe/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/agentmd-forge`
- If a verification command is unavailable or fails for environmental reasons, report the exact
  command and error instead of marking the work done.
