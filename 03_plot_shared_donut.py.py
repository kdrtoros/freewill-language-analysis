import pandas as pd
import re
import matplotlib.pyplot as plt

# ============================
# SETTINGS (edit these easily)
# ============================

EXCEL_FILE = "freewill.xlsx"
TEXT_COL = "text context"
COND_COL = "status 1 profreewill 2 antifreewill"

TOP_N = 5  # keep pies small (6–10 is best)

# If you want to remove generic moral evaluation words too, set True
REMOVE_MORAL_WORDS = False

# ============================
# FILTER LISTS
# ============================

# Basic Turkish function words
STOPWORDS_TR = {
    "ve", "bir", "bu", "şu", "o", "da", "de", "için", "ile", "ama", "çünkü",
    "ben", "bana", "benim", "sen", "sana", "senin", "biz", "bizi", "bizim",
    "siz", "sizi", "sizin", "onlar", "onlara", "onların",
    "mi", "mı", "mu", "mü",
    "ne", "niye", "neden", "nasıl", "ki"
}

# Free-will concept words you want to exclude
EXCLUDE_CONCEPT_WORDS = {
    "özgür", "özgürlük",
    "irade", "iradem", "irademi", "iradeye", "iradeyi",
    "özgürirade",
    "determinist", "determinizm", "kader",
    "kontrol", "seçim", "seçmek",
    "ajan", "fail", "sorumluluk", "sorumlu"
}

# Shared-vocab chart “banned” list (glue/discourse words)
BANNED_SHARED = {
    "ya", "her", "veya", "örneğin", "verirken",
    "sadece", "değil", "olan", "olarak", "olduğunu", "olduğu", "oluyor", "olması",
    "çok", "daha", "kadar", "göre", "bazen", "zaman", "gün"
}

# Optionally ban moral words
if REMOVE_MORAL_WORDS:
    BANNED_SHARED.update({"iyi", "kötü", "doğru"})

# ============================
# TOKENIZER
# ============================

def tokenize_tr(text):
    text = str(text).lower()
    # keep letters incl Turkish, replace everything else with spaces
    text = re.sub(r"[^a-zçğıöşü]+", " ", text)

    tokens = []
    for t in text.split():
        # length filter helps remove some noise
        if len(t) < 3:
            continue
        if t in STOPWORDS_TR:
            continue
        if t in EXCLUDE_CONCEPT_WORDS:
            continue
        tokens.append(t)
    return tokens

# ============================
# MAIN
# ============================

df = pd.read_excel(EXCEL_FILE)
conds = sorted(df[COND_COL].unique())

# Build word frequency per condition
freq = {}
for cond in conds:
    toks = []
    for txt in df[df[COND_COL] == cond][TEXT_COL].fillna(""):
        toks.extend(tokenize_tr(txt))
    freq[cond] = pd.Series(toks).value_counts()

# Compute shared words (intersection)
shared = set(freq[conds[0]].index)
for cond in conds[1:]:
    shared &= set(freq[cond].index)

# Filter shared words further (remove glue words)
shared = [w for w in shared if w not in BANNED_SHARED]

if len(shared) == 0:
    raise ValueError(
        "After filtering, no shared words remained. "
        "Try lowering filters (e.g., REMOVE_MORAL_WORDS=False or remove items from BANNED_SHARED)."
    )

# Rank shared words by combined frequency across conditions
combined = {w: int(freq[conds[0]].get(w, 0) + freq[conds[1]].get(w, 0)) for w in shared}
top_shared = sorted(shared, key=lambda w: combined[w], reverse=True)[:TOP_N]

# Normalize within each condition (so pies are comparable)
vals_1 = freq[conds[0]].reindex(top_shared).fillna(0)
vals_2 = freq[conds[1]].reindex(top_shared).fillna(0)

if vals_1.sum() == 0 or vals_2.sum() == 0:
    raise ValueError("One condition has zero counts for the selected shared words. Increase TOP_N or relax filters.")

vals_1 = vals_1 / vals_1.sum()
vals_2 = vals_2 / vals_2.sum()

# ============================
# PLOT: DONUTS
# ============================

plt.rcParams.update({
    "font.size": 11,
    "axes.titlesize": 13
})

fig, axes = plt.subplots(1, 2, figsize=(12.5, 6))
colors = plt.cm.Set2.colors  # modern palette

def donut(ax, values, labels, title):
    wedges, texts, autotexts = ax.pie(
        values,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90,
        colors=colors,
        pctdistance=0.75,
        textprops={"fontsize": 10}
    )
    # donut hole
    centre = plt.Circle((0, 0), 0.55, fc="white")
    ax.add_artist(centre)
    ax.set_title(title, weight="bold", pad=12)
    ax.axis("equal")

donut(axes[0], vals_1.values, top_shared, f"Condition {conds[0]} — Pro Free Will")
donut(axes[1], vals_2.values, top_shared, f"Condition {conds[1]} — Anti Free Will")

subtitle = "Shared Non-Concept Vocabulary (Proportional Distribution)"
if REMOVE_MORAL_WORDS:
    subtitle += " — moral words removed"

fig.suptitle(subtitle, fontsize=16, weight="bold", y=0.96)

plt.tight_layout()
plt.show()

# Optional export:
# fig.savefig("shared_words_donut_filtered.png", dpi=300, bbox_inches="tight")
