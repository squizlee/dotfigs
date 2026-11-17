(require 'package)
(add-to-list 'package-archives
             '("melpa" . "https://melpa.org/packages/"))

;; Initialize use-package
(require 'use-package)
(setq use-package-always-ensure t)

;; Keep Customize output out of this (symlinked, tracked) file.
(setq custom-file (expand-file-name "custom.el" user-emacs-directory))
(load custom-file 'noerror)

;; Load config.org from the same directory as the real (symlink-resolved) init.el
(org-babel-load-file
 (expand-file-name "config.org"
                   (file-name-directory (file-truename load-file-name))))
