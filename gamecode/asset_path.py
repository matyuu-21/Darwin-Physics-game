import sys
from pathlib import Path

def asset_path(relative_path):
    base = getattr(sys, "_MEIPASS", None)
    base = Path(base) if base else Path(__file__).resolve().parent.parent
    return str(base / relative_path)