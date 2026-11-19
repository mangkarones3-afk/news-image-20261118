#!/usr/bin/env python3
"""Entry program for the make.fun bounty "news-image-20261118".

Writes the one-image summary of the world news of Wednesday 18 November 2026
to /output/entry.png. The finished image ships with this repository as
``entry.png`` next to this file; the program simply copies it into place.

Standard library only. No network access.
"""

from pathlib import Path
import shutil

ASSET = Path(__file__).resolve().parent / "entry.png"
OUTPUT = Path("/output/entry.png")


def main() -> None:
    if not ASSET.is_file():
        raise SystemExit(f"asset not found: {ASSET}")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ASSET, OUTPUT)
    written = OUTPUT.stat().st_size
    expected = ASSET.stat().st_size
    if written != expected:
        raise SystemExit(f"copy incomplete: wrote {written} of {expected} bytes")
    print(f"wrote {OUTPUT} ({written} bytes, matches asset)")


if __name__ == "__main__":
    main()
