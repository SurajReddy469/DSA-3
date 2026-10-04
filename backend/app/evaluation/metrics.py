import os
import sys
from pathlib import Path
from typing import Dict, Any


def get_file_size_mb(path: Path) -> float:
    """Returns size of a file in Megabytes."""
    if not path.exists():
        return 0.0
    return round(path.stat().st_size / (1024.0 * 1024.0), 3)


def calculate_speedup(naive_time: float, indexed_time: float) -> float:
    """
    Calculates speedup factor: Naive execution time / Indexed execution time.
    """
    if indexed_time <= 0:
        return 1.0
    return round(naive_time / indexed_time, 2)
