import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------
# Load computed results
# ----------------------------
pro = pd.read_csv("distinctive_unigrams_cond1_top5.csv")
anti = pd.read_csv("distinctive_unigrams_cond2_top5.csv")

# Make anti scores positive for visual symmetry
anti["score"] = anti["score"].abs()

# ----------------------------
# Global style
# ----------------------------
plt.rcParams.update({
    "font.size": 11,
    "axes.titlesize": 14,
    "axes.labelsize": 11,
    "xtick.labelsize": 10,
    "ytick.labelsize": 11
})

def lollipop(ax, df, title, color):
    y = range(len(df))

    # Lines
    ax.hlines(
        y=y,
        xmin=0,
        xmax=df["score"],
        color=color,
        linewidth=2,
        alpha=0.8
    )

    # Dots
    ax.plot(
        df["score"],
        y,
        "o",
        color=color,
        markersize=8
    )

    ax.set_yticks(y)
    ax.set_yticklabels(df["word"])
    ax.invert_yaxis()

    # Clean look
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)

    ax.grid(axis="x", linestyle=":", alpha=0.4)

    ax.set_title(title, weight="bold", pad=10)
    ax.set_xlabel("Distinctiveness score")

    max_val = df["score"].max()
    pad = max_val * 0.04

    # Value labels
    for i, val in enumerate(df["score"]):
        ax.text(
            val + pad,
            i,
            f"{val:.4f}",
            va="center",
            fontsize=10,
            color="#333333"
        )

    ax.set_xlim(0, max_val * 1.3)

# ----------------------------
# Figure
# ----------------------------
fig, axes = plt.subplots(1, 2, figsize=(12.5, 6))

fig.suptitle(
    "Distinctive Language in Free-Will Explanations (Top 5)",
    fontsize=17,
    weight="bold",
    y=0.97
)

lollipop(
    axes[0],
    pro,
    "Condition 1.0 — Pro Free Will",
    color="#4C72B0"  # muted blue
)

lollipop(
    axes[1],
    anti,
    "Condition 2.0 — Anti Free Will",
    color="#C44E52"  # muted red
)

fig.text(
    0.5,
    0.03,
    "Distinctiveness = normalized frequency difference between conditions.",
    ha="center",
    fontsize=10,
    color="#555555"
)

plt.tight_layout(rect=[0, 0.06, 1, 0.93])
plt.show()

# Optional export:
# fig.savefig("distinctive_unigrams_lollipop.png", dpi=300, bbox_inches="tight")
