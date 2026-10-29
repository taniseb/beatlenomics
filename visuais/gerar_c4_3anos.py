"""Update do C4 — Now and Then, 3 anos depois: o halo durou?
Mesmo DiD do C4 (gerar_c4_nowandthen.py): tratado = The Beatles, controle = média
de Rolling Stones, Led Zeppelin, Pink Floyd; pré = 12 semanas antes de 02/11/2023.
Janela estendida: 2023-05-28 a 2026-09-27 (semanas completas), coleta pytrends
em 09/10/2026 (mesma query conjunta, mundial). Efeito por trimestre desde o
lançamento. O pico de 100 cai na mesma semana do C4, então a escala bate e o
+13 pts das 8 semanas replica o C4.
Outros choques Beatles na janela (marcados no gráfico, NÃO separáveis por este
desenho): Beatles '64 (Disney+, 29/11/2024); Anthology 4 (21/11/2025) e série
Anthology no Disney+ (26/11/2025).
Dado: dados/nowandthen_trends_2026.csv
"""
import pandas as pd
import matplotlib.dates as mdates
from beatlenomics_style import make_canvas, VERMELHO, AZUL, PRETO, CINZA

CINZA_LINHA = "#B7B7B5"
df = pd.read_csv("dados/nowandthen_trends_2026.csv", parse_dates=["date"]).set_index("date")
df = df[~df["isPartial"].astype(bool)]
ctrl = ["The Rolling Stones", "Led Zeppelin", "Pink Floyd"]
df["Control"] = df[ctrl].mean(axis=1)

release = pd.Timestamp("2023-11-02")
pre = df.loc[release - pd.Timedelta(weeks=12): release - pd.Timedelta(weeks=1)]
b_pre, c_pre = pre["The Beatles"].mean(), pre["Control"].mean()
df["Counterfactual"] = df["Control"] + (b_pre - c_pre)
df["effect"] = (df["The Beatles"] - b_pre) - (df["Control"] - c_pre)

post = df.loc[release:].copy()
post["quarter"] = ((post.index - release).days // 91) + 1
tab = post.groupby("quarter").agg(start=("effect", lambda s: s.index.min().date()),
                                  effect=("effect", "mean"))
tab["pct_of_baseline"] = tab["effect"] / b_pre * 100
did8 = df.loc[release:release + pd.Timedelta(weeks=8), "effect"].mean()

fig, ax = make_canvas("Three years later, the halo has company",
                      "Google searches for the Beatles vs. control bands, 2023 to 2026. Same diff-in-diff as the original post.",
                      figsize=(11, 8))
ax.set_position([0.09, 0.15, 0.86, 0.52])
x = df.index
ax.plot(x, df["Counterfactual"], color=VERMELHO, lw=1.4, ls=(0, (4, 3)), zorder=3)
m = x >= release
ax.fill_between(x[m], df["Counterfactual"][m], df["The Beatles"][m],
                where=(df["The Beatles"][m] >= df["Counterfactual"][m]),
                color=VERMELHO, alpha=0.14, zorder=1)
ax.plot(x, df["The Beatles"], color=VERMELHO, lw=2.2, zorder=4)
ax.plot(x, df["Control"], color=CINZA_LINHA, lw=1.8, zorder=2)

eventos = [(release, "Now and Then"), (pd.Timestamp("2024-11-29"), "Beatles '64"),
           (pd.Timestamp("2025-11-21"), "Anthology 4\n+ series")]
for d, lab in eventos:
    ax.axvline(d, color=AZUL, lw=1.1, ls=":", zorder=5)
    ax.text(d, 104, " " + lab, color=AZUL, fontsize=9.5, fontweight="bold",
            va="top", ha="left", family="DejaVu Sans")

ax.set_ylim(0, 106)
ax.set_ylabel("Search interest (0-100)", color=CINZA, fontsize=10.5)
ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 7]))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %y"))

q4 = tab.loc[4]
fig.text(0.09, 0.085, f"Original estimate replicates: +{did8:.0f} index points over the first 8 weeks. "
         f"One year out: +{q4.effect:.0f} ({q4.pct_of_baseline:.0f}% of baseline).",
         color=PRETO, fontsize=10.5, family="DejaVu Sans")
fig.text(0.09, 0.055, "After that, two more Beatles releases land in the window, and this design cannot tell them apart.",
         color=PRETO, fontsize=10.5, family="DejaVu Sans")

out = "visuais/c4_3anos.png"
fig.savefig(out, dpi=200)
print("salvo:", out)
print(f"baseline Beatles {b_pre:.2f}, controle {c_pre:.2f}, DiD 8 semanas {did8:.2f}")
print(tab.round(1).to_string())
