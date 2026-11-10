"""Post — McCartney Index 1965: Shea Stadium
Ingresso mais barato inteira / salário mínimo mensal x 30 = dias de salário mínimo.
EUA: mensal = salário-hora federal x 2080 / 12 (mesma conversão de paul_mccartney_index.csv).
Dado: dados/shea_1965_index.csv
"""
import pandas as pd
from beatlenomics_style import make_canvas, VERMELHO, AZUL, LARANJA, CINZA, PRETO

df = pd.read_csv("dados/shea_1965_index.csv")
df["dias"] = df.preco_min_inteira / df.salario_min_mensal * 30
rot = ["Beatles\nShea Stadium, 1965\n$4.50", "Paul\nUSA, 2022\n$26.50", "Paul\nSão Paulo, 2024\nR$450"]
cores = [VERMELHO, AZUL, LARANJA]

fig, ax = make_canvas("Shea Stadium, 1965",
                      "Cheapest full-price ticket, in days of minimum wage at the time.",
                      figsize=(10, 9))
ax.bar(range(3), df.dias, width=0.6, color=cores)
for i, d in enumerate(df.dias):
    ax.text(i, d + 0.15, f"{d:.1f}", ha="center", va="bottom", fontsize=16,
            fontweight="bold", color=PRETO, family="DejaVu Sans")
ax.set_xticks(range(3))
ax.set_xticklabels(rot, fontsize=11, color=CINZA)
ax.set_ylim(0, 11)
ax.set_ylabel("Days of minimum wage", color=CINZA, fontsize=10.5)

out = "visuais/shea_1965.png"
fig.savefig(out, dpi=200)
print("salvo:", out)
print(df[["show", "ano", "preco_min_inteira", "salario_min_mensal", "dias"]].round(3).to_string(index=False))
print("horas 1965:", 4.50/1.25, "horas 2022:", 26.50/7.25, "razao BR/US2022:", df.dias[2]/df.dias[1])
