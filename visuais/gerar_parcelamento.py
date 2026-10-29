"""Post terça — "The installment that cost more than cash" (parcelamento-12x, alcance)
Premissa do brief ("12x sem juros") NÃO se confirmou nas fontes de preço da série:
2011/2012 sem info de parcelas; 2017 = 2x na venda geral (5x/3x só cartão ELO);
2023 = 10x COM juros no site; 2024 = até 10x só online, com taxa de conveniência
de 20% online (bilheteria sem taxa e sem parcelamento).
Conta, 2024 (Cadeira Superior, R$450): à vista na bilheteria vs 10x online
(R$450 + 20% = R$540), trazido a valor presente pela Selic meta do dia da venda
(26/06/2024, 10,50% a.a., BCB SGS 432). Assume 10x SEM juros (fonte não diz;
pendência). Se tivesse juros, o online fica ainda mais caro.
"""
import pandas as pd
from beatlenomics_style import make_canvas, VERMELHO, AZUL, CINZA, PRETO

CINZA_MEIO = "#B7B7B5"

preco, taxa, n, selic = 450.0, 0.20, 10, 0.105
online = preco * (1 + taxa)
parcela = online / n
r = (1 + selic) ** (1 / 12) - 1
# 1a parcela 1 mês após a compra (padrão de fatura de cartão)
vp = sum(parcela / (1 + r) ** k for k in range(1, n + 1))

termos = pd.DataFrame([
    dict(ano=2011, cidade="Rio de Janeiro", selic_venda=11.75, data_venda="2011-04-14", parcelas="não informado", taxa_online="não informado"),
    dict(ano=2012, cidade="Recife", selic_venda=None, data_venda="", parcelas="não informado", taxa_online="não informado"),
    dict(ano=2017, cidade="Porto Alegre", selic_venda=11.25, data_venda="2017-05-08", parcelas="2x venda geral (5x/3x cartão ELO)", taxa_online="sim, valor não informado"),
    dict(ano=2023, cidade="Sao Paulo", selic_venda=13.25, data_venda="2023-08-10", parcelas="10x com juros, só online", taxa_online="não informado"),
    dict(ano=2024, cidade="Sao Paulo", selic_venda=10.50, data_venda="2024-06-26", parcelas="até 10x, só online", taxa_online="20%"),
])
termos.to_csv("dados/parcelamento_termos.csv", index=False)

fig, ax = make_canvas(
    "The installment that cost more than cash",
    "Paul McCartney, Sao Paulo 2024, same upper-tier seat (R$450 full price).",
    figsize=(10, 9))

nomes = ["Cash at the\nbox office", "10 installments online\n(sticker, with 20% fee)", "10 installments online\n(present value at Selic 10.5%)"]
vals = [preco, online, vp]
cores = [CINZA_MEIO, VERMELHO, AZUL]
xs = range(3)
ax.bar(xs, vals, color=cores, width=0.6)
for x, v in zip(xs, vals):
    ax.text(x, v + 8, f"R${v:.0f}", ha="center", va="bottom", fontsize=15,
            fontweight="bold", color=PRETO, family="DejaVu Sans")
ax.set_xticks(list(xs))
ax.set_xticklabels(nomes, fontsize=10.5, color=CINZA)
ax.set_ylim(0, 640)
ax.set_ylabel("Reais", color=CINZA, fontsize=10.5)
ax.text(2, vp / 2, f"still +R${vp - preco:.0f}\nvs cash", ha="center", va="center",
        color="white", fontsize=12, fontweight="bold", family="DejaVu Sans")

out = "visuais/parcelamento.png"
fig.savefig(out, dpi=200)
print("salvo:", out)
print(f"online={online:.2f} parcela={parcela:.2f} r_mensal={r:.5f} VP={vp:.2f} "
      f"desconto financeiro={online - vp:.2f} ({(online - vp) / online:.1%}) "
      f"taxa={online - preco:.2f} VP-avista={vp - preco:.2f} ({vp / preco - 1:.1%})")
