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

Symlink the skill folder when you want local edits in this repo to propagate automatically. Copy it if
you want a fixed snapshot.

For OpenAI Codex:

```bash
mkdir -p ~/.agents/skills
ln -s "$PWD/skills/agentmd-forge" ~/.agents/skills/agentmd-forge
```

Invoke it with `$agentmd-forge` or through your skills UI.

For Claude Code:

```bash
mkdir -p ~/.claude/skills
ln -s "$PWD/skills/agentmd-forge" ~/.claude/skills/agentmd-forge
```

Invoke it with `/agentmd-forge`, or ask Claude Code to create or improve an `AGENTS.md` file.

Any `SKILL.md`-aware agent can use the same `skills/agentmd-forge` folder.

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
