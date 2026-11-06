"""Summary figure for the README: Simon's algorithm (n = 3, secret s = 010) on FakeQmio and Qmio.

Counts are copied from the outputs of notebook/simon_algorithm_qmio.ipynb (100 shots each),
with the bit order of the notebook (after reverse_bitstrings).
Usage: python figures/make_simon_figure.py  (writes the PNGs next to this script)
"""
import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

out_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))

allowed = ["000", "001", "100", "101"]    # s . y = 0 for s = 010
forbidden = ["010", "011", "110", "111"]  # s . y = 1
fake = {"000": 25, "001": 29, "100": 25, "101": 21}
qmio = {"000": 33, "001": 14, "100": 22, "101": 20, "010": 2, "110": 6, "111": 3}
labels = allowed + forbidden
x = np.arange(len(labels))
w = 0.38

themes = {
    "light": dict(bg="#ffffff", fg="#1f2328", muted="#59636e", grid="#d1d9e0", region="#f6f8fa",
                  s1="#2a78d6", s2="#eb6834"),
    "dark": dict(bg="#0d1117", fg="#e6edf3", muted="#9198a1", grid="#3d444d", region="#161b22",
                 s1="#3987e5", s2="#d95926"),
}

for name, t in themes.items():
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 11, "mathtext.fontset": "dejavusans",
        "text.color": t["fg"], "axes.labelcolor": t["fg"], "xtick.color": t["fg"], "ytick.color": t["muted"],
        "axes.edgecolor": t["grid"], "figure.facecolor": t["bg"], "axes.facecolor": t["bg"],
    })
    fig, ax = plt.subplots(figsize=(9, 4.2))
    ax.axvspan(3.5, 7.6, color=t["region"], zorder=0)
    ax.axvline(3.5, color=t["muted"], lw=1.0, zorder=1)
    xf = [i for i, k in enumerate(labels) if fake.get(k, 0)]
    xq = [i for i, k in enumerate(labels) if qmio.get(k, 0)]
    ax.bar(np.array(xf) - w / 2 - 0.01, [fake[labels[i]] for i in xf], w, color=t["s1"], label="FakeQmio (noisy emulator)",
           edgecolor=t["bg"], linewidth=2, zorder=3)
    ax.bar(np.array(xq) + w / 2 + 0.01, [qmio[labels[i]] for i in xq], w, color=t["s2"], label="Qmio (real QPU)",
           edgecolor=t["bg"], linewidth=2, zorder=3)
    ax.text(1.5, 41, r"allowed: $s\cdot y = 0$" + "\nFakeQmio 100/100 · Qmio 89/100", ha="center", va="top",
            fontsize=10, color=t["muted"])
    ax.text(5.55, 41, r"forbidden: $s\cdot y = 1$" + "\nQmio 11/100 (noise)", ha="center", va="top",
            fontsize=10, color=t["muted"])
    ax.set_xticks(x, [f"$y={k}$" for k in labels])
    ax.set_xlim(-0.6, 7.6)
    ax.set_ylim(0, 42)
    ax.set_ylabel("counts (100 shots)")
    ax.grid(axis="y", color=t["grid"], lw=0.6, zorder=0)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.tick_params(length=0, pad=6)
    ax.set_title(r"Simon's algorithm, $n=3$, secret $s=010$: measured bitstrings $y$", fontsize=12, loc="left",
                 color=t["fg"], pad=10)
    leg = ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=2, frameon=False, fontsize=10)
    for txt in leg.get_texts():
        txt.set_color(t["fg"])
    fig.tight_layout()
    fig.savefig(f"{out_dir}/simon_{name}.png", dpi=150, facecolor=t["bg"])
    plt.close(fig)
print("ok")
