# 🧠 cerebrum

The LLM brain of (.)figs.

```
cerebrum/
├── AGENTS.md          # global preferences for every agent
└── skills/<name>/     # one folder per skill, each with a SKILL.md
```

`../init.py` wires it up:

| repo                  | lands at                                        |
| --------------------- | ----------------------------------------------- |
| `AGENTS.md`           | imported by `~/.claude/CLAUDE.md`, symlinked to `~/.codex/AGENTS.md` |
| `skills/<name>/`      | symlinked into `~/.claude/skills/` and `~/.codex/skills/` |

Add a skill: `mkdir skills/foo && $EDITOR skills/foo/SKILL.md && ../init.py`.
Rename or delete one and the next `init.py` run prunes the dead link.
