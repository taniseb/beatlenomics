"""Post C6 (2o gráfico) — placebo em NÍVEIS, na mesma escala 0-100 do C3 (segunda).
Alinha o interesse de busca dos Beatles no tempo relativo ao tratamento (semana 0)
para a data real do Get Back E para as datas falsas (n dinâmico, 63 na config
atual). Mesmo eixo y de segunda
(search interest 0-100): a linha real dispara até 100, as falsas nunca saem da
faixa dos ~40. Mostra a magnitude do efeito na mesma régua do post de segunda.
Par de quinta: c6_lines.png (gap DiD centrado) + c6_levels.png (este, em níveis).
Dado: dados/getback_trends_raw.csv. Fontes: posts/c6-placebo/referencias.md
"""
import pandas as pd, numpy as np
from beatlenomics_style import make_canvas, VERMELHO, AZUL, PRETO, CINZA

df = pd.read_csv("dados/getback_trends_raw.csv", parse_dates=["date"]).set_index("date").drop(columns=["isPartial"])
weeks = df.index
# semana do índice que contém o lançamento (25-27/nov): início 2021-11-21
real = weeks[weeks.get_indexer([pd.Timestamp("2021-11-25")], method="ffill")[0]]
PRE, POST = 12, 8
ks = np.arange(-PRE, POST + 1)


def level_curve(t):
    """interesse de busca dos Beatles (nível), semanas -12..+8 relativas a t."""
    return np.array([df["The Beatles"].get(t + pd.Timedelta(weeks=int(k)), np.nan) for k in ks], float)


lo = weeks.min() + pd.Timedelta(weeks=PRE)
hi = weeks.max() - pd.Timedelta(weeks=POST)
rel = pd.Timestamp("2021-11-25")
# exclui janelas que tocam o evento real (pré ou pós), p/ não contaminar o placebo
excl = (rel - pd.Timedelta(weeks=10), rel + pd.Timedelta(weeks=16))
placebo_dates = [w for w in weeks if lo <= w <= hi and not (excl[0] <= w <= excl[1])]
n = len(placebo_dates)

fig, ax = make_canvas(
    f"The same spike, tried on {n} other weeks",
    "Beatles search interest around each treatment week. Same 0-100 scale as Monday's chart.",
    figsize=(11, 8))
ax.set_position([0.09, 0.15, 0.86, 0.52])

for t in placebo_dates:
    ax.plot(ks, level_curve(t), color="#B7B7B5", lw=0.8, alpha=0.45, zorder=2)
real_curve = level_curve(real)
ax.plot(ks, real_curve, color=VERMELHO, lw=2.8, zorder=4)

ax.axvline(0, color=AZUL, lw=1.2, ls=":", zorder=3)
ax.text(-0.5, 92, "treatment\nweek", color=AZUL, fontsize=10, fontweight="bold",
        va="center", ha="right", family="DejaVu Sans")

peak_k = int(ks[np.nanargmax(real_curve)])
peak_v = float(np.nanmax(real_curve))
ax.text(peak_k + 1.3, peak_v, "Get Back (real)", color=VERMELHO, fontsize=12,
        fontweight="bold", va="center", ha="left", family="DejaVu Sans")
ax.text(-11.5, 52, f"{n} fake treatment dates", color="#7A7A7A", fontsize=11,
        family="DejaVu Sans")

ax.set_ylim(0, 112)                              # MESMA escala do C3 (segunda)
ax.set_xlim(-PRE, POST)
from matplotlib.ticker import MultipleLocator
ax.xaxis.set_major_locator(MultipleLocator(2))   # semanas inteiras no eixo
ax.set_ylabel("Search interest (0-100)", color=CINZA, fontsize=10.5)
ax.set_xlabel("Weeks relative to treatment", color=CINZA, fontsize=10.5)

fig.text(0.09, 0.085,
         "The real Get Back week is the only line that leaves the pack. It jumps to 2.7x its baseline, to 100.",
         color=PRETO, fontsize=11, family="DejaVu Sans")
fig.text(0.09, 0.055,
         f"The {n} fake dates never break out of the low band. On Monday's own scale, the effect is unmistakable.",
         color=PRETO, fontsize=11, family="DejaVu Sans")

out = "visuais/c6_levels.png"
fig.savefig(out, dpi=200)
print(f"salvo: {out} | placebos={len(placebo_dates)} | pico real {peak_v:.0f} (escala 0-112 do C3)")
