#!/usr/bin/env python3
"""Rebuild notebooks/training_and_evaluation_pipeline.ipynb from notebooks/src/."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
OUT = ROOT / "training_and_evaluation_pipeline.ipynb"


def main() -> None:
    manifest = json.loads((SRC / "manifest.json").read_text(encoding="utf-8"))
    cells = []
    for item in manifest:
        text = (SRC / item["file"]).read_text(encoding="utf-8")
        cell = {
            "cell_type": item["type"],
            "metadata": {},
            "source": text.splitlines(True),
        }
        if item["type"] == "code":
            cell["outputs"] = []
            cell["execution_count"] = None
        cells.append(cell)
    nb = {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python"},
        },
        "cells": cells,
    }
    OUT.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes, {len(cells)} cells)")


if __name__ == "__main__":
    main()
