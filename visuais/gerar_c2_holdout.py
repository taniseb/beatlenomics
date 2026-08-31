"""Post C2 — the holdout question that data can't honestly answer
NOT a counterfactual projection. Spotify publishes no historical
per-artist stream series, so there is no observed trajectory to fit
a "what if they'd joined earlier" curve against. This chart shows only
what is real and dated: streaming entry dates for The Beatles and three
comparable legacy catalogues, plus the two dated Beatles milestones
that exist in the press record.
Fontes: posts/c2-spotify-holdout/referencias.md
"""
import pandas as pd
import matplotlib.dates as mdates
from beatlenomics_style import make_canvas, VERMELHO, AZUL, PRETO, CINZA

entradas = pd.DataFrame([
    ("Pink Floyd", "2013-06-17"),
    ("Led Zeppelin", "2013-12-13"),
    ("AC/DC", "2015-06-01"),
    ("The Beatles", "2015-12-24"),
], columns=["artista", "data"])
entradas["data"] = pd.to_datetime(entradas["data"])

marcos = pd.DataFrame([
    ("100 days: 6.5M monthly listeners", "2016-04-03"),
    ("\"Here Comes the Sun\" hits 1B streams", "2023-05-09"),
], columns=["marco", "data"])
marcos["data"] = pd.to_datetime(marcos["data"])

fig, ax = make_canvas(
    "The curve this post doesn't draw",
    "Streaming entry dates for four legacy catalogues. No trajectory line: Spotify keeps no\npublic historical stream series, so there is no honest counterfactual to plot.",
    figsize=(11, 6.5))
ax.set_position([0.09, 0.20, 0.86, 0.48])

y_map = {"Pink Floyd": 3, "Led Zeppelin": 2, "AC/DC": 1, "The Beatles": 0}
for _, r in entradas.iterrows():
    color = VERMELHO if r["artista"] == "The Beatles" else CINZA
    y = y_map[r["artista"]]
    ax.scatter([r["data"]], [y], s=140, color=color, zorder=3)
    ax.text(r["data"], y + 0.28, r["artista"], ha="center", fontsize=10.5,
             fontweight="bold" if color == VERMELHO else "normal",
             color=PRETO, family="DejaVu Sans")

for _, r in marcos.iterrows():
    ax.scatter([r["data"]], [0], s=70, marker="D", color=AZUL, zorder=4)
    ax.annotate(r["marco"], (r["data"], 0), xytext=(0, -38), textcoords="offset points",
                ha="center", fontsize=9, color=AZUL, family="DejaVu Sans",
                arrowprops=dict(arrowstyle="-", color=AZUL, lw=0.9))

ax.set_ylim(-1.1, 3.9)
pad = pd.Timedelta(days=200)
ax.set_xlim(entradas["data"].min() - pad, marcos["data"].max() + pd.Timedelta(days=650))
ax.set_yticks([])
for spine in ("left", "top", "right"):
    ax.spines[spine].set_visible(False)
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
ax.tick_params(axis="x", colors=CINZA)

fig.text(0.09, 0.10,
         "Zeppelin and Pink Floyd beat the Beatles to streaming by about two years. AC/DC, six months.",
         color=PRETO, fontsize=11, family="DejaVu Sans")
fig.text(0.09, 0.07,
         "Not a decade of missed comparison. A cluster of holdouts, arriving within three years of each other.",
         color=PRETO, fontsize=11, family="DejaVu Sans")

out = "visuais/c2_holdout.png"
fig.savefig(out, dpi=200)
print("salvo:", out)
