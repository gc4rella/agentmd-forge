# AGENTS.md

agentmdforge is a collection of portable skills for coding agents, in the open `SKILL.md` format
(works across Claude Code, OpenAI Codex, and others). See README.md for install steps.

## Repository map
- `skills/<name>/SKILL.md` — a skill's tight core; supporting files sit alongside it
- `skills/writing-agents-md/` — the flagship skill (forges AGENTS.md files)
- `skills/writing-agents-md/scripts/validate_agents_md.py` — the only executable here

## Setup & commands
- No build, no package manager, no dependencies (Markdown + one stdlib-only Python script).
- Run the validator: `python3 skills/writing-agents-md/scripts/validate_agents_md.py <AGENTS.md> --repo .`
- Render flowcharts (optional, if graphviz is installed): `dot -Tsvg file.dot -o file.svg`

## Conventions
- Every skill is a folder with `SKILL.md` whose YAML frontmatter has only `name` and `description`.
- `description` starts with "Use when…", states triggers only, and never summarizes the workflow.
- Keep `SKILL.md` tight (≤ ~200 lines); push catalogs/tables into sibling reference files.
- Reference supporting files by relative path so the skill works under either tool's skills dir.

## Safety & constraints
- NEVER commit secrets or credentials anywhere in the repo.
- Do not edit a skill without re-validating it (see Verification); untested skill edits are not kept.

## Verification (definition of done)
- For any AGENTS.md this repo's skill produces, run the validator above; it must exit 0.
- For changes to a skill, follow the skill-authoring TDD (baseline without the skill, confirm the
  skill improves behavior) before considering the change done.
