"""Post C6 (alternativa visual) — placebo em formato event-study, no estilo do C3.
Em vez de histograma, alinha cada data de tratamento (a real do Get Back + as
falsas; n dinâmico, 63 na config atual) no tempo relativo (semana 0 = tratamento)
e plota o gap DiD ao longo
das semanas. As placebo viram um feixe cinza colado no zero; a real dispara.
Mesma gramática visual do C3 (linhas no tempo + destaque vermelho), pra o par
segunda/quinta ficar coeso.
Dado: dados/getback_trends_raw.csv. Fontes: posts/c6-placebo/referencias.md
"""
import pandas as pd, numpy as np
from beatlenomics_style import make_canvas, VERMELHO, AZUL, PRETO, CINZA

df = pd.read_csv("dados/getback_trends_raw.csv", parse_dates=["date"]).set_index("date").drop(columns=["isPartial"])
ctrl = ["The Rolling Stones", "Led Zeppelin", "Pink Floyd"]
df["gap"] = df["The Beatles"] - df[ctrl].mean(axis=1)   # diferença tratado - controle
weeks = df.index
# pytrends rotula a semana pela data de INÍCIO; a semana do lançamento (25-27/nov)
# é a que começa em 2021-11-21. ffill = última data do índice <= o lançamento.
real = weeks[weeks.get_indexer([pd.Timestamp("2021-11-25")], method="ffill")[0]]
PRE, POST = 12, 8
ks = np.arange(-PRE, POST + 1)


def event_curve(t):
    """gap DiD centrado no baseline pré, semanas -12..+8 relativas a t."""
    vals = []
    for k in ks:
        d = t + pd.Timedelta(weeks=int(k))
        vals.append(df["gap"].get(d, np.nan))
    vals = np.array(vals, float)
    base = np.nanmean(vals[ks < 0])
    return vals - base


lo = weeks.min() + pd.Timedelta(weeks=PRE)
hi = weeks.max() - pd.Timedelta(weeks=POST)
# exclui janelas que tocam o evento real (pré ou pós), p/ não contaminar o placebo
rel = pd.Timestamp("2021-11-25")
excl = (rel - pd.Timedelta(weeks=10), rel + pd.Timedelta(weeks=16))
placebo_dates = [w for w in weeks if lo <= w <= hi and not (excl[0] <= w <= excl[1])]
n = len(placebo_dates)

fig, ax = make_canvas(
    "The placebo test, in one chart",
    f"Same diff-in-diff, aligned at the treatment week. The real Get Back effect vs. {n} fake dates.",
    figsize=(11, 8))
ax.set_position([0.09, 0.16, 0.86, 0.50])

# feixe placebo (cinza, fino, transparente)
for t in placebo_dates:
    ax.plot(ks, event_curve(t), color="#B7B7B5", lw=0.8, alpha=0.45, zorder=2)
# efeito real (vermelho grosso)
real_curve = event_curve(real)
ax.plot(ks, real_curve, color=VERMELHO, lw=2.8, zorder=4)

ax.axhline(0, color=CINZA, lw=1, ls=":", zorder=1)
ax.axvline(0, color=AZUL, lw=1.2, ls=":", zorder=3)

peak_k = int(ks[np.nanargmax(real_curve)])
peak_v = float(np.nanmax(real_curve))
ax.set_ylim(-35, peak_v + 14)

# rótulo do tratamento à ESQUERDA da linha, na região vazia do pré (sem tocar o vermelho)
ax.text(-0.5, 44, "treatment\nweek", color=AZUL, fontsize=10, fontweight="bold",
        va="center", ha="right", family="DejaVu Sans")
# rótulo do efeito real acima e à direita do pico
ax.text(peak_k + 1.3, peak_v + 5, "Get Back (real)", color=VERMELHO, fontsize=12,
        fontweight="bold", va="bottom", ha="left", family="DejaVu Sans")
ax.text(-11.5, 8, f"{n} fake treatment dates", color="#7A7A7A", fontsize=11,
        family="DejaVu Sans")

ax.set_xlabel("Weeks relative to treatment", color=CINZA, fontsize=10.5)
ax.set_ylabel("DiD gap vs. pre-baseline (index pts)", color=CINZA, fontsize=10.5)
ax.set_xlim(-PRE, POST)
from matplotlib.ticker import MultipleLocator
ax.xaxis.set_major_locator(MultipleLocator(2))   # semanas inteiras no eixo

peak = np.nanmax(real_curve)
fig.text(0.09, 0.095,
         "Before the treatment week, everything hugs zero. That co-movement is the parallel-trends check.",
         color=PRETO, fontsize=11, family="DejaVu Sans")
fig.text(0.09, 0.065,
         f"After it, only the real line jumps (about +{peak:.0f} at its peak). The {len(placebo_dates)} fakes never leave the flat band.",
         color=PRETO, fontsize=11, family="DejaVu Sans")

out = "visuais/c6_lines.png"
fig.savefig(out, dpi=200)
print(f"salvo: {out} | anchor={real.date()} | placebos={len(placebo_dates)} | pico real +{peak:.1f}")
