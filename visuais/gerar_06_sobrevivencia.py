"""Post 6 — Which songs never retire?
Kaplan-Meier survival analysis of Paul McCartney's live setlist, 1976-2024.
One representative full setlist per tour era (12 eras) gives, per song, the
first and last era it appeared in. "Survival" = still being played some
number of tour-eras after entering rotation; a song still present in the
most recent era (Got Back) is right-censored (still alive), not "immortal".
Split by origin: written/released as a Beatles song vs. Wings/solo.
Dado: dados/paul_setlists_por_turne.csv -> dados/paul_setlist_sobrevivencia.csv.
Fontes por turne: dados/paul_setlists_por_turne_notas.md.
"""
import pandas as pd
import numpy as np
from beatlenomics_style import make_canvas, VERMELHO, AZUL, PRETO, CINZA


def km(durations, events):
    df = pd.DataFrame({"t": durations, "e": events})
    times = sorted(df["t"].unique())
    surv = 1.0
    ts, survs = [0], [1.0]
    for t in times:
        d = ((df["t"] == t) & (df["e"] == 1)).sum()
        n_t = (df["t"] >= t).sum()
        if n_t > 0:
            surv *= (1 - d / n_t)
        ts.append(t)
        survs.append(surv)
    return np.array(ts), np.array(survs)


g = pd.read_csv("dados/paul_setlist_sobrevivencia.csv")
beatles = g[g["grupo"] == "Beatles"]
wings = g[g["grupo"] == "Wings/solo"]

t_b, s_b = km(beatles["duration"], beatles["event"])
t_w, s_w = km(wings["duration"], wings["event"])

fig, ax = make_canvas(
    "Which songs never retire?",
    "Share of songs still in Paul's live rotation, by tour-eras since they first appeared\n(12 eras sampled, 1976-2024). A step down means songs stopped being played that far out.",
    figsize=(11, 7.2))
ax.set_position([0.09, 0.17, 0.86, 0.52])

ax.step(t_b, s_b, where="post", color=VERMELHO, lw=2.6, zorder=4, label="Beatles songs")
ax.step(t_w, s_w, where="post", color=AZUL, lw=2.2, zorder=3, label="Wings / solo songs")

ax.set_ylim(0, 1.02)
ax.set_xlim(0, 12)
ax.set_xlabel("Tour-eras since first appearance", color=CINZA, fontsize=10.5)
ax.set_ylabel("Share still in rotation", color=CINZA, fontsize=10.5)
ax.legend(loc="upper right", frameon=False, fontsize=11)
for spine in ("top", "right"):
    ax.spines[spine].set_visible(False)

fig.text(0.09, 0.09,
         "After 12 tour-eras: 41% of Beatles songs are still in rotation. Of Wings/solo songs, 19%.",
         color=PRETO, fontsize=11, family="DejaVu Sans")
fig.text(0.09, 0.06,
         "A Beatles song that makes the set is roughly twice as likely to still be there decades later.",
         color=PRETO, fontsize=11, family="DejaVu Sans")

out = "visuais/06_sobrevivencia.png"
fig.savefig(out, dpi=200)
print("salvo:", out)
print(f"Beatles t=12: {s_b[-1]:.3f} | Wings/solo t={t_w[-1]}: {s_w[-1]:.3f}")
