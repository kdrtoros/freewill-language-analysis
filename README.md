# freewill-text-viz

Exploratory Python scripts for analyzing and visualizing linguistic patterns in open-ended free-will explanations across experimental conditions.

---

## Overview

This repository contains a small, modular pipeline for **exploratory text analysis** of open-ended responses collected in a psychology experiment on **free will and moral cognition**.

Participants were asked to explain why free will is (or is not) compatible with their own lives. The scripts in this repository analyze **aggregate, anonymized language patterns** across experimental conditions, focusing on:

- **Shared vocabulary** between conditions (proportional usage)
- **Condition-distinctive terms** (relative frequency differences)

The goal is **methodological exploration and visualization**, not confirmatory hypothesis testing.

---

## Important Notes on Scope and Ethics

- All analyses are **post-hoc and exploratory**
- They were **not preregistered** and **not part of confirmatory hypothesis tests**
- No raw participant data are included in this repository
- All figures are generated from **aggregate statistics**
- Participants provided informed consent for anonymized scientific use of their data

This repository is intended to demonstrate **computational approaches to qualitative data** in social and moral psychology.

##Compute word frequencies

python 02_word_counts.py

##Visualize shared vocabulary

python 03_plot_shared_donut.py

##Visualize distinctive language

python 04_plot_distinctive_lollipop.py
Dependencies

Python 3.9 or later

pandas

matplotlib

openpyxl (for local Excel-based workflows)

Install dependencies with:

pip install -r requirements.txt

Language Notes

The original data were collected in Turkish.
Visualizations therefore include Turkish surface forms (e.g., kendi, karar, iyi/kötü).

When figures are shared publicly, a mini-glossary is provided to support non-Turkish readers.

Use of Generative AI

ChatGPT (version 5.2) was used to assist with:

drafting and refactoring Python code

data normalization logic

visualization design

All analytical decisions, interpretations, and ethical judgments remain the responsibility of the author.

License

This project is shared for academic and educational purposes.
If you reuse or adapt the code, please cite appropriately.

Contact

Kadir Toros
kdrtoros@gmail.com
