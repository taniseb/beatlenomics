"""Post — If Paul's setlist were a market
HHI (Herfindahl-Hirschman Index) of catalogue share (Beatles / Wings /
solo+covers) in Paul McCartney's live setlist, 12 tour eras, 1976-2024.
Catalogue classification inherited from the survival-analysis post
(dados/paul_setlist_sobrevivencia.csv), split further into Wings vs solo.
Dado: dados/paul_setlist_hhi.csv. Fontes: posts/setlist-hhi/referencias.md.
"""
import pandas as pd
from beatlenomics_style import make_canvas, VERMELHO, AZUL, LARANJA, PRETO, CINZA

df = pd.read_csv("dados/paul_setlist_hhi.csv")

fig, ax = make_canvas(
    "If Paul's setlist were a market",
    "Catalogue share of Paul's live setlist (Beatles / Wings / solo & covers), 12 tour eras,\n1976-2024. HHI (line, right axis) against the antitrust thresholds for market concentration.",
    figsize=(11, 7.5))
ax.set_position([0.09, 0.19, 0.78, 0.50])

x = df["ano"]
ax.stackplot(x, df["share_Beatles"] * 100, df["share_Wings"] * 100, df["share_Solo/covers"] * 100,
             colors=[VERMELHO, LARANJA, "#8C8C8A"],
             labels=["Beatles", "Wings", "Solo & covers"], alpha=0.92, zorder=2)
ax.set_ylim(0, 100)
ax.set_ylabel("Share of setlist slots (%)", color=CINZA, fontsize=10.5)
ax.legend(loc="lower right", frameon=False, fontsize=10, ncol=3)
ax.set_xticks(x)
ax.tick_params(axis="x", rotation=45)

ax2 = ax.twinx()
ax2.plot(x, df["hhi"], color=PRETO, lw=2.4, marker="o", ms=6, zorder=5)
ax2.axhline(1500, color=AZUL, lw=1, ls=":", zorder=1)
ax2.axhline(2500, color=AZUL, lw=1, ls="--", zorder=1)
ax2.text(x.iloc[0], 1560, "moderately concentrated (1,500)", fontsize=8.5, color=AZUL, family="DejaVu Sans")
ax2.text(x.iloc[0], 2560, "highly concentrated (2,500)", fontsize=8.5, color=AZUL, family="DejaVu Sans")
ax2.set_ylim(0, 7000)
ax2.set_ylabel("HHI", color=PRETO, fontsize=10.5)

last = df.iloc[-1]
first = df.iloc[0]
fig.text(0.09, 0.10,
         f"1976: Wings held {first['share_Wings']*100:.0f}% of the set. 2024: Beatles hold {last['share_Beatles']*100:.0f}%, "
         f"HHI at {last['hhi']:.0f}.",
         color=PRETO, fontsize=11, family="DejaVu Sans")
fig.text(0.09, 0.065,
         "Every single era on record sits above the \"highly concentrated\" line. The dominant firm dissolved in 1970.",
         color=PRETO, fontsize=11, family="DejaVu Sans")

out = "visuais/setlist_hhi.png"
fig.savefig(out, dpi=200)
print("salvo:", out)
print(df[["ano","hhi","share_Beatles","share_Wings","share_Solo/covers"]].round(3).to_string(index=False))
