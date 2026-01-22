# versioning.py

import sys
from pathlib import Path
import os

from build_core import update_version, StrictError


def get_required_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def main() -> int:
    try:
        source_path = Path(get_required_env("SourcePath"))
        build_num = get_required_env("BuildNum")

        results = update_version(source_path, build_num)

        for fname, changed in results.items():
            print(f"{'UPDATED' if changed else 'OK'}: {fname}")

        return 0

    except StrictError as e:
        print(f"ERROR (strict mode): {e}", file=sys.stderr)
        return 4
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
