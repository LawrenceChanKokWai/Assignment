import os
import sys
from pathlib import Path

from build_core import update_version


def main() -> int:
    source_path = os.environ.get("SourcePath")
    build_num = os.environ.get("BuildNum")

    if not source_path:
        print("ERROR: SourcePath environment variable is not set", file=sys.stderr)
        return 2
    if not build_num:
        print("ERROR: BuildNum environment variable is not set", file=sys.stderr)
        return 2

    results = update_version(Path(source_path), build_num)

    for name, changed in results.items():
        print(f"{'UPDATED' if changed else 'NO CHANGE'}: {name}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
