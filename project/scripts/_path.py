"""Imported first by every script: puts project/ on the import path so `fars` imports."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
