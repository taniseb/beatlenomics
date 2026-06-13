"""Post 5 — concentração de autoria dentro dos Beatles.
Dois dos quatro Beatles escreveram ~88% do catálogo original.
Fontes: Wikipedia (Lennon-McCartney ~180), Far Out / UNCUT (Harrison ~22), Starr 2.
"""
import pandas as pd
from beatlenomics_style import make_canvas, VERMELHO, AZUL, LARANJA, PRETO

d = pd.read_csv("dados/beatles_autoria.csv")
tot = d["musicas"].sum()
d["share"] = 100 * d["musicas"] / tot

cores = [VERMELHO, AZUL, LARANJA]

fig, ax = make_canvas(
    "Two Beatles wrote 88% of the songs",
    "Songwriting credit, and the royalties that follow it, was never split four ways",
    figsize=(9, 9))
ax.set_position([0.08, 0.40, 0.86, 0.18])   # barra única, centralizada

left = 0
for (_, row), c in zip(d.iterrows(), cores):
    ax.barh(0, row["share"], left=left, color=c, height=0.6,
            label=f'{row["compositor"]} ({int(row["musicas"])})')
    # rótulo do percentual dentro do segmento (só se couber)
    if row["share"] > 4:
        ax.text(left + row["share"]/2, 0, f'{row["share"]:.0f}%',
                ha="center", va="center", color="white",
                fontweight="bold", fontsize=15)
    left += row["share"]

ax.set_xlim(0, 100); ax.set_ylim(-0.5, 0.5)
ax.set_yticks([])
ax.set_xticks([0, 25, 50, 75, 100])
ax.set_xticklabels(["0%", "25%", "50%", "75%", "100%"])
ax.spines["left"].set_visible(False)
ax.set_xlabel("Share of the Beatles' original catalogue (204 songs)",
              fontsize=11, color=PRETO)
ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.7), ncol=1,
          frameon=False, fontsize=12)

out = "visuais/05_autoria.png"
fig.savefig(out, dpi=200)
print("salvo:", out, "| total:", tot, "| L-M share:", round(d['share'][0], 1))
