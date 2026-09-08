"""Post - Why is a 60-year-old catalog worth a billion?
Timeline das 4 vendas de catalogo (2020-2024): Dylan, Springsteen, Queen,
Pink Floyd. Barras mostram faixa reportada quando o valor exato nao foi
confirmado (Dylan, Springsteen). Cor destaca que Queen/Pink Floyd fecharam
DEPOIS da alta de juros (2022+) -- o ponto central do post.
Fontes: posts/catalogo-bilhao/referencias.md.
"""
import matplotlib.pyplot as plt
from beatlenomics_style import make_canvas, VERMELHO, AZUL, PRETO, CINZA

CINZA_BARRA = "#B7B7B5"

# (label, ano, valor_baixo, valor_alto, cor)
deals = [
    ("Bob Dylan\n(songwriting)\n2020", 2020, 250, 300, CINZA_BARRA),
    ("Bruce Springsteen\n(recordings + songwriting)\n2021", 2021, 500, 600, CINZA_BARRA),
    ("Pink Floyd\n(recordings)\nOct 2024", 2024.3, 400, 400, VERMELHO),
    ("Queen\n(recordings + publishing)\nJun 2024", 2024.0, 1270, 1270, VERMELHO),
]
deals.sort(key=lambda d: d[1])

fig, ax = make_canvas(
    "Why is a 60-year-old catalog worth a billion?",
    "Four legacy music catalog sales, 2020-2024 (US$ millions). Red = closed after rates had already climbed.",
    figsize=(11, 7.5))
ax.set_position([0.10, 0.20, 0.85, 0.52])

xs = range(len(deals))
low = [d[2] for d in deals]
high = [d[3] for d in deals]
cores = [d[4] for d in deals]
mid = [(l + h) / 2 for l, h in zip(low, high)]

bars = ax.bar(xs, mid, color=cores, width=0.55, zorder=3)
for i, (lo, hi, m) in enumerate(zip(low, high, mid)):
    if lo != hi:
        ax.plot([i, i], [lo, hi], color=PRETO, lw=2, zorder=4)
        ax.plot([i - 0.08, i + 0.08], [lo, lo], color=PRETO, lw=2, zorder=4)
        ax.plot([i - 0.08, i + 0.08], [hi, hi], color=PRETO, lw=2, zorder=4)
        label = f"${lo}-{hi}M\nreported"
    else:
        label = f"${hi}M"
    ax.text(i, hi + 35, label, ha="center", va="bottom", fontsize=10.5,
            fontweight="bold", color=PRETO, family="DejaVu Sans")

ax.set_xticks(list(xs))
ax.set_xticklabels([d[0] for d in deals], fontsize=9.5, family="DejaVu Sans")
ax.set_ylabel("Deal value (US$ millions)", color=CINZA, fontsize=10.5)
ax.set_ylim(0, 1500)
for spine in ("top", "right"):
    ax.spines[spine].set_visible(False)

fig.text(0.10, 0.10,
         "Fed funds rate: near zero in 2020-21, above 5% by the time Queen and Pink Floyd closed.",
         color=PRETO, fontsize=11, family="DejaVu Sans")
fig.text(0.10, 0.07,
         "Queen, the largest deal on record, closed after cheap money ended, not during it.",
         color=PRETO, fontsize=11, family="DejaVu Sans")

out = "visuais/catalogo_bilhao.png"
fig.savefig(out, dpi=200, facecolor=fig.get_facecolor())
print("salvo:", out)
