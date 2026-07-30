from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


def write_generated_content_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    """Write generated content metadata for later Excel / SharePoint import."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    fields = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
