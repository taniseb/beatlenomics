"""Post C4 — Now and Then: the halo effect on the catalogue
Efeito causal do lancamento de "Now and Then" (02/nov/2023) nas buscas por
"The Beatles" no Google Trends, via diff-in-diff contra bandas legacy sem
choque no periodo (Rolling Stones, Led Zeppelin, Pink Floyd). Mesmo estimador
do C3 (gerar_c3_getback.py), outra data de tratamento e outro dado bruto.
A marca do grafico: a linha tracejada = contrafactual (o Beatles que NAO teve
a musica nova). A area sombreada entre o observado e o contrafactual = o efeito.
Dado: dados/nowandthen_trends_raw.csv (Google Trends, semanal, mai/2023-fev/2024).
Fontes: ver posts/c4-nowandthen-halo/referencias.md
"""
import pandas as pd, numpy as np
import matplotlib.dates as mdates
from beatlenomics_style import make_canvas, VERMELHO, AZUL, PRETO, CINZA

CINZA_LINHA = "#B7B7B5"

df = pd.read_csv("dados/nowandthen_trends_raw.csv", parse_dates=["date"]).set_index("date")
ctrl = ["The Rolling Stones", "Led Zeppelin", "Pink Floyd"]
df["Control"] = df[ctrl].mean(axis=1)

release = pd.Timestamp("2023-11-02")
pre = df.loc[release - pd.Timedelta(weeks=12): release - pd.Timedelta(weeks=1)]
b_pre, c_pre = pre["The Beatles"].mean(), pre["Control"].mean()
gap = b_pre - c_pre
df["Counterfactual"] = df["Control"] + gap

fig, ax = make_canvas(
    "A new song, and the old ones got a lift too",
    "Google searches for the Beatles vs. control bands, around the Now and Then release. Diff-in-diff.",
    figsize=(11, 8))
ax.set_position([0.09, 0.15, 0.86, 0.52])

x = df.index
ax.plot(x, df["Counterfactual"], color=VERMELHO, lw=1.6, ls=(0, (4, 3)), zorder=3)
mask = x >= release
ax.fill_between(x[mask], df["Counterfactual"][mask], df["The Beatles"][mask],
                where=(df["The Beatles"][mask] >= df["Counterfactual"][mask]),
                color=VERMELHO, alpha=0.16, zorder=1)
ax.plot(x, df["The Beatles"], color=VERMELHO, lw=2.6, zorder=4)
ax.plot(x, df["Control"], color=CINZA_LINHA, lw=2.0, zorder=2)

ax.axvline(release, color=AZUL, lw=1.3, ls=":", zorder=5)
ax.text(release, 116, " Nov 2:\n song\n releases", color=AZUL, fontsize=10.5,
        fontweight="bold", va="top", ha="left", family="DejaVu Sans")

ax.text(x[2], df["The Beatles"].iloc[2] + 4, "The Beatles (observed)",
        color=VERMELHO, fontsize=11, fontweight="bold", family="DejaVu Sans")
ax.text(x[-14], df["Counterfactual"].iloc[-14] - 9,
        "Beatles counterfactual\n(no new song)", color=VERMELHO, fontsize=9.5,
        style="italic", family="DejaVu Sans", va="top")
ax.text(x[10], df["Control"].iloc[10] - 8,
        "Control bands\n(Stones, Zeppelin, Pink Floyd)", color="#7A7A7A",
        fontsize=9.5, family="DejaVu Sans", va="top")

peak_week = df["The Beatles"].idxmax()
peak_val = df.loc[peak_week, "The Beatles"]
ax.annotate(f"peak: {peak_val/b_pre:.1f}x baseline\n(release week itself;\nteaser + announcement week was already +27%)",
            xy=(peak_week, peak_val), xytext=(x[13], 100),
            color=PRETO, fontsize=10.5, fontweight="bold", family="DejaVu Sans",
            ha="left", arrowprops=dict(arrowstyle="-", color=CINZA, lw=1,
                                       connectionstyle="arc3,rad=0.2"))

ax.set_ylim(0, 118)
ax.set_ylabel("Search interest (0-100)", color=CINZA, fontsize=10.5)
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %y"))

did = (df.loc[release:release+pd.Timedelta(weeks=8), "The Beatles"].mean() - b_pre) \
      - (df.loc[release:release+pd.Timedelta(weeks=8), "Control"].mean() - c_pre)
late = df.loc[release+pd.Timedelta(weeks=12):release+pd.Timedelta(weeks=16)]
late_gap = (late["The Beatles"].mean() - b_pre) - (late["Control"].mean() - c_pre)
fig.text(0.09, 0.085,
         f"The gap after the dotted line is the effect: +{did:.0f} index points over 8 weeks,",
         color=PRETO, fontsize=11, family="DejaVu Sans")
fig.text(0.09, 0.055,
         f"a smaller pulse than a documentary gets. But 3 months out it was still +{late_gap:.0f} pts above baseline. This one stuck.",
         color=PRETO, fontsize=11, family="DejaVu Sans")

out = "visuais/c4_nowandthen.png"
fig.savefig(out, dpi=200)
print("salvo:", out, f"| DiD 8sem = +{did:.1f} pts | late gap (12-16sem) = +{late_gap:.1f} pts"
      f" | baseline Beatles {b_pre:.1f} -> peak {peak_val}")
