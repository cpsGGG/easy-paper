# Claude Code Adapter

This directory contains the minimal Claude Code specific files for `easy-paper`.

## What This Adapter Adds

- `/easy-paper` comes from the skill name in `SKILL.md`
- `/ep` is provided as a Claude Code command alias

## Install Layout

Copy the repository files into Claude Code like this:

```text
~/.claude/skills/easy-paper/
  SKILL.md
  README.md
  scripts/
  references/
  agents/

~/.claude/commands/ep.md
```

## Why `/ep` Needs An Extra File

Claude Code does not automatically create a second slash command just because the skill body says `/ep` should work.

The `easy-paper` skill itself provides `/easy-paper`.
The alias file in `commands/ep.md` provides `/ep`.

Other agent frameworks may use a different alias mechanism. Keep the root `SKILL.md` as the portable core, and treat files under `agents/` as platform adapters.
