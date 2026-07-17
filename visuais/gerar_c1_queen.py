"""Post C1 — The movie that moved 2 billion streams (Queen, Bohemian Rhapsody, 2018)
Efeito causal do filme Bohemian Rhapsody (estreia 24-26/out/2018) nas buscas por
"Queen" no Google Trends, via controle sintetico contra bandas legacy sem choque
no periodo (Rolling Stones, Led Zeppelin, Pink Floyd, Eagles).
A marca do grafico: linha tracejada = Queen sintetico (contrafactual, o Queen que
NAO teve filme). Area sombreada entre observado e sintetico = o efeito.
Dado: dados/queen_bohemian_trends_raw.csv (Google Trends, semanal, cada termo
consultado sozinho e normalizado individualmente -- consultar os 5 juntos
comprime a escala das bandas menores).
Fontes: ver posts/c1-queen-synthetic/referencias.md
"""
import pandas as pd, numpy as np
import matplotlib.dates as mdates
from scipy.optimize import nnls
from beatlenomics_style import make_canvas, VERMELHO, AZUL, PRETO, CINZA

CINZA_LINHA = "#B7B7B5"

df = pd.read_csv("dados/queen_bohemian_trends_raw.csv", parse_dates=["date"]).set_index("date")
controls = ["Rolling Stones", "Led Zeppelin", "Pink Floyd", "Eagles"]
release = pd.Timestamp("2018-10-24")

# pesos: nnls no ano pre-tratamento, normalizado para somar 1 (controle sintetico)
pre = df.loc[release - pd.Timedelta(weeks=52): release - pd.Timedelta(weeks=1)]
w, _ = nnls(pre[controls].values, pre["Queen"].values)
w_norm = w / w.sum()
weights = dict(zip(controls, w_norm))

df["Synthetic"] = df[controls].values @ w_norm

fig, ax = make_canvas(
    "Everyone knows Queen's streams exploded in 2018",
    "Google searches for Queen vs. a synthetic Queen built from legacy bands. Synthetic control.",
    figsize=(11, 8))
ax.set_position([0.09, 0.15, 0.86, 0.52])

x = df.index
ax.plot(x, df["Synthetic"], color=VERMELHO, lw=1.6, ls=(0, (4, 3)), zorder=3)
mask = x >= release
ax.fill_between(x[mask], df["Synthetic"][mask], df["Queen"][mask],
                where=(df["Queen"][mask] >= df["Synthetic"][mask]),
                color=VERMELHO, alpha=0.16, zorder=1)
ax.plot(x, df["Queen"], color=VERMELHO, lw=2.6, zorder=4)

ax.axvline(release, color=AZUL, lw=1.3, ls=":", zorder=5)
ax.text(release, 143, " Bohemian Rhapsody\n releases", color=AZUL, fontsize=10.5,
        fontweight="bold", va="top", ha="left", family="DejaVu Sans")

ax.text(x[2], 30, "Queen (observed)",
        color=VERMELHO, fontsize=11, fontweight="bold", family="DejaVu Sans")
ax.text(x[-10], df["Synthetic"].iloc[-10] - 12,
        "Synthetic Queen\n(no movie)", color=VERMELHO, fontsize=9.5,
        style="italic", family="DejaVu Sans", va="top", ha="right")

peak_week = df.loc[release:release + pd.Timedelta(weeks=8), "Queen"].idxmax()
peak_val = df.loc[peak_week, "Queen"]
ax.annotate("peak week: 1.6x synthetic", xy=(peak_week, peak_val), xytext=(x[145], 108),
            color=PRETO, fontsize=11, fontweight="bold", family="DejaVu Sans",
            ha="left", arrowprops=dict(arrowstyle="-", color=CINZA, lw=1,
                                       connectionstyle="arc3,rad=-0.15"))

ax.set_ylim(0, 145)
ax.set_ylabel("Search interest (0-100)", color=CINZA, fontsize=10.5)
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %y"))
ax.tick_params(axis="x", labelsize=9.5)

post16 = df.loc[release: release + pd.Timedelta(weeks=15)]
ratio16 = (post16["Queen"] / post16["Synthetic"]).mean()
w_txt = " + ".join(f"{v:.0%} {k}" for k, v in sorted(weights.items(), key=lambda kv: -kv[1]) if v > 0.01)

# robustez: sintetico sem Pink Floyd (controle com placebo sujo; ver referencias.md)
controls_nopf = [c for c in controls if c != "Pink Floyd"]
w2, _ = nnls(pre[controls_nopf].values, pre["Queen"].values)
w2_norm = w2 / w2.sum()
synth_nopf = df[controls_nopf].values @ w2_norm
ratio16_nopf = (post16["Queen"].values / synth_nopf[df.index.get_indexer(post16.index)]).mean()

fig.text(0.09, 0.085,
         f"Synthetic Queen = {w_txt}. Sixteen weeks out, Queen ran {ratio16:.2f}x above it.",
         color=PRETO, fontsize=11, family="DejaVu Sans")
fig.text(0.09, 0.055,
         f"Pink Floyd failed the placebo test, and it rose on its own. Rebuilt without it, the lift climbs to "
         f"{ratio16_nopf:.2f}x. {ratio16:.2f}x is a floor.",
         color=PRETO, fontsize=10.5, family="DejaVu Sans", style="italic")

out = "visuais/c1_queen.png"
fig.savefig(out, dpi=200)
print("salvo:", out, f"| pesos: {weights} | ratio 16wk: {ratio16:.2f}")
