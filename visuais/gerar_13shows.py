"""Post pessoal — "I saw Paul McCartney live 13 times"
Curva completa das 85 musicas tocadas nos 13 shows da Tanise (2010-2024),
ordenadas por frequencia: o nucleo fixo de 12 musicas (13/13 shows) aparece
como plato no topo, em contraste com a cauda de 73 musicas que entraram e
sairam do repertorio. Ob-La-Di, Ob-La-Da (a favorita dela, parte do nucleo)
destacada em vermelho.
Dado: dados/meus_13_shows_musicas.csv (setlists de dados/meus_13_shows.csv,
coletados via setlist.fm).
"""
import numpy as np
import pandas as pd
from beatlenomics_style import make_canvas, VERMELHO, PRETO, CINZA

CINZA_NUCLEO = "#8C8C8A"
CINZA_CAUDA = "#B7B7B5"

df = pd.read_csv("dados/meus_13_shows_musicas.csv")
counts = df["musica"].value_counts()
n_shows = df["show_num"].nunique()

# ordena: nucleo (13/13) primeiro, Ob-La-Di no meio do plato para a anotacao respirar
counts = counts.sort_values(ascending=False)
nucleo = counts[counts == n_shows]
cauda = counts[counts < n_shows]

cores = [VERMELHO if s == "Ob-La-Di, Ob-La-Da" else CINZA_NUCLEO for s in nucleo.index]
cores += [CINZA_CAUDA] * len(cauda)
valores = list(nucleo.values) + list(cauda.values)

fig, ax = make_canvas(
    "The 12 songs Paul never dropped on me",
    f"All {len(counts)} songs across the 13 shows I've seen, 2010-2024, sorted by times played.",
    figsize=(11, 8))
ax.set_position([0.09, 0.14, 0.86, 0.56])

xs = np.arange(len(valores))
ax.bar(xs, valores, color=cores, width=0.86)

# anotacao do nucleo
ax.annotate(f"the core: 12 songs,\nplayed at all 13 shows",
            xy=(len(nucleo) * 0.55, n_shows), xytext=(16, 14.6),
            color=PRETO, fontsize=11.5, fontweight="bold", family="DejaVu Sans",
            ha="left", va="top",
            arrowprops=dict(arrowstyle="-", color=CINZA, lw=1,
                            connectionstyle="arc3,rad=0.2"))

# anotacao da Ob-La-Di
idx_obladi = list(nucleo.index).index("Ob-La-Di, Ob-La-Da")
ax.annotate("Ob-La-Di, Ob-La-Da\n(my favorite)",
            xy=(idx_obladi, 12.4), xytext=(idx_obladi + 9, 11.2),
            color=VERMELHO, fontsize=11, fontweight="bold", family="DejaVu Sans",
            ha="left", va="top",
            arrowprops=dict(arrowstyle="-", color=VERMELHO, lw=1,
                            connectionstyle="arc3,rad=-0.2"))

# anotacao da cauda
ax.text(len(nucleo) + len(cauda) * 0.45, 5.4,
        f"the other {len(cauda)} rotated in and out",
        color=CINZA, fontsize=11, style="italic", family="DejaVu Sans")

ax.set_ylim(0, 15.5)
ax.set_yticks(range(0, 14, 13))
ax.set_yticks([0, 13])
ax.set_ylabel("Times played (out of 13 shows)", color=CINZA, fontsize=10.5)
ax.set_xticks([])
ax.set_xlabel(f"{len(counts)} songs, sorted by times played", color=CINZA, fontsize=10.5)
ax.set_xlim(-1, len(valores))

out = "visuais/13shows_top.png"
fig.savefig(out, dpi=200)
print("salvo:", out)
print(f"nucleo: {len(nucleo)} musicas | cauda: {len(cauda)} | Ob-La-Di em posicao {idx_obladi}")
