"""Post - The fund that bought 65,000 songs and imploded
Timeline dupla: Bowie Bonds (1997-2007) e Hipgnosis Songs Fund (2018-2024),
mesmo padrao de erro (precificar royalty como perpetuo) em escalas diferentes.
Fontes: posts/hipgnosis-bowie-bonds/referencias.md.
"""
from beatlenomics_style import make_canvas, VERMELHO, AZUL, PRETO, CINZA

fig, ax = make_canvas(
    "The fund that bought 65,000 songs and imploded",
    "Two royalty-securitization stories, same failure mode, 21 years apart.",
    figsize=(11, 7.5))
ax.set_position([0.08, 0.18, 0.87, 0.54])
ax.set_axis_off()

# cada linha tem seu proprio eixo temporal (nao compartilham escala de ano),
# espacados por ORDEM (nao por ano exato) pra evitar colisao de rotulo quando
# os eventos ficam proximos (2023/2024)
LINE_X0, LINE_X1 = 0.14, 0.98

def row_positions(n):
    return [LINE_X0 + (LINE_X1 - LINE_X0) * i / (n - 1) for i in range(n)]

ax.axhline(0.72, color=CINZA, lw=1.5, xmin=0.0, xmax=1.0, zorder=1)
ax.axhline(0.28, color=CINZA, lw=1.5, xmin=0.0, xmax=1.0, zorder=1)

bowie = [
    (1997, "Bowie Bonds issued\n$55M, 7.9% coupon, A3", AZUL),
    (2004, "Downgraded to Baa3\none notch above junk", VERMELHO),
    (2007, "Paid off in full", PRETO),
]
hipgnosis = [
    (2018, "IPO\n£200M raised", AZUL),
    (2023, "Shareholders vote\nagainst continuation", VERMELHO),
    (2024, "Sold to Blackstone\nvalued at $1.6B", PRETO),
]

for (year, label, color), x in zip(bowie, row_positions(len(bowie))):
    ax.plot(x, 0.72, "o", color=color, ms=11, zorder=3, transform=ax.transAxes)
    ax.annotate(label, xy=(x, 0.72), xytext=(x, 0.86), xycoords="axes fraction",
                textcoords="axes fraction", ha="center", va="bottom", fontsize=10,
                color=PRETO, family="DejaVu Sans",
                arrowprops=dict(arrowstyle="-", color=CINZA, lw=0.8))
    ax.text(x, 0.63, str(year), ha="center", va="top", fontsize=9.5, color=CINZA,
            transform=ax.transAxes)

for (year, label, color), x in zip(hipgnosis, row_positions(len(hipgnosis))):
    ax.plot(x, 0.28, "o", color=color, ms=11, zorder=3, transform=ax.transAxes)
    ax.annotate(label, xy=(x, 0.28), xytext=(x, 0.09), xycoords="axes fraction",
                textcoords="axes fraction", ha="center", va="top", fontsize=10,
                color=PRETO, family="DejaVu Sans",
                arrowprops=dict(arrowstyle="-", color=CINZA, lw=0.8))
    ax.text(x, 0.37, str(year), ha="center", va="bottom", fontsize=9.5, color=CINZA,
            transform=ax.transAxes)

ax.text(0.0, 0.755, "Bowie Bonds", ha="left", va="bottom", fontsize=12,
        fontweight="bold", color=AZUL, family="DejaVu Sans", transform=ax.transAxes)
ax.text(0.0, 0.315, "Hipgnosis Songs Fund", ha="left", va="bottom", fontsize=12,
        fontweight="bold", color=AZUL, family="DejaVu Sans", transform=ax.transAxes)

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

fig.text(0.08, 0.09,
         "Same mechanism: price a royalty stream as permanent, then find out it isn't.",
         color=PRETO, fontsize=11, family="DejaVu Sans")

out = "visuais/hipgnosis_timeline.png"
fig.savefig(out, dpi=200, facecolor=fig.get_facecolor())
print("salvo:", out)
