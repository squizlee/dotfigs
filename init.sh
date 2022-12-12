#!/usr/bin/env bash
# Setup by installing and symlinking packages

# INSTALL PACKAGES
sudo pacman -S fish emacs neovim kitty git base-devel noto-fonts ttc-iosevka

# AUR SETUP
if [ -x "$(yay -v)" ] ; then
	git clone https://aur.archlinux.org/yay.git
	cd yay
	makepkg -si
	cd ..
	rm -rf yay
fi

yay -S nerd-fonts-complete

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
cp ~/dotfigs/fish/conf.d/dracula.fish "$HOME/.config/fish/conf.d"

echo "System is setup"
