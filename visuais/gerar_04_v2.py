"""Post 4, slide 3 (prova): ranking top 15 por era, com identidade #beatlenomics."""
import pandas as pd
from beatlenomics_style import make_canvas, PALETA, PRETO
from matplotlib.patches import Patch

df = pd.read_csv("dados/paul_setlist_top52.csv").head(15).copy()
df = df.sort_values("performances")  # menor -> maior p/ barh

cores = [PALETA[e] for e in df["era"]]

fig, ax = make_canvas(
    "The songs Paul plays the most",
    "10 of his 15 most played live are Beatles songs",
    figsize=(9, 9))

ax.set_position([0.34, 0.14, 0.58, 0.60])   # margem p/ nomes longos
barras = ax.barh(df["song"], df["performances"], color=cores)
ax.bar_label(barras, padding=4, fontsize=9.5, color=PRETO)
ax.set_xlim(0, df["performances"].max()*1.13)
ax.set_xlabel("Times played live (solo career)", fontsize=11, color=PRETO)
ax.tick_params(axis="y", labelsize=9.5)

ax.legend(handles=[Patch(color=PALETA["Beatles"], label="Beatles"),
                   Patch(color=PALETA["Wings"], label="Wings"),
                   Patch(color=PALETA["Solo"], label="McCartney solo")],
          loc="lower right", frameon=False, fontsize=9.5)

out = "visuais/04_v2.png"
fig.savefig(out, dpi=200)
print("salvo:", out)
