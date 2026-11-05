import json
import matplotlib.pyplot as plt
import mplcursors
from IPython import get_ipython
import numpy as np
import pandas as pd


def enable_interactive():
    """Equivalent of `%matplotlib widget` (needs ipympl installed)."""
    ip = get_ipython()
    if ip is None:
        raise RuntimeError("Must be called from a Jupyter/IPython session")
    ip.run_line_magic("matplotlib", "widget")


def interactive_jupyter_plot(x, y):
    """
    Plot x, y; click points to select them. Returns (fig, picked_points).
    Updates automatically as you click or unclick points. Use mplcursors to select multiple points.
    """
    enable_interactive()          # must run BEFORE the figure is created
    fig, ax = plt.subplots()
    line, = ax.plot(x, y)

    picked = []                   # filled live as you click

    cursor = mplcursors.cursor(line, multiple=True)

    @cursor.connect("add")
    def on_add(sel):
        px, py = sel.target
        picked.append((float(px), float(py)))
        picked.sort(key=lambda p: p[0])  # sort on x only
        sel.annotation.set_text(f"x={px:.4g}\ny={py:.4g}")

    @cursor.connect("remove")
    def on_remove(sel):
        pt = (float(sel.target[0]), float(sel.target[1]))
        if pt in picked:
            picked.remove(pt)

    return fig, picked

def save_selected_points(config, selected_points):
    with open(rf"C:\Users\Client\Documents\Calibration_ISF\Data\ForceDisplacement\Config{config}\selected_points_config{config}.json", "w") as f:
        json.dump(selected_points, f)
    print(f"Saved {len(selected_points)} points to selected_points_config{config}.json")

def load_selected_points(config):
    with open(rf"C:\Users\Client\Documents\Calibration_ISF\Data\ForceDisplacement\Config{config}\selected_points_config{config}.json") as f:
        return [tuple(p) for p in json.load(f)]


def slice_load_cell_data(selected_points, data):
    """
    Averages every column of `data` over each range defined by consecutive pairs of
    selected points. Ranges are taken on column "Time" (pair of points -> [x_start, x_end]).

    Returns a DataFrame with the same columns as `data`, one row per pair.
    """
    selected_points.sort(key=lambda p: p[0])  # in place, ascending x only (y ignored)

    if len(selected_points) % 2 != 0:
        print(f"Warning: {len(selected_points)} points selected, last unpaired point ignored.")

    rows = []
    for i in range(0, len(selected_points) - 1, 2):
        x_start, x_end = sorted((selected_points[i][0], selected_points[i + 1][0]))
        in_range = (data["Time"] >= x_start) & (data["Time"] <= x_end)
        rows.append(data.loc[in_range].mean(numeric_only=True))

        print(f"Pair {i // 2}: Time in [{x_start:.1f}, {x_end:.1f}] ({in_range.sum()} samples)")

    return pd.DataFrame(rows, columns=data.columns).reset_index(drop=True)
