"""Post — The setlist is made of blocks
Hierarchical clustering (average linkage) on Paul McCartney's live setlist
position, 13 shows Tanise attended (2010-2024). Distance between two songs
= mean absolute difference in normalized set position, across shows where
both appear. Songs in fewer than 5 of the 13 shows excluded (44 of 85 kept).
Cut at k=4: three contiguous positional blocks (opener / middle / encore)
plus a 4th non-contiguous group of "wildcard" songs whose position swings
wildly show to show, the exception that proves the block structure.
Dado: dados/meus_13_shows_musicas.csv -> dados/paul_setlist_blocos.csv.
Fontes: posts/setlist-blocos/referencias.md.
"""
import pandas as pd
from beatlenomics_style import make_canvas, VERMELHO, AZUL, LARANJA, PRETO, CINZA

df = pd.read_csv("dados/paul_setlist_blocos.csv").sort_values("mean")
cores = {1: AZUL, 2: LARANJA, 3: VERMELHO, 4: "#9A9A98"}
nomes = {1: "Opener", 2: "Middle", 3: "Encore block", 4: "Wildcards (no fixed slot)"}

fig, ax = make_canvas(
    "The setlist is made of blocks",
    "Position of each song in the set, across the 13 Paul McCartney shows I've seen (2010-2024).\nDots = average position; bars = the full range across shows. Songs in <5 of 13 shows excluded.",
    figsize=(11, 13))
ax.set_position([0.30, 0.16, 0.66, 0.58])

y = range(len(df))
for yi, (_, r) in zip(y, df.iterrows()):
    color = cores[r["cluster"]]
    ax.plot([r["min"] * 100, r["max"] * 100], [yi, yi], color=color, lw=4, alpha=0.55, zorder=2, solid_capstyle="round")
    ax.scatter([r["mean"] * 100], [yi], color=color, s=36, zorder=3)

ax.set_yticks(list(y))
ax.set_yticklabels(df["musica"], fontsize=8.3, family="DejaVu Sans")
ax.set_xlim(0, 100)
ax.set_xlabel("Position in the set (%)", color=CINZA, fontsize=10.5)
for spine in ("top", "right"):
    ax.spines[spine].set_visible(False)

handles = [plt_line for plt_line in []]
import matplotlib.lines as mlines
handles = [mlines.Line2D([], [], color=cores[c], marker="o", lw=4, alpha=0.7, markersize=7, label=nomes[c])
           for c in [1, 2, 3, 4]]
ax.legend(handles=handles, loc="lower right", frameon=False, fontsize=9.5)

fig.text(0.09, 0.10,
         "The encore trio (Golden Slumbers, Carry That Weight, The End) moved under 5.3% of the set across 13 shows.",
         color=PRETO, fontsize=11, family="DejaVu Sans")
fig.text(0.09, 0.075,
         "Three songs never found a stable slot at all: that inconsistency is the exception that proves the blocks are real.",
         color=PRETO, fontsize=11, family="DejaVu Sans")

out = "visuais/setlist_blocos.png"
fig.savefig(out, dpi=200)
print("salvo:", out)
