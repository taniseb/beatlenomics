"""Post — The Beatles never played Brazil (alcance)
Beatles: ~1.400 apresentações 1957-66 (Gould 2007, via Wikipedia), 20 países/territórios, zero na América do Sul.
Paul solo no Brasil: shows por ano, contagem setlist.fm (piso). Duas entradas excluídas por dúvida (ver nota no CSV).
Dado: dados/paul_brasil_shows.csv
"""
import pandas as pd
from matplotlib.patches import Rectangle
from beatlenomics_style import make_canvas, VERMELHO, LARANJA, CINZA, PRETO

df = pd.read_csv("dados/paul_brasil_shows.csv")
df = df[df.incluido == "sim"]
por_ano = df.groupby("ano").size()

fig, ax = make_canvas("The Beatles never played Brazil",
                      "Shows in Brazil per year. Beatles 1957-66: ~1,400 shows, none in South America.\nPaul McCartney solo, 1990-2024 (setlist.fm).",
                      figsize=(10, 9))
ax.add_patch(Rectangle((1956.5, 0), 10, 9.6, color=VERMELHO, alpha=0.12, lw=0))
ax.text(1961.5, 5.0, "The Beatles\n~1,400 shows\n0 in Brazil", ha="center", va="center",
        fontsize=14, fontweight="bold", color=VERMELHO, family="DejaVu Sans")
ax.bar(por_ano.index, por_ano.values, width=0.8, color=LARANJA)
for ano, n in por_ano.items():
    ax.text(ano, n + 0.15, str(n), ha="center", va="bottom", fontsize=11,
            fontweight="bold", color=PRETO, family="DejaVu Sans")
ax.annotate("1990, Maracanã:\n184,000 paying fans", xy=(1990, 2.2), xytext=(1976, 7.2),
            fontsize=11, color=PRETO, family="DejaVu Sans",
            arrowprops=dict(arrowstyle="-", color=CINZA, lw=0.8))
ax.set_xlim(1955, 2026)
ax.set_ylim(0, 9.8)
ax.set_xticks([1957, 1966, 1990, 2010, 2024])
ax.set_ylabel("Shows in Brazil", color=CINZA, fontsize=10.5)

out = "visuais/never_played_brazil.png"
fig.savefig(out, dpi=200)
print("salvo:", out)
print(por_ano.to_string(), "\ntotal:", por_ano.sum(), "anos:", len(por_ano))
