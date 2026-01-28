import pandas as pd
import re
from collections import Counter

# ----------------------------
# 1) Load data
# ----------------------------
df = pd.read_excel("freewill.xlsx")

TEXT_COL = "text context"
COND_COL = "status 1 profreewill 2 antifreewill"

# ----------------------------
# 2) Stopwords
#    A) Basic function words
#    B) Discourse/glue words that often pollute qualitative interpretation
# ----------------------------
STOPWORDS_TR = {
    "ve", "bir", "bu", "şu", "o", "da", "de", "için", "ile", "ama", "çünkü",
    "ben", "bana", "benim", "sen", "sana", "senin", "biz", "bizi", "bizim",
    "siz", "sizi", "sizin", "onlar", "onlara", "onların",
    "mi", "mı", "mu", "mü",
    "ne", "niye", "neden", "nasıl", "ki",
    "i", "İ"
}

DISCOURSE_STOPWORDS = {
    # common glue / vague / meta words
    "kendi", "kendim", "bunun", "şunun",
    "şey", "şeyler",
    "sadece", "değil",
    "olan", "olarak",
    "olduğunu", "olduğu", "oluyor", "olması",
    "çok", "daha", "kadar", "göre",
    "gün", "zaman", "bazen"
}

# ----------------------------
# 3) Tokenizer
# ----------------------------
def tokenize_tr(text: str):
    text = str(text).lower()
    # keep Turkish letters, remove punctuation/numbers
    text = re.sub(r"[^a-zçğıöşü]+", " ", text)

    tokens = [
        t for t in text.split()
        if len(t) >= 2 and t not in STOPWORDS_TR and t not in DISCOURSE_STOPWORDS
    ]
    return tokens

def make_bigrams(tokens):
    return [f"{tokens[i]} {tokens[i+1]}" for i in range(len(tokens) - 1)]

# ----------------------------
# 4) Build counters (unigrams + bigrams) per condition
# ----------------------------
conds = sorted(df[COND_COL].unique())

uni_counters = {}
bi_counters = {}

for cond in conds:
    sub = df[df[COND_COL] == cond]

    uni_all = []
    bi_all = []

    for t in sub[TEXT_COL].fillna(""):
        toks = tokenize_tr(t)
        uni_all.extend(toks)
        bi_all.extend(make_bigrams(toks))

    uni_counters[cond] = Counter(uni_all)
    bi_counters[cond] = Counter(bi_all)

# ----------------------------
# 5) Helper: common words/phrases (intersection) ranked by combined frequency
# ----------------------------
def top_common(counter_dict, topn=20):
    c_list = list(counter_dict.keys())
    common = set(counter_dict[c_list[0]].keys())
    for c in c_list[1:]:
        common &= set(counter_dict[c].keys())

    combined = Counter()
    for c in c_list:
        combined += counter_dict[c]

    ranked = sorted([(w, combined[w]) for w in common], key=lambda x: x[1], reverse=True)[:topn]
    return ranked

# ----------------------------
# 6) Helper: distinctiveness (normalized difference)
# ----------------------------
def distinctive_top(counter_dict, topn=10):
    cA, cB = list(counter_dict.keys())  # assumes 2 conditions
    totalA = sum(counter_dict[cA].values())
    totalB = sum(counter_dict[cB].values())

    all_items = set(counter_dict[cA].keys()) | set(counter_dict[cB].keys())
    scores = []
    for item in all_items:
        fa = counter_dict[cA][item] / totalA if totalA > 0 else 0
        fb = counter_dict[cB][item] / totalB if totalB > 0 else 0
        scores.append((item, fa - fb))

    topA = sorted(scores, key=lambda x: x[1], reverse=True)[:topn]
    topB = sorted(scores, key=lambda x: x[1])[:topn]
    return topA, topB

# ----------------------------
# 7) Print results: UNIGRAMS
# ----------------------------
print("\n" + "=" * 50)
print("UNIGRAMS — TOP 20 PER CONDITION (stopwords + discourse words removed)")

for cond in conds:
    print("\n" + "-" * 50)
    print(f"Condition {cond} TOP 20 (unigrams)")
    for w, c in uni_counters[cond].most_common(20):
        print(f"{w:20} {c}")

print("\n" + "-" * 50)
print("UNIGRAMS — TOP 20 COMMON (shared across conditions)")
for w, c in top_common(uni_counters, topn=20):
    print(f"{w:20} {c}")

# Distinctive unigrams
topA_uni, topB_uni = distinctive_top(uni_counters, topn=10)

print("\n" + "-" * 50)
print("UNIGRAMS — TOP 10 DISTINCTIVE FOR Condition 1.0 (higher in 1.0 than 2.0)")
for w, s in topA_uni:
    print(f"{w:20} {s:.6f}")

print("\n" + "-" * 50)
print("UNIGRAMS — TOP 10 DISTINCTIVE FOR Condition 2.0 (higher in 2.0 than 1.0)")
for w, s in topB_uni:
    print(f"{w:20} {abs(s):.6f}")

# ----------------------------
# 8) Print results: BIGRAMS (phrases)
# ----------------------------
print("\n" + "=" * 50)
print("BIGRAMS — TOP 20 PER CONDITION (phrases)")

for cond in conds:
    print("\n" + "-" * 50)
    print(f"Condition {cond} TOP 20 (bigrams)")
    for w, c in bi_counters[cond].most_common(20):
        print(f"{w:25} {c}")

# Distinctive bigrams
topA_bi, topB_bi = distinctive_top(bi_counters, topn=10)

print("\n" + "-" * 50)
print("BIGRAMS — TOP 10 DISTINCTIVE FOR Condition 1.0")
for w, s in topA_bi:
    print(f"{w:25} {s:.6f}")

print("\n" + "-" * 50)
print("BIGRAMS — TOP 10 DISTINCTIVE FOR Condition 2.0")
for w, s in topB_bi:
    print(f"{w:25} {abs(s):.6f}")
# ----------------------------
# 9) SAVE DISTINCTIVE RESULTS FOR PLOTTING
# ----------------------------

# Top 5 distinctive unigrams
top5_cond1 = topA_uni[:5]
top5_cond2 = topB_uni[:5]

# Convert to DataFrames for easy reuse
df_plot_cond1 = pd.DataFrame(top5_cond1, columns=["word", "score"])
df_plot_cond2 = pd.DataFrame(top5_cond2, columns=["word", "score"])

# Save to CSV
df_plot_cond1.to_csv("distinctive_unigrams_cond1_top5.csv", index=False)
df_plot_cond2.to_csv("distinctive_unigrams_cond2_top5.csv", index=False)
