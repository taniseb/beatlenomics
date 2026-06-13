"""Post 4, slide 1 (gancho) com identidade #beatlenomics.
Assimetria: 12% da carreira gera 65% do tempo de palco.
"""
import numpy as np
from beatlenomics_style import make_canvas, VERMELHO, AZUL, PRETO, CINZA

# Share dos anos de carreira: Beatles 1962-70 (~8a) vs pos-Beatles 1970-2026 (~56a)
anos = (8/64*100, 56/64*100)
# Share das performances (top 52): Beatles 65.1% vs resto 34.9%
palco = (65.1, 34.9)

fig, ax = make_canvas(
    "Eight years, two thirds of the setlist",
    "Demand sticks to the legacy catalogue, not to 50 years of new output",
    figsize=(9, 9))
ax.set_position([0.28, 0.24, 0.64, 0.44])   # mais espaço p/ rótulos e legenda

metrics = ["Career years", "Songs played live"]
beatles = [anos[0], palco[0]]
resto = [anos[1], palco[1]]
y = np.arange(len(metrics))
h = 0.5

ax.barh(y, beatles, h, color=VERMELHO, label="Beatles era (1962 to 1970)")
ax.barh(y, resto, h, left=beatles, color=AZUL, label="Solo and Wings (1970 to today)")
for i, (b, r) in enumerate(zip(beatles, resto)):
    ax.text(b/2, i, f"{b:.0f}%", ha="center", va="center",
            color="white", fontweight="bold", fontsize=15)
    ax.text(b + r/2, i, f"{r:.0f}%", ha="center", va="center",
            color="white", fontweight="bold", fontsize=15)

ax.set_yticks(y); ax.set_yticklabels(metrics, fontsize=12, color=PRETO)
ax.invert_yaxis()
ax.set_xlim(0, 100)
ax.set_xticks([0, 25, 50, 75, 100])
ax.set_xticklabels(["0%", "25%", "50%", "75%", "100%"])
ax.spines["left"].set_visible(False)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=1,
          frameon=False, fontsize=10)

out = "visuais/04b_v2.png"
fig.savefig(out, dpi=200)
print("salvo:", out)
