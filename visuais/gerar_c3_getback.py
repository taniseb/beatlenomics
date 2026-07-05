"""Post C3 — Did Get Back move the catalogue? (DiD didático)
Efeito causal do documentário Get Back (Disney+, 25-27/nov/2021) nas buscas
por "The Beatles" no Google Trends, via diff-in-diff contra bandas legacy sem
choque no período (Rolling Stones, Led Zeppelin, Pink Floyd).
A marca do gráfico: a linha tracejada = contrafactual (o Beatles que NÃO teve
documentário). A área sombreada entre o observado e o contrafactual = o efeito.
Dado: dados/getback_trends_raw.csv (Google Trends, semanal, mai/2020-jun/2022).
Fontes: ver posts/c3-get-back-did/referencias.md
"""
import pandas as pd, numpy as np
import matplotlib.dates as mdates
from beatlenomics_style import make_canvas, VERMELHO, AZUL, PRETO, CINZA

CINZA_LINHA = "#B7B7B5"

df = pd.read_csv("dados/getback_trends_raw.csv", parse_dates=["date"]).set_index("date")
ctrl = ["The Rolling Stones", "Led Zeppelin", "Pink Floyd"]
df["Control"] = df[ctrl].mean(axis=1)

release = pd.Timestamp("2021-11-25")
pre = df.loc[release - pd.Timedelta(weeks=12): release - pd.Timedelta(weeks=1)]
b_pre, c_pre = pre["The Beatles"].mean(), pre["Control"].mean()
gap = b_pre - c_pre                      # gap pré-tratamento (tend. paralelas)
df["Counterfactual"] = df["Control"] + gap   # Beatles contrafactual

fig, ax = make_canvas(
    "The week a 52-year-old band went viral again",
    "Google searches for the Beatles vs. control bands, around the Get Back release. Diff-in-diff.",
    figsize=(11, 8))
ax.set_position([0.09, 0.15, 0.86, 0.52])

x = df.index
# contrafactual (o Beatles sem documentário) + área do efeito
ax.plot(x, df["Counterfactual"], color=VERMELHO, lw=1.6, ls=(0, (4, 3)), zorder=3)
mask = x >= release
ax.fill_between(x[mask], df["Counterfactual"][mask], df["The Beatles"][mask],
                where=(df["The Beatles"][mask] >= df["Counterfactual"][mask]),
                color=VERMELHO, alpha=0.16, zorder=1)
# séries observadas
ax.plot(x, df["The Beatles"], color=VERMELHO, lw=2.6, zorder=4)
ax.plot(x, df["Control"], color=CINZA_LINHA, lw=2.0, zorder=2)

# linha do tratamento
ax.axvline(release, color=AZUL, lw=1.3, ls=":", zorder=5)
ax.text(release, 104, " Get Back\n releases", color=AZUL, fontsize=10.5,
        fontweight="bold", va="top", ha="left", family="DejaVu Sans")

# rótulos das linhas
ax.text(x[2], df["The Beatles"].iloc[2] + 4, "The Beatles (observed)",
        color=VERMELHO, fontsize=11, fontweight="bold", family="DejaVu Sans")
ax.text(x[-14], df["Counterfactual"].iloc[-14] - 11,
        "Beatles counterfactual\n(no documentary)", color=VERMELHO, fontsize=9.5,
        style="italic", family="DejaVu Sans", va="top")
ax.text(x[10], df["Control"].iloc[10] - 12,
        "Control bands\n(Stones, Zeppelin, Pink Floyd)", color="#7A7A7A",
        fontsize=9.5, family="DejaVu Sans", va="top")

# anotação do pico
peak_week = pd.Timestamp("2021-11-28")
ax.annotate("2.7x baseline", xy=(peak_week, 100), xytext=(x[62], 92),
            color=PRETO, fontsize=11, fontweight="bold", family="DejaVu Sans",
            arrowprops=dict(arrowstyle="-", color=CINZA, lw=1))

ax.set_ylim(0, 112)
ax.set_ylabel("Search interest (0-100)", color=CINZA, fontsize=10.5)
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %y"))

# fecho: o número
did = (df.loc[release:release+pd.Timedelta(weeks=8), "The Beatles"].mean() - b_pre) \
      - (df.loc[release:release+pd.Timedelta(weeks=8), "Control"].mean() - c_pre)
fig.text(0.09, 0.085,
         f"The gap after the dotted line is the effect: +{did:.0f} index points over 8 weeks,",
         color=PRETO, fontsize=11, family="DejaVu Sans")
fig.text(0.09, 0.055,
         "a +63% lift the control bands never got. Then it faded. Documentaries are a pulse, not a plateau.",
         color=PRETO, fontsize=11, family="DejaVu Sans")

out = "visuais/c3_getback.png"
fig.savefig(out, dpi=200)
print("salvo:", out, f"| DiD = +{did:.1f} pts | baseline Beatles {b_pre:.1f} -> peak 100")
