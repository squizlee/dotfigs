import sys
import os
from pathlib import Path
import platform
import errno

def force_symlink(target: Path, link_name: Path):
    try:
        os.symlink(target, link_name)
    except OSError as e:
        if e.errno == errno.EEXIST:
            os.remove(link_name)
            os.symlink(target, link_name)
        else:
            raise e

def main() -> int:
    if platform.system() not in ['Linux', 'Darwin']:
        print('Unsupported platform', file=sys.stderr)
        return -1

    dotfigs_dir = Path(__file__).resolve().parent
    emacs_dir = dotfigs_dir / 'emacs'

    home = Path.home()
    Path(home / '.config').mkdir(parents=True, exist_ok=True)

    Path(home / '.config' / 'emacs').mkdir(parents=True, exist_ok=True)
    force_symlink(Path(emacs_dir / 'init.el'), Path(home / '.config' / 'emacs' / 'init.el'))

    return 0


if __name__ == '__main__':
    sys.exit(main())
