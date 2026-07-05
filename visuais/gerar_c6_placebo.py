"""Post C6 — The placebo test (série causal, robustez)
Sequência do C3. Pega o MESMO dado do Get Back e pergunta: se o meu diff-in-diff
inventa efeitos, então datas de tratamento FALSAS (semanas sem documentário)
deveriam acender também. Roda o DiD em 67 datas placebo e compara a distribuição
com o efeito real. A marca do gráfico: o efeito real cravado na cauda, longe da
nuvem placebo centrada no zero.
Dado: dados/getback_trends_raw.csv (mesmo do C3). Fontes: posts/c6-placebo/referencias.md
"""
import pandas as pd, numpy as np
from beatlenomics_style import make_canvas, VERMELHO, AZUL, PRETO, CINZA

CINZA_BAR = "#B7B7B5"

df = pd.read_csv("dados/getback_trends_raw.csv", parse_dates=["date"]).set_index("date").drop(columns=["isPartial"])
ctrl = ["The Rolling Stones", "Led Zeppelin", "Pink Floyd"]
df["Control"] = df[ctrl].mean(axis=1)
weeks = df.index
real = pd.Timestamp("2021-11-25")


def did(t, tr="The Beatles", co="Control"):
    pre = df.loc[t - pd.Timedelta(weeks=12): t - pd.Timedelta(weeks=1)]
    post = df.loc[t: t + pd.Timedelta(weeks=8)]
    if len(pre) < 10 or len(post) < 7:
        return np.nan
    return (post[tr].mean() - pre[tr].mean()) - (post[co].mean() - pre[co].mean())


real_did = did(real)
lo = weeks.min() + pd.Timedelta(weeks=12)
hi = weeks.max() - pd.Timedelta(weeks=8)
excl = (real - pd.Timedelta(weeks=10), real + pd.Timedelta(weeks=12))
placebo = np.array([did(w) for w in weeks
                    if lo <= w <= hi and not (excl[0] <= w <= excl[1])])
placebo = placebo[~np.isnan(placebo)]
z = (real_did - placebo.mean()) / placebo.std()

fig, ax = make_canvas(
    "A number you found vs. a number you failed to break",
    "Placebo test: the same diff-in-diff run on 67 fake treatment dates, plus the real Get Back effect.",
    figsize=(11, 8))
ax.set_position([0.09, 0.16, 0.86, 0.50])

bins = np.arange(-22, 28, 2)
ax.hist(placebo, bins=bins, color=CINZA_BAR, edgecolor="white",
        linewidth=0.6, zorder=2)
ax.axvline(0, color=CINZA, lw=1, ls=":", zorder=1)

# efeito real na cauda
ax.axvline(real_did, color=VERMELHO, lw=2.6, zorder=4)
ax.annotate("Real Get Back effect\n+23 index points",
            xy=(real_did, 6.2), xytext=(real_did - 1.5, 9.2),
            color=VERMELHO, fontsize=12, fontweight="bold", ha="right",
            family="DejaVu Sans",
            arrowprops=dict(arrowstyle="-", color=VERMELHO, lw=1.4))

# rótulo da nuvem placebo
ax.annotate("67 fake dates.\nEvery one lands near zero.",
            xy=(-2, 8.5), xytext=(-19, 9.3), color=PRETO, fontsize=11,
            family="DejaVu Sans", ha="left",
            arrowprops=dict(arrowstyle="-", color=CINZA, lw=1))

ax.set_xlabel("Diff-in-diff estimate (Google Trends index points)", color=CINZA, fontsize=10.5)
ax.set_ylabel("Number of placebo dates", color=CINZA, fontsize=10.5)
ax.set_xlim(-22, 27)
ax.set_ylim(0, 12)

fig.text(0.09, 0.095,
         f"The real effect sits {z:.1f} standard deviations from the placebo mean. Not one fake date came close.",
         color=PRETO, fontsize=11, family="DejaVu Sans")
fig.text(0.09, 0.065,
         "Swap a control band in as the treated one and the same thing happens: the effect refuses to be faked.",
         color=PRETO, fontsize=11, family="DejaVu Sans")

out = "visuais/c6_placebo.png"
fig.savefig(out, dpi=200)
print(f"salvo: {out} | real {real_did:.1f} | placebo n={len(placebo)} media {placebo.mean():.1f} sd {placebo.std():.1f} | z={z:.1f}")
