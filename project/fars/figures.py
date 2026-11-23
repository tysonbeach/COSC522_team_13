"""Matplotlib set up for file output only (no plot windows)."""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from .config import PROJECT_DIR  # noqa: E402


def save_fig(fig, path):
    """Save a figure as a PNG (creating its folder) and close it."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved figure: {path.relative_to(PROJECT_DIR)}")
