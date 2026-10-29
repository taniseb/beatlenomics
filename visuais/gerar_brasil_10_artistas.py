"""Post quinta — "Nine stadium shows, one price band" (brasil-10-artistas-index, técnico leve)
Régua da franquia: inteira mais barata, sem visão parcial, em dias de salário
mínimo vigente na data da venda. 9 shows pagos em estádio de São Paulo
(8 no Allianz Parque, Oasis no Morumbis), 2022-2025. Paul em vermelho.
Madonna 2024 (grátis, Copacabana) fica no CSV mas sai do gráfico (decisão 13/10/2026).
Dado: dados/brasil_10_artistas.csv (fontes por linha).
"""
import pandas as pd
from beatlenomics_style import make_canvas, VERMELHO, AZUL, CINZA, PRETO

CINZA_MEIO = "#B7B7B5"
df = pd.read_csv("dados/brasil_10_artistas.csv")
df = df[df["artista"] != "Madonna"]
df["dias"] = df["preco_inteira_brl"] / df["salario_minimo_venda_brl"] * 30
df = df.sort_values("dias").reset_index(drop=True)

fig, ax = make_canvas("Nine stadium shows, one price band",
                      "Cheapest full-price ticket in São Paulo, in days of minimum wage at the time of sale.",
                      figsize=(10, 9))
ax.set_position([0.27, 0.13, 0.65, 0.62])
cores = [VERMELHO if a == "Paul McCartney" else CINZA_MEIO for a in df["artista"]]
ax.barh(range(len(df)), df["dias"], color=cores, height=0.62)
for i, r in df.iterrows():
    txt = "free" if r.dias == 0 else f"{r.dias:.1f}"
    ax.text(r.dias + 0.15, i, txt, va="center", fontsize=12, fontweight="bold",
            color=PRETO, family="DejaVu Sans")
ax.set_yticks(range(len(df)))
ax.set_yticklabels([f"{a} ({y})" for a, y in zip(df["artista"], df["ano_show"])], fontsize=10.5, color=CINZA)
ax.set_xlabel("Days of minimum wage", color=CINZA, fontsize=10.5)
ax.set_xlim(0, 14.5)

out = "visuais/brasil_10_artistas.png"
fig.savefig(out, dpi=200)
print("salvo:", out)
print(df[["artista", "ano_show", "preco_inteira_brl", "salario_minimo_venda_brl", "dias"]].round(2).to_string(index=False))
pagos = df[df.dias > 0]
print("faixa pagos:", round(pagos.dias.min(), 1), "a", round(pagos.dias.max(), 1),
      "| mediana:", round(pagos.dias.median(), 2),
      "| posição do Paul entre os pagos (1 = mais barato):", int((pagos.dias < pagos[pagos.artista == 'Paul McCartney'].dias.iloc[0]).sum()) + 1)
