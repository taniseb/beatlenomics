"""Post — The McCartney Index
Big Mac Index logic applied to Paul McCartney's Got Back tour (2022-2025):
same artist, same tour, same production, cheapest full-price non-restricted
ticket per country. Headline metric: days of local minimum wage per ticket.
Dado: dados/paul_ticket_prices.csv + dados/paul_fx_minwage.csv, combinados em
dados/paul_mccartney_index.csv. Fontes por linha: posts/mccartney-index/pesquisa_notas.md.
"""
import pandas as pd
from beatlenomics_style import make_canvas, VERMELHO, AZUL, PRETO, CINZA

df = pd.read_csv("dados/paul_mccartney_index.csv")
# uma linha por pais: Brasil usa o ano mais recente (2024) para nao duplicar
df = df.sort_values("data_show").drop_duplicates("pais", keep="last")
df = df.sort_values("dias_salario_minimo")

fig, ax = make_canvas(
    "The McCartney Index",
    "Days of local minimum wage to buy the cheapest full-price, unrestricted-view ticket,\nsame tour (Got Back, 2022-2025), same production, same setlist.",
    figsize=(11, 7))
ax.set_position([0.28, 0.16, 0.66, 0.54])

cores = [VERMELHO if p == "Brasil" else CINZA for p in df["pais"]]
y = range(len(df))
ax.barh(y, df["dias_salario_minimo"], color=cores, height=0.6, zorder=3)
ax.set_yticks(list(y))
EN = {"Brasil": "Brazil", "Reino Unido": "UK", "Franca": "France",
      "Espanha": "Spain", "Estados Unidos": "United States"}
ax.set_yticklabels([EN.get(p, p) for p in df["pais"]], fontsize=11, family="DejaVu Sans")

for yi, (val, pais) in enumerate(zip(df["dias_salario_minimo"], df["pais"])):
    ax.text(val + 0.15, yi, f"{val:.1f}", va="center", fontsize=10.5,
            fontweight="bold", color=PRETO, family="DejaVu Sans")

usa_val = df.loc[df["pais"] == "Estados Unidos", "dias_salario_minimo"].iloc[0]
ax.axvline(usa_val, color=AZUL, lw=1.1, ls=":", zorder=1)
ax.text(usa_val + 0.1, len(df) - 0.4, "USA reference", color=AZUL, fontsize=9,
        family="DejaVu Sans")

ax.set_xlabel("Days of local minimum wage per cheapest ticket", color=CINZA, fontsize=10.5)
for spine in ("top", "right"):
    ax.spines[spine].set_visible(False)

fig.text(0.09, 0.085,
         "Brazil's cheapest ticket costs 9.6 days of minimum wage. In the US, 0.6 of a day.",
         color=PRETO, fontsize=11, family="DejaVu Sans")
fig.text(0.09, 0.055,
         "Burgernomics, but with a beatle: same product everywhere, wildly different local cost.",
         color=PRETO, fontsize=11, family="DejaVu Sans")

out = "visuais/mccartney_index.png"
fig.savefig(out, dpi=200)
print("salvo:", out)
print(df[["pais", "dias_salario_minimo"]].round(2).to_string(index=False))
