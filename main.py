#!/usr/bin/env python3
"""Entrypoint for the news-image-20261118 entry.

The finished poster lives next to this file as ``entry.png``. Running
the program copies that asset into the output directory, producing
``/output/entry.png``. Standard library only; no network access.
"""

import hashlib
import os
import sys

ASSET_FILENAME = "entry.png"
OUTPUT_DIR = "/output"
OUTPUT_FILENAME = "entry.png"
BLOCK = 65536


def asset_path():
    folder = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(folder, ASSET_FILENAME)


def destination_path():
    return os.path.join(OUTPUT_DIR, OUTPUT_FILENAME)


def digest_of(path):
    hasher = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            piece = handle.read(BLOCK)
            if not piece:
                break
            hasher.update(piece)
    return hasher.hexdigest()


def copy_asset(source, target):
    moved = 0
    with open(source, "rb") as reader, open(target, "wb") as writer:
        while True:
            piece = reader.read(BLOCK)
            if not piece:
                break
            writer.write(piece)
            moved += len(piece)
    return moved


def run():
    source = asset_path()
    if not os.path.isfile(source):
        sys.stderr.write("missing asset: %s\n" % source)
        return 1
    if not os.path.isdir(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    target = destination_path()
    nbytes = copy_asset(source, target)
    source_digest = digest_of(source)
    written_digest = digest_of(target)
    if written_digest != source_digest:
        sys.stderr.write(
            "digest mismatch: source %s, written %s\n"
            % (source_digest, written_digest)
        )
        return 1
    print("copied %d bytes -> %s" % (nbytes, target))
    print("sha256 %s" % written_digest)
    return 0


if __name__ == "__main__":
    sys.exit(run())
