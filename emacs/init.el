;; add melpa packages
(require 'package)
(add-to-list 'package-archives '("melpa" . "https://melpa.org/packages/") t)
(package-initialize)

(unless (package-installed-p 'use-package)
  (package-refresh-contents)
  (package-install 'use-package))

(unless (package-installed-p 'dracula-theme)
  (package-refresh-contents)
  (package-install 'dracula-theme))

;; command completion display
(use-package which-key
  :ensure t
  :config
  (which-key-mode))

;; vim emulation
(use-package evil
  :ensure t
  :config
  (evil-mode 1))

;; key-chord
(use-package key-chord
  :ensure t
  :config
  (key-chord-mode 1)
  (setq key-chord-two-keys-delay 0.5))

;; relative line numbers
(global-display-line-numbers-mode 1)
(setq display-line-numbers-type 'relative)

;; beacon package briefly highlight cursor location
(use-package beacon
  :ensure t
  :config
  (beacon-mode 1))

;; pretty up org with bullets
(use-package org-bullets
  :ensure t
  :config
  (add-hook 'org-mode-hook (lambda () (org-bullets-mode 1))))

;; Turn on visual line (word wrapping) mode when working with just text
(add-hook 'text-mode-hook 'turn-on-visual-line-mode)

;; org mode latex syntax highlighting
(setq org-highlight-latex-and-related '(latex script entities))

;; remove tool, menu, and scroll bars
(tool-bar-mode -1)
(menu-bar-mode -1)
(scroll-bar-mode -1)

;; remove default screen
(setq inhibit-startup-message t)

;; chill scroll speed
(setq scroll-conservatively 100)

;; disable bell sounds
(setq ring-bell-function 'ignore)

;; disable autosave and backup
(setq make-backup-files nil)
(setq auto-save-default nil)

;; vim / evil mode configuration

;; jj for escape
(key-chord-define evil-insert-state-map "jj" 'evil-normal-state)

(custom-set-variables
 ;; custom-set-variables was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(ansi-color-names-vector
   ["#0a0814" "#f2241f" "#67b11d" "#b1951d" "#4f97d7" "#a31db1" "#28def0" "#b2b2b2"])
 '(custom-enabled-themes (quote (dracula)))
 '(custom-safe-themes
   (quote
    ("2dff5f0b44a9e6c8644b2159414af72261e38686072e063aa66ee98a2faecf0e" "24714e2cb4a9d6ec1335de295966906474fdb668429549416ed8636196cb1441" "bffa9739ce0752a37d9b1eee78fc00ba159748f50dc328af4be661484848e476" default)))
 '(hl-todo-keyword-faces
   (quote
    (("TODO" . "#dc752f")
     ("NEXT" . "#dc752f")
     ("THEM" . "#2d9574")
     ("PROG" . "#4f97d7")
     ("OKAY" . "#4f97d7")
     ("DONT" . "#f2241f")
     ("FAIL" . "#f2241f")
     ("DONE" . "#86dc2f")
     ("NOTE" . "#b1951d")
     ("KLUDGE" . "#b1951d")
     ("HACK" . "#b1951d")
     ("TEMP" . "#b1951d")
     ("FIXME" . "#dc752f")
     ("XXX+" . "#dc752f")
     ("\\?\\?\\?+" . "#dc752f"))))
 '(package-selected-packages
   (quote
    (key-chord hl-todo evil-org org-bullets beacon nlinum-relative evil-escape dracula-theme spacemacs-theme which-key use-package evil)))
 '(pdf-view-midnight-colors (quote ("#b2b2b2" . "#292b2e"))))
(custom-set-faces
 ;; custom-set-faces was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(default ((t (:inherit nil :stipple nil :inverse-video nil :box nil :strike-through nil :overline nil :underline nil :slant normal :weight normal :height 113 :width normal :foundry "BE5N" :family "Iosevka")))))
