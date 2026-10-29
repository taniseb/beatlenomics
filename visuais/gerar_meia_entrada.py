"""Post terça — "Who pays for the half-price ticket?" (meia-entrada, alcance)
Barras da inteira mais barata do Paul no Brasil (2011-2024), em dias de salário
mínimo, com a Lei 12.933 (sanção 26/12/2013) e o Decreto 8.537 (vigência
01/12/2015, quando a cota de 40% passa a valer) marcados.
2017 é o primeiro show depois das duas datas: coincidência sugestiva, NÃO efeito
(o efeito é o C11, DiD Brasil vs vizinhos).
Dado: dados/paul_brasil_ao_longo_tempo.csv + dados/paul_brasil_2013_2014.csv (shows de 2013 e 2014, antes faltando).
"""
import pandas as pd
from beatlenomics_style import make_canvas, VERMELHO, AZUL, CINZA, PRETO

CINZA_MEIO = "#B7B7B5"

cols = ["ano", "cidade", "preco_inteira_brl", "salario_minimo_mensal_brl"]
df = pd.concat([pd.read_csv("dados/paul_brasil_ao_longo_tempo.csv")[cols],
                pd.read_csv("dados/paul_brasil_2013_2014.csv")[cols]]).sort_values("ano").reset_index(drop=True)
df["cidade"] = df["cidade"].replace({"Goiania": "Goiânia"})
df["dias_sm"] = df["preco_inteira_brl"] / df["salario_minimo_mensal_brl"] * 30

fig, ax = make_canvas(
    "Who pays for the half-price ticket?",
    "Paul McCartney's cheapest full-price ticket in Brazil, in days of minimum wage.",
    figsize=(11, 9))

# eixo categórico (shows igualmente espaçados); lei e decreto caem entre 2012 e 2017
xs = list(range(len(df)))
cores = [VERMELHO if a == 2017 else CINZA_MEIO for a in df["ano"]]
ax.bar(xs, df["dias_sm"], color=cores, width=0.62)

for x, d, p, c in zip(xs, df["dias_sm"], df["preco_inteira_brl"], df["cidade"]):
    ax.text(x, d + 0.25, f"{d:.1f}", ha="center", va="bottom",
            fontsize=13, fontweight="bold", color=PRETO, family="DejaVu Sans")
    ax.text(x, 0.3, f"R${p:.0f}", ha="center", va="bottom",
            fontsize=9.5, color="white", family="DejaVu Sans")

lei, decreto = 2.5, 3.5
ax.axvline(lei, color=AZUL, lw=1.2, ls="--")
ax.axvline(decreto, color=AZUL, lw=1.2, ls="--")
ax.text(lei - 0.04, 13.6, "Law 12.933\nsigned\nDec 2013", color=AZUL, fontsize=10,
        ha="right", va="top", family="DejaVu Sans")
ax.text(decreto + 0.04, 13.6, "40% cap\nin force\nDec 2015", color=AZUL, fontsize=10,
        ha="left", va="top", family="DejaVu Sans")

i17 = list(df["ano"]).index(2017)
ax.text(i17 + 0.36, 12.6, "first show\nafter the cap",
        color=VERMELHO, fontsize=10.5, ha="left", va="center", style="italic",
        family="DejaVu Sans")

ax.set_ylim(0, 14)
ax.set_xlim(-0.6, len(df) - 0.4)
ax.set_xticks(xs)
ax.set_xticklabels([f"{a}\n{c}" for a, c in zip(df["ano"], df["cidade"])],
                   fontsize=9.5, color=CINZA)
ax.set_ylabel("Days of minimum wage", color=CINZA, fontsize=10.5)

out = "visuais/meia_entrada.png"
fig.savefig(out, dpi=200)
print("salvo:", out)
print(df[["ano", "cidade", "preco_inteira_brl", "salario_minimo_mensal_brl", "dias_sm"]].round(1).to_string(index=False))
# aritmética da incidência: receita fixa, 40% a meio preço
# 0.6*P + 0.4*P/2 = P0  ->  P = P0/0.8 = 1.25*P0
print("markup da inteira com cota cheia e receita fixa:", round(1 / 0.8 - 1, 4))
print("2014 em dias x 1.25 =", round(220 / 724 * 30 * 1.25, 2))
