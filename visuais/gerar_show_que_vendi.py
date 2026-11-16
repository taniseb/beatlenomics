"""Post — The show I sold (17/11/2026). Card sem gráfico.
26.5 dias = R$600 (Pista Premium inteira, BH 04/05/2013) / R$678 (mínimo 2013) x 30.
"""
from beatlenomics_style import make_canvas, VERMELHO, LARANJA, AZUL, CINZA, PRETO

fig, ax = make_canvas("The show I sold",
                      "Paul McCartney, Mineirão, Belo Horizonte, 4 May 2013.\nPista Premium, sold at face value.",
                      figsize=(9, 9))
ax.set_axis_off()
ax.set_xlim(0, 1); ax.set_ylim(0, 1)
ax.text(0.5, 0.80, "R$600", ha="center", va="center", fontsize=84, fontweight="bold",
        color=VERMELHO, family="DejaVu Serif")
ax.text(0.5, 0.61, "= 26.5 days of the 2013 minimum wage", ha="center", va="center",
        fontsize=19, color=PRETO, family="DejaVu Sans")
ax.plot([0.08, 0.92], [0.47, 0.47], color=CINZA, lw=0.8)
ax.text(0.27, 0.33, "Money back", ha="center", fontsize=14, color=CINZA, family="DejaVu Sans")
ax.text(0.27, 0.20, "100%", ha="center", fontsize=34, fontweight="bold", color=AZUL, family="DejaVu Sans")
ax.text(0.73, 0.33, "Opportunity cost", ha="center", fontsize=14, color=CINZA, family="DejaVu Sans")
ax.text(0.73, 0.20, "the show", ha="center", fontsize=34, fontweight="bold", color=LARANJA, family="DejaVu Sans")
out = "posts/show-que-vendi/show_que_vendi.png"
fig.savefig(out, dpi=200)
print("salvo:", out)
