"""Post - Dynamic pricing do Oasis
Barras: preco anunciado (148.50), preco no checkout (>350), e o markup do
selo "platinum" (2.5x o padrao equivalente) achado pela CMA. Sem eixo de
tempo -- o ponto e a distancia entre o que foi anunciado e o que foi pago.
Fontes: posts/oasis-dynamic-pricing/referencias.md.
"""
from beatlenomics_style import make_canvas, VERMELHO, AZUL, PRETO, CINZA

fig, ax = make_canvas(
    "What fans saw vs. what fans paid",
    "Oasis reunion tour tickets, UK, August 2024 (GBP)",
    figsize=(10, 7.5))
ax.set_position([0.14, 0.20, 0.80, 0.52])

itens = [
    ("Advertised\nprice", 148.50, AZUL),
    ("In-demand price\nat checkout (reported)", 350.0, VERMELHO),
]

xs = range(len(itens))
vals = [v for _, v, _ in itens]
cores = [c for _, _, c in itens]
ax.bar(xs, vals, color=cores, width=0.45, zorder=3)
labels = ["£148.50", "£350+"]
for i, v in enumerate(vals):
    ax.text(i, v + 8, labels[i], ha="center", va="bottom",
            fontsize=13, fontweight="bold", color=PRETO, family="DejaVu Sans")

ax.set_xticks(list(xs))
ax.set_xticklabels([n for n, _, _ in itens], fontsize=11, family="DejaVu Sans")
ax.set_ylabel("Price (GBP)", color=CINZA, fontsize=10.5)
ax.set_ylim(0, 420)
ax.set_xlim(-0.6, 1.6)
for spine in ("top", "right"):
    ax.spines[spine].set_visible(False)

fig.text(0.14, 0.10,
         "Same ticket, same queue: price at checkout ran over 2.3x what was advertised.",
         color=PRETO, fontsize=11, family="DejaVu Sans")
fig.text(0.14, 0.07,
         "Separately, the CMA found \"platinum\" seats priced ~2.5x standard ones, same section, no upgrade.",
         color=PRETO, fontsize=11, family="DejaVu Sans")

out = "visuais/oasis_pricing.png"
fig.savefig(out, dpi=200, facecolor=fig.get_facecolor())
print("salvo:", out)
