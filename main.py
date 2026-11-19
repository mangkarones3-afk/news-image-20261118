"""Deliver the finished news poster to the grader's output folder.

The poster itself ships beside this script as entry.png. Running the
program places a copy of that file where the harness expects to find
it and then proves, by hashing both files, that the copy arrived
byte for byte intact.
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path


POSTER_NAME = "entry.png"
FALLBACK_OUTPUT_DIR = "/output"
CHUNK_SIZE = 64 * 1024


def digest_of(path):
    """Return the SHA-256 hex digest of the file at *path*."""
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            block = handle.read(CHUNK_SIZE)
            if not block:
                break
            hasher.update(block)
    return hasher.hexdigest()


def destination_path():
    """Work out where the poster copy has to land."""
    folder = os.environ.get("MAKEFUN_OUTPUT_DIR") or FALLBACK_OUTPUT_DIR
    return Path(folder) / POSTER_NAME


def main():
    source = Path(__file__).resolve().parent / POSTER_NAME
    if not source.is_file():
        print(f"poster not found beside the script: {source}", file=sys.stderr)
        return 1

    target = destination_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.resolve() != source:
        shutil.copyfile(source, target)
    # When the output folder is the script's own folder the poster is
    # already in place, so copying it onto itself is skipped; the hash
    # check below still proves the file at the destination is intact.

    source_digest = digest_of(source)
    target_digest = digest_of(target)
    if target_digest != source_digest:
        print(
            "copied poster failed verification: "
            f"source sha256 {source_digest} != output sha256 {target_digest}",
            file=sys.stderr,
        )
        return 1

    print(f"entry.png delivered to {target} (sha256 {target_digest})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
