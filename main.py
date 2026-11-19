#!/usr/bin/env python3
"""Entry for make.fun news-image-20261119.

Copies the committed entry.png (a one-image summary of world news on
Thursday 19 November 2026, drawn by draw_image.py) to the output
directory. Standard library only; deterministic.
"""

import os
import shutil
from pathlib import Path


def main() -> None:
    here = Path(__file__).resolve().parent
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(here / "entry.png", out_dir / "entry.png")


if __name__ == "__main__":
    main()
