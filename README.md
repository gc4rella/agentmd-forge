# AgentMD Forge

AgentMD Forge is a single portable skill for crafting high-signal `AGENTS.md` files. It is packaged
as a plain `SKILL.md` folder that works across agents that support skills, including OpenAI Codex and
Claude Code.

## Skill

### `agentmd-forge`

Crafts **`AGENTS.md`** files: the repo-level behavioral contract a coding agent should follow. It
works in two modes: scaffold one for a brand-new project through a short interview, or derive one
from an existing repo through a trust-tier codebase scan. It focuses on right altitude, exact
commands, negative rules, and hard-gate verification instead of generic section filling.

```
skills/agentmd-forge/
  SKILL.md                  # the skill (tight core)
  reference.md              # section catalog, trust-tier tables, compatibility notes, monorepo guidance
  EXAMPLE.md                # one fully worked example
  templates/                # AGENTS.md archetypes
  scripts/validate_agents_md.py
```

## Install

Symlink the skill folder so updates here propagate, or copy it into your agent's skills directory.

**Claude Code** (`~/.claude/skills/`):
```bash
ln -s "$PWD/skills/agentmd-forge" ~/.claude/skills/agentmd-forge
```
Invoke with `/agentmd-forge`, or describe the `AGENTS.md` task.

**OpenAI Codex** (`~/.agents/skills/`, also scanned per-repo at `.agents/skills/`):
```bash
ln -s "$PWD/skills/agentmd-forge" ~/.agents/skills/agentmd-forge
```
Invoke with `$agentmd-forge` or via `/skills`.

Any other `SKILL.md`-aware agent can point at the same folder.

## Validator

```bash
python skills/agentmd-forge/scripts/validate_agents_md.py AGENTS.md --repo . --json
```
Checks line/byte budget, required gate sections, secret leaks, and (with `--repo`) that the commands
and paths it references actually exist. It is stdlib-only Python 3.8+ and exists to quality-check
`AGENTS.md` files produced by the skill.
