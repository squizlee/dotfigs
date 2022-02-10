#!/usr/bin/env bash

# link.sh - symlink and reset all configuration files
location="$HOME/dotfigs"
config="$HOME/.config"

# CORE PACKAGES
# bash
ln -sf "$location/shell/.bashrc" ~/.bashrc
# emacs
ln -sf "$location/emacs/init.el" "$config/emacs/init.el"
# kitty
ln -sf "$location/kitty/diff.conf" "$config/kitty/diff.conf"
ln -sf "$location/kitty/dracula.conf" "$config/kitty/dracula.conf"
ln -sf "$location/kitty/kitty.conf" "$config/kitty/kitty.conf"
# fish 
ln -sf "$location/fish/config.fish" "$config/fish/config.fish"
ln -sf "$location/fish/fish_plugins" "$config/fish/fish_plugins"
ln -sf "$location/fish/fish_variables" "$config/fish/fish_variables"
# neovim
ln -sf "$location/neovim/init.vim" "$config/nvim/init.vim"

