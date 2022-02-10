#!/usr/bin/env bash
# Setup by installing and symlinking packages

# INSTALL PACKAGES
sudo pacman -S fish emacs neovim kitty 

# MAKE CONFIG FOLDERS IF NECESSARY
pushd "$HOME/.config"
mkdir -p fish emacs nvim kitty
popd

# SYMLINK CONFIG FILES
source ./link.sh

# CONFIGURE FISHER
chsh -s $(which fish) "$(whoami)"
sh -c "$(curl -fsSL https://starship.rs/install.sh)"
fish --command "curl -sL https://git.io/fisher | source && fisher install jorgebucaran/fisher"

# DONE
