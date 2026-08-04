(require 'package)
(add-to-list 'package-archives
             '("melpa" . "https://melpa.org/packages/"))

;; Initialize use-package
(require 'use-package)
(setq use-package-always-ensure t)

;; Load config.org for init.el configuration
(org-babel-load-file (expand-file-name "~/dotfigs/emacs/config.org"))
