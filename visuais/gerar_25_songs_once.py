"""Post pessoal — "The 25 songs I only heard once"
Espelho do post 13 (mesmo dado, ângulo oposto): em vez do núcleo fixo de 12
músicas tocadas em todos os 13 shows, aqui é a cauda de 25 músicas tocadas em
exatamente 1 show, em 14 anos (2010-2024). Angulo é sorte/irrepetibilidade,
NAO concentracao/desigualdade (isso ja foi feito no post 4, Gini, e no HHI de
27/ago) -- nao usar Gini/HHI/Lorenz aqui.
Dado: dados/meus_13_shows_musicas.csv (setlists de dados/meus_13_shows.csv,
coletados via setlist.fm). Mesmo dado do post 13 (posts/13-shows-paul/).
"""
import numpy as np
import pandas as pd
from beatlenomics_style import make_canvas, VERMELHO, PRETO, CINZA

CINZA_MEIO = "#B7B7B5"

df = pd.read_csv("dados/meus_13_shows_musicas.csv")
shows = pd.read_csv("dados/meus_13_shows.csv")
counts = df["musica"].value_counts()
n_shows = df["show_num"].nunique()

nucleo = counts[counts == n_shows]
meio = counts[(counts > 1) & (counts < n_shows)]
uma_vez = counts[counts == 1]

# ordena a cauda de 1x alfabeticamente pra distribuir bem no eixo (sem hierarquia real)
uma_vez = uma_vez.sort_index()

cores = [CINZA_MEIO] * len(nucleo) + [CINZA_MEIO] * len(meio) + [VERMELHO] * len(uma_vez)
valores = list(nucleo.values) + list(meio.values) + list(uma_vez.values)

fig, ax = make_canvas(
    "The 25 songs I only heard once",
    f"All {len(counts)} songs across the 13 Paul McCartney shows I've seen, 2010-2024, sorted by times played.",
    figsize=(11, 8))
ax.set_position([0.09, 0.14, 0.86, 0.56])

xs = np.arange(len(valores))
ax.bar(xs, valores, color=cores, width=0.86)

start_once = len(nucleo) + len(meio)
ax.annotate(f"25 songs, played once\nin 14 years of shows",
            xy=(start_once + len(uma_vez) * 0.5, 1), xytext=(start_once - 18, 6.5),
            color=VERMELHO, fontsize=12, fontweight="bold", family="DejaVu Sans",
            ha="left", va="bottom",
            arrowprops=dict(arrowstyle="-", color=VERMELHO, lw=1,
                            connectionstyle="arc3,rad=0.25"))

ax.text(1, 13.6, f"the core: {len(nucleo)} songs,\nplayed every time",
        color=CINZA, fontsize=10.5, style="italic", family="DejaVu Sans", va="top")

ax.set_ylim(0, 15.5)
ax.set_yticks([0, 1, 13])
ax.set_ylabel("Times played (out of 13 shows)", color=CINZA, fontsize=10.5)
ax.set_xticks([])
ax.set_xlabel(f"{len(counts)} songs, sorted by times played", color=CINZA, fontsize=10.5)
ax.set_xlim(-1, len(valores))

out = "visuais/25_songs_once.png"
fig.savefig(out, dpi=200)
print("salvo:", out)
print(f"nucleo (13/13): {len(nucleo)} | meio: {len(meio)} | uma vez: {len(uma_vez)}")
print("lista das 25 tocadas uma vez:", uma_vez.index.tolist())
