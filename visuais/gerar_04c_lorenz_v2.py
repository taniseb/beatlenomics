"""Post 4 — curva de Lorenz COM identidade visual #beatlenomics."""
import pandas as pd, numpy as np
import matplotlib.pyplot as plt
from beatlenomics_style import make_canvas, VERMELHO, CINZA, PRETO, LARANJA

d = pd.read_csv("dados/paul_setlist_full.csv")
asc = d.sort_values("performances").reset_index(drop=True)   # menor -> maior
p = asc["performances"].values
n = len(p)
cum = np.insert(np.cumsum(p), 0, 0) / p.sum()
x = np.linspace(0, 1, n + 1)
gini = (n + 1 - 2*np.sum(np.cumsum(p))/np.cumsum(p)[-1]) / n

# --- destaque pessoal: música favorita da Tanise ---
fav = asc.index[asc["song"].str.contains("Ob-La-Di", case=False)][0]  # idx ascendente
fav_x = (fav + 1) / n
fav_y = cum[fav + 1]

fig, ax = make_canvas(
    "Paul's setlist is wildly unequal",
    "117 songs played just once · 48% of the catalogue played ≤5 times")

ax.plot([0, 1], [0, 1], "--", color=CINZA, lw=1.4, label="Perfect equality")
ax.plot(x, cum, color=VERMELHO, lw=3.2, label=f"Paul's setlist (Gini = {gini:.2f})")
ax.fill_between(x, cum, x, color=VERMELHO, alpha=0.10)

ax.annotate("Bottom 50% of songs\n= 1% of stage time",
            xy=(0.5, cum[n//2]), xytext=(0.16, 0.46), fontsize=11, color=PRETO,
            arrowprops=dict(arrowstyle="->", color=PRETO))

# destaque pessoal: Ob-La-Di, Ob-La-Da (favorita da Tanise)
ax.scatter([fav_x], [fav_y], s=120, color=LARANJA, edgecolor="white",
           lw=1.5, zorder=6)
ax.annotate('My pick: "Ob-La-Di, Ob-La-Da"\n395 plays · top 6% of 373 songs',
            xy=(fav_x, fav_y), xytext=(0.40, 0.78), fontsize=10.5,
            color=LARANJA, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=LARANJA, lw=1.5))

ax.set_xlim(0, 1); ax.set_ylim(0, 1)
ax.set_xlabel("Cumulative share of songs (373 total)", fontsize=11, color=PRETO)
ax.set_ylabel("Cumulative share of performances", fontsize=11, color=PRETO)
ax.legend(loc="upper left", frameon=False, fontsize=11)
ticks = np.arange(0, 1.1, 0.25)
ax.set_xticks(ticks); ax.set_yticks(ticks)
ax.set_xticklabels([f"{int(v*100)}%" for v in ticks])
ax.set_yticklabels([f"{int(v*100)}%" for v in ticks])

out = "visuais/04c_lorenz_v2.png"
fig.savefig(out, dpi=200)
print("salvo:", out)
