"""Post — The McCartney Index, personal edition (BR-UY-AR-MX)
Not the clean 7-country Got Back-only version. This one uses Tanise's own
tier at her own 4 shows across different tours (Out There 2014, Freshen Up
2019, Got Back 2023-2024) - premium standing in UY/AR/BR, regular standing
in MX (her own choice that year). Less comparable by design; the point is
personal, not methodological purity. See posts/mccartney-index/pesquisa_notas.md
("Versao pessoal") for every caveat.
Dado: dados/paul_meu_indice.csv.
"""
import pandas as pd
from beatlenomics_style import make_canvas, VERMELHO, AZUL, PRETO, CINZA

df = pd.read_csv("dados/paul_meu_indice.csv")
df["salario_diario"] = df["salario_min_mensal_local"] / 30
df["dias_salario_minimo"] = df["preco_tier_oficial"] / df["salario_diario"]
df = df.sort_values("dias_salario_minimo")

fig, ax = make_canvas(
    "My own McCartney Index",
    "Days of local minimum wage per ticket, at the tier I actually bought,\nacross four shows and four different tours (2014-2023).",
    figsize=(11, 6.5))
ax.set_position([0.24, 0.20, 0.70, 0.48])

cores = [VERMELHO if p == "Brasil" else CINZA for p in df["pais"]]
y = range(len(df))
ax.barh(y, df["dias_salario_minimo"], color=cores, height=0.55, zorder=3)
ax.set_yticks(list(y))
EN = {"Brasil": "Brazil", "México": "Mexico", "Uruguai": "Uruguay"}
labels = [f"{EN.get(p, p)}\n({t})" for p, t in zip(df["pais"], df["turne"])]
ax.set_yticklabels(labels, fontsize=10, family="DejaVu Sans")

for yi, val in zip(y, df["dias_salario_minimo"]):
    ax.text(val + 0.3, yi, f"{val:.1f}", va="center", fontsize=11,
            fontweight="bold", color=PRETO, family="DejaVu Sans")

ax.set_xlabel("Days of local minimum wage per ticket", color=CINZA, fontsize=10.5)
for spine in ("top", "right"):
    ax.spines[spine].set_visible(False)

fig.text(0.09, 0.10,
         "My Brazil ticket (Pista Premium) cost 21 days of minimum wage. My Uruguay ticket, 3.5.",
         color=PRETO, fontsize=11, family="DejaVu Sans")
fig.text(0.09, 0.07,
         "Not apples to apples: different tours, different years, and Mexico is regular standing, not premium.",
         color=CINZA, fontsize=9.5, family="DejaVu Sans")

out = "visuais/mccartney_meu_indice.png"
fig.savefig(out, dpi=200)
print("salvo:", out)
print(df[["pais", "dias_salario_minimo"]].round(2).to_string(index=False))
