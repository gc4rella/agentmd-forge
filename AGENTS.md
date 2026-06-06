# AGENTS.md

AgentMD Forge is a single portable skill for crafting `AGENTS.md` files. See README.md for install
steps.

## Repository map
- `skills/agentmd-forge/SKILL.md` — the skill's tight core
- `skills/agentmd-forge/reference.md` and `EXAMPLE.md` — supporting material loaded only as needed
- `skills/agentmd-forge/templates/` — AGENTS.md archetypes
- `skills/agentmd-forge/scripts/validate_agents_md.py` — the only executable here

## Setup & commands
- No build, no package manager, no dependencies (Markdown + one stdlib-only Python script).
- Run the validator: `python3 skills/agentmd-forge/scripts/validate_agents_md.py <AGENTS.md> --repo .`
- Render flowcharts (optional, if graphviz is installed): `dot -Tsvg file.dot -o file.svg`

## Conventions
- This repo ships exactly one skill: `agentmd-forge`.
- The skill folder name must match the `name` in `SKILL.md`.
- `SKILL.md` YAML frontmatter has only `name` and `description`.
- `description` starts with "Use when…", states triggers only, and never summarizes the workflow.
- Keep `SKILL.md` tight (≤ ~200 lines); push catalogs/tables into sibling reference files.
- Reference supporting files by relative path so the skill works from any skills directory.

## Safety & constraints
- NEVER commit secrets or credentials anywhere in the repo.
- Do not edit a skill without re-validating it (see Verification); untested skill edits are not kept.

## Verification (definition of done)
- For any AGENTS.md this repo's skill produces, run the validator above; it must exit 0.
- For changes to the skill, run:
  `python3 /Users/giuseppe/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/agentmd-forge`
