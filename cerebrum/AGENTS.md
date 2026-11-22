# AGENTS.md

Top-level preferences for every coding agent I use (Claude Code, Codex, …).
Lives in `~/dotfigs/cerebrum/` and is wired up by `init.py`.

## How I like to work

- I'm hands-on and work collaboratively most of the time. Treat me as a pair, not a client: show your reasoning at decision points, keep changes reviewable, and leave the final call on direction to me.
- Be direct. Lead with the answer, skip the preamble.
- Within a task I've agreed to, act on the obvious steps. Check in before anything that changes direction or scope.
- Prefer small, readable changes over clever ones. Delete dead code rather than commenting it out.
- Match the existing style of whatever repo you're in.

## Code

- Idempotent scripts: running twice should be a no-op, never destructive.
- Never delete user data to make room. Back it up or stop and ask.
- Verify before claiming done: run it, test it, show the output.
- Don't launch or restart GUI apps from the shell (`open -a`, `killall`). They inherit the agent's env (e.g. `GIT_EDITOR=true`) and pass it to everything they spawn. Ask me to do it.

## Self-improvement

When this session shows an instruction is wrong, stale, or missing (I corrected you, a command broke, you had to rediscover something), fix it at the source:

- Edit directly: skills in `~/dotfigs/cerebrum/skills/` (not the symlinks) and the current repo's `AGENTS.md`/`CLAUDE.md`.
- Ask first: this file, vendored/plugin skills, new skills.
- Smallest fix; tighten or delete before adding. No speculative or stylistic edits.
- Leave edits uncommitted and list them (file, what, why) at the end of the turn.

## Git

- Conventional-ish commit messages (`feat:`, `fix:`, `chore:`), imperative mood.
- Never commit, push, or create PRs. I do my own commits. Leave changes in the working tree and tell me what's ready; suggest a commit message if useful.
