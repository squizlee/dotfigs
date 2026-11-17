# (.)figs

My dotfiles. `./init.py` sets everything up and is safe to rerun (`-n` for a dry run).

- `cerebrum/`: AGENTS.md and LLM skills ([details](cerebrum/README.md))
- `emacs/`: org-mode Emacs config
- `ghostty/`: Ghostty terminal config (green theme, cmd+j/k to switch tabs). `init.py` also copies its colors into VS Code's integrated terminal (a marked block in VS Code's `settings.json`)
- `hammerspoon/`: macOS-only hotkeys (ctrl+option+t opens or focuses Ghostty)
- `shell/`: zsh config and Starship prompt. `~/.zshrc` stays local (secrets, machine setup) and sources `shell/zshrc` from its last line
