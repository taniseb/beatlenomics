"""Post terça — McCartney Index, mesmo estádio (mesma-cidade-2011-2024, alcance)
Brief pedia 2011 vs 2024; o par limpo que existe com fonte é outro: mesmo estádio
e mesmo setor em duas visitas da turnê. Curitiba (Couto Pereira, Arquibancada)
2019 vs 2023; São Paulo (Allianz Parque, Cadeira Superior) 2019, 2023, 2024.
Unidade: dias de salário mínimo vigente na data da venda (2019 vendido em
dez/2018, salário de 2018 = R$954).
Porto Alegre 2010 vs 2017 descartado: preço da arquibancada de 2010 não confirmado.
Dado: dados/mesma_cidade.csv
"""
import pandas as pd
from beatlenomics_style import make_canvas, VERMELHO, AZUL, CINZA, PRETO

CINZA_MEIO = "#B7B7B5"
df = pd.read_csv("dados/mesma_cidade.csv")
df["dias"] = df["preco_inteira_brl"] / df["salario_minimo_venda_brl"] * 30

fig, ax = make_canvas("Same stadium, same seat, opposite directions",
                      "Paul McCartney's cheapest full-price ticket, in days of minimum wage at the time of sale.",
                      figsize=(10, 9))
cores_ano = {2019: CINZA_MEIO, 2023: VERMELHO, 2024: AZUL}
grupos = [("Curitiba", "Curitiba\nCouto Pereira, upper stands"),
          ("Sao Paulo", "Sao Paulo\nAllianz Parque, upper tier")]
xpos, labels = [], []
x = 0
for cid, lab in grupos:
    sub = df[df.cidade == cid]
    for i, r in enumerate(sub.itertuples()):
        ax.bar(x + i * 0.8, r.dias, width=0.7, color=cores_ano[r.ano_show])
        ax.text(x + i * 0.8, r.dias + 0.2, f"{r.dias:.1f}", ha="center", va="bottom",
                fontsize=14, fontweight="bold", color=PRETO, family="DejaVu Sans")
        ax.text(x + i * 0.8, 0.3, f"{r.ano_show}\nR${r.preco_inteira_brl}", ha="center", va="bottom",
                fontsize=10, color="white", family="DejaVu Sans")
    xpos.append(x + (len(sub) - 1) * 0.4); labels.append(lab)
    x += len(sub) * 0.8 + 1.0
ax.set_xticks(xpos)
ax.set_xticklabels(labels, fontsize=11, color=CINZA)
ax.set_ylim(0, 14.5)
ax.set_ylabel("Days of minimum wage", color=CINZA, fontsize=10.5)

out = "visuais/mesma_cidade.png"
fig.savefig(out, dpi=200)
print("salvo:", out)
print(df[["cidade", "ano_show", "preco_inteira_brl", "salario_minimo_venda_brl", "dias"]].round(2).to_string(index=False))
for cid in ("Curitiba", "Sao Paulo"):
    s = df[df.cidade == cid].sort_values("ano_show")
    print(cid, f"{s.dias.iloc[0]:.2f} -> {s.dias.iloc[-1]:.2f} ({s.dias.iloc[-1]/s.dias.iloc[0]-1:+.1%})")
