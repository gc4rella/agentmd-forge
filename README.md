# AgentMD Forge

AgentMD Forge is a portable skill for writing high-signal `AGENTS.md` files: the repo-level
behavioral contracts coding agents should follow before they edit code, run commands, or declare work
done.

It is intentionally small. The skill is a plain `SKILL.md` directory, uses Markdown templates, and
ships one stdlib-only validator. There is no package manager, build step, or runtime dependency.

## What It Does

`agentmd-forge` helps an agent create, review, or revise an `AGENTS.md` file in two situations:

- **Existing repo:** scan trusted repo signals first, then draft instructions from verified commands,
  paths, conventions, and CI gates.
- **Greenfield repo:** run a short interview, pick an archetype template, and leave unknown commands
  as TODOs instead of inventing them.

The output style is deliberately strict: exact runnable commands, clear safety constraints, repo maps
that matter, and hard verification gates. It avoids README duplication, generic advice, stale command
guesses, and parallel instruction files that drift.

## Repository Layout

```text
skills/agentmd-forge/
  SKILL.md                  # skill entrypoint and core workflow
  reference.md              # section catalog, trust model, compatibility notes, monorepo guidance
  EXAMPLE.md                # worked AGENTS.md example
  templates/                # archetypes for common repo shapes
  scripts/validate_agents_md.py
  agents/openai.yaml        # agent metadata/config
```

Templates currently cover CLI tools, libraries, monorepo roots, research prototypes, services, and
web apps.

## Install

Install from GitHub with the Skills CLI:

```bash
npx --yes skills add gc4rella/agentmd-forge --skill agentmd-forge -g -y
```

Preview the skill without installing:

```bash
npx --yes skills add gc4rella/agentmd-forge --list
```

Install from a local checkout while developing:

```bash
npx --yes skills add . --skill agentmd-forge -g -y
```

Target specific agents when needed:

```bash
npx --yes skills add gc4rella/agentmd-forge --skill agentmd-forge -a codex -a claude-code -g -y
```

Invoke it as `agentmd-forge` through your agent's skills UI, or ask the agent to use
`agentmd-forge` to create or improve an `AGENTS.md` file.

## Typical Usage

Ask your agent to use the skill from the target repository:

```text
$agentmd-forge create an AGENTS.md for this repo
```

For an existing repo, the skill should inspect manifests, lockfiles, Makefiles, CI workflows, lint
configs, existing instruction files, and other high-trust sources before asking follow-up questions.
For a new repo, it should ask for the stack, commands, constraints, and definition of done before
drafting.

After drafting, validate the result:

```bash
python3 skills/agentmd-forge/scripts/validate_agents_md.py AGENTS.md --repo .
```

Use JSON output when another tool needs structured findings:

```bash
python3 skills/agentmd-forge/scripts/validate_agents_md.py AGENTS.md --repo . --json
```

The validator checks budget, required gate sections, secret leaks, and repo-aware command/path
references. It is compatible with Python 3.8+ and uses only the standard library.

## Editing This Skill

Keep `SKILL.md` concise and workflow-focused. Put expanded rationale, tables, compatibility notes, and
examples in `reference.md`, `EXAMPLE.md`, or `templates/`.

Before handing off changes under `skills/agentmd-forge/`, run the skill validator from your Codex
installation:

```bash
python3 path/to/skill-creator/scripts/quick_validate.py skills/agentmd-forge
```

For changes to this repo's own `AGENTS.md`, run:

```bash
python3 skills/agentmd-forge/scripts/validate_agents_md.py AGENTS.md --repo .
```

`CLAUDE.md` should remain a pointer to `AGENTS.md`; do not duplicate the canonical instructions into
multiple files.
