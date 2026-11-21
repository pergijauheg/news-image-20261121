#!/usr/bin/env python3
"""The Saturday Globe — one-page newspaper for 21 November 2026.

Copies the bundled front-page image (entry.png) to /output/entry.png.
This program uses only the Python standard library, so it runs in the
grader even without Pillow installed.

The artwork itself is generated at build time by draw.py (Pillow), which
lives in this repository for provenance; the generated entry.png is what
this program ships.
"""

import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        sys.stderr.write("entry.png not found next to main.py\n")
        return 1
    outdir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    dst = os.path.join(outdir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote", dst, os.path.getsize(dst), "bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
