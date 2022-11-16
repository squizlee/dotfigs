;;; Config file

; packages
(require 'package)
(add-to-list 'package-archives '("melpa" . "https://melpa.org/packages/") t)
(package-initialize)

;; use package
(unless (package-installed-p 'use-package)
  (package-refresh-contents)
  (package-install 'use-package))

;; which key: show a list of possible options when typing a keypress
(use-package which-key
	:ensure t
	:init 
	(which-key-mode))

;; evil mode: Vim emulation the right way to edit text
(use-package evil
	:ensure t
	:init
	(evil-mode 1))

;; key-chord: mainly used for remapping <Esc> to jj
(use-package key-chord
	:ensure t
	:init
	(key-chord-mode 1)
	:config
	(setq key-chord-two-keys-delay 0.5)
	(key-chord-define evil-insert-state-map "jk" 'evil-normal-state))


;; remove unneeded UI 
(tool-bar-mode -1)
(menu-bar-mode -1)
(scroll-bar-mode -1)

;;; line numbers
(display-line-numbers-mode)
(setq display-line-numbers 'relative)

; remove that annoying alarm bell when you press the wrong key
(setq ring-bell-function 'ignore)

;;; IGNORE ;;;
(custom-set-variables
 ;; custom-set-variables was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(package-selected-packages '(zen-mode zig-mode use-package)))
(custom-set-faces
 ;; custom-set-faces was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 )
