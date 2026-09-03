"""Gráfico do Post C7 — ticket em BRL, câmbio USD/BRL e ticket em USD equivalente,
todos indexados a 2011=100. Mostra que o preço em dólar NÃO acompanha o câmbio.
Fonte: dados/paul_brasil_ao_longo_tempo.csv (preço) + Frankfurter API na data do show (fx).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from beatlenomics_style import make_canvas, VERMELHO, AZUL, CINZA, PRETO

anos = [2011, 2012, 2017, 2023, 2024]
brl = {2011: 180.0, 2012: 160.0, 2017: 350.0, 2023: 420.0, 2024: 450.0}
fx = {2011: 1.6211, 2012: 1.8783, 2017: 3.1767, 2023: 4.9117, 2024: 5.5901}
usd = {a: brl[a] / fx[a] for a in anos}

base_brl, base_fx, base_usd = brl[2011], fx[2011], usd[2011]
idx_brl = [100 * brl[a] / base_brl for a in anos]
idx_fx = [100 * fx[a] / base_fx for a in anos]
idx_usd = [100 * usd[a] / base_usd for a in anos]

fig, ax = make_canvas(
    "Is the ticket priced in dollars?",
    "McCartney ticket in Brazil, indexed to 2011 = 100",
)

x = range(len(anos))
ax.plot(x, idx_fx, color=PRETO, lw=2.2, marker="o", ms=6, label="USD/BRL exchange rate")
ax.plot(x, idx_brl, color=AZUL, lw=2.2, marker="o", ms=6, label="Ticket price (BRL)")
ax.plot(x, idx_usd, color=VERMELHO, lw=2.6, marker="o", ms=7,
        label="Ticket price (USD-equivalent)")
ax.axhline(100, color=CINZA, lw=1, ls="--", zorder=1)
ax.text(len(anos) - 1 - 0.05, 108, "if dollar-indexed", color=CINZA, fontsize=9,
        ha="right", va="bottom")

ax.set_xticks(list(x))
ax.set_xticklabels([str(a) for a in anos])
ax.set_xlim(-0.3, len(anos) - 1 + 0.3)
ax.set_ylabel("Index (2011 = 100)", color=CINZA, fontsize=10)
ax.set_ylim(0, 370)
ax.legend(loc="upper left", frameon=False, fontsize=9)

fig.savefig(os.path.join(os.path.dirname(__file__), "c7_ticket_dolar.png"),
            dpi=200, facecolor=fig.get_facecolor())
print("ok: c7_ticket_dolar.png")
