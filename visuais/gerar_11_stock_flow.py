"""Post 11 — It never gets old. But does it never get old?
Stock vs. flow: os Beatles dominam a métrica de estoque (vendas acumuladas
por ano de carreira) e somem na métrica de fluxo (ouvintes mensais no Spotify).
A mesma banda no topo de um painel e no fim do outro = a tese do post.
Fontes: ver posts/11-never-gets-old/referencias.md
"""
import numpy as np
from beatlenomics_style import make_canvas, VERMELHO, AZUL, PRETO, CINZA

CINZA_BAR = "#B7B7B5"   # não-Beatles, pra o vermelho saltar

# --- STOCK: vendas por ano de carreira ativa (milhões de discos/ano) ---
stock_art = ["The Beatles", "Elvis", "Taylor Swift"]
stock_val = [86, 22, 11]

# --- FLOW: ouvintes mensais no Spotify (milhões) ---
flow_art = ["Taylor Swift", "Queen", "The Beatles"]
flow_val = [103, 50, 10]

fig, ax = make_canvas(
    "Greatest ever, but not most-streamed now",
    "By the stock metric no one catches the Beatles. By the flow metric they are a mid-tier legacy act.",
    figsize=(11, 9))

# reposiciona o eixo padrão como painel ESQUERDO e cria o painel DIREITO
ax.set_position([0.10, 0.16, 0.34, 0.44])
ax2 = fig.add_axes([0.60, 0.16, 0.34, 0.44])
ax2.set_facecolor(ax.get_facecolor())
for s in ("top", "right"):
    ax2.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax2.spines[s].set_color(CINZA)
ax2.tick_params(colors=CINZA, length=0)


def painel(a, arts, vals, unidade, vmax):
    y = np.arange(len(arts))
    cores = [VERMELHO if "Beatles" in nm else CINZA_BAR for nm in arts]
    a.barh(y, vals, 0.62, color=cores)
    for i, v in enumerate(vals):
        a.text(v + vmax*0.02, i, f"{v}{unidade}", va="center", ha="left",
               fontsize=12, fontweight="bold",
               color=VERMELHO if "Beatles" in arts[i] else PRETO)
    a.set_yticks(y)
    a.set_yticklabels(arts, fontsize=12, color=PRETO)
    a.invert_yaxis()
    a.set_xlim(0, vmax)
    a.set_xticks([])
    a.spines["left"].set_visible(False)
    a.spines["bottom"].set_visible(False)


painel(ax,  stock_art, stock_val, "M", 120)
painel(ax2, flow_art,  flow_val,  "M", 120)

# títulos dos painéis (coords da figura)
fig.text(0.10, 0.655, "THE STOCK METRIC", color=VERMELHO, fontsize=13,
         fontweight="bold", family="DejaVu Sans")
fig.text(0.10, 0.625, "Records sold per active career year",
         color=CINZA, fontsize=11, family="DejaVu Sans")
fig.text(0.60, 0.655, "THE FLOW METRIC", color=AZUL, fontsize=13,
         fontweight="bold", family="DejaVu Sans")
fig.text(0.60, 0.625, "Spotify monthly listeners",
         color=CINZA, fontsize=11, family="DejaVu Sans")

# fecho: Here Comes the Sun como o que de fato não envelhece
fig.text(0.10, 0.105,
         "And one 1969 track still pulls ~472,000 plays a day, 57 years on:",
         color=PRETO, fontsize=11, family="DejaVu Sans")
fig.text(0.10, 0.075, "Here Comes the Sun.",
         color=VERMELHO, fontsize=13, fontweight="bold", family="DejaVu Serif")

out = "visuais/11_stock_flow.png"
fig.savefig(out, dpi=200)
print("salvo:", out, "| stock:", stock_val, "| flow:", flow_val)
