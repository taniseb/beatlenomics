"""Post - If Abbey Road dropped today, would it chart?
Grafico da mudanca de regra do Billboard 200 (streams por unidade-equivalente
de album): 1.250/3.750 (ate jan/2026) vs 1.000/2.500 (vigente). Ancora factual
do post, nao a especulacao sobre o medley.
Fontes: posts/abbey-road-hoje/referencias.md.
"""
from beatlenomics_style import make_canvas, VERMELHO, AZUL, PRETO, CINZA

fig, ax = make_canvas(
    "The bar to chart keeps dropping",
    "Streams needed to count as one album-equivalent unit, Billboard 200",
    figsize=(10, 7.5))
ax.set_position([0.14, 0.20, 0.80, 0.52])

grupos = ["Paid / subscription\nstreams", "Ad-supported\nstreams"]
antes = [1250, 3750]
depois = [1000, 2500]

import numpy as np
x = np.arange(len(grupos))
w = 0.32
ax.bar(x - w/2, antes, width=w, color=CINZA, label="Until Jan 2026", zorder=3)
ax.bar(x + w/2, depois, width=w, color=VERMELHO, label="From Jan 2026", zorder=3)

for xi, v in zip(x - w/2, antes):
    ax.text(xi, v + 60, f"{v:,}", ha="center", va="bottom", fontsize=10.5,
            fontweight="bold", color=PRETO, family="DejaVu Sans")
for xi, v in zip(x + w/2, depois):
    ax.text(xi, v + 60, f"{v:,}", ha="center", va="bottom", fontsize=10.5,
            fontweight="bold", color=PRETO, family="DejaVu Sans")

ax.set_xticks(list(x))
ax.set_xticklabels(grupos, fontsize=10.5, family="DejaVu Sans")
ax.set_ylabel("Streams = 1 album-equivalent unit", color=CINZA, fontsize=10.5)
ax.set_ylim(0, 4200)
ax.legend(loc="upper right", frameon=False, fontsize=10)
for spine in ("top", "right"):
    ax.spines[spine].set_visible(False)

fig.text(0.14, 0.10,
         "Streams now convert to units faster, so streaming counts for more against sales than it used to.",
         color=PRETO, fontsize=11, family="DejaVu Sans")
fig.text(0.14, 0.07,
         "A chart position today rewards being streamed a lot in pieces, not bought whole.",
         color=PRETO, fontsize=11, family="DejaVu Sans")

out = "visuais/abbey_road_billboard.png"
fig.savefig(out, dpi=200, facecolor=fig.get_facecolor())
print("salvo:", out)
