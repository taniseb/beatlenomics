"""Post 9 — Paul at 80+, still playing full sets
No decline in setlist length across the 13 shows Tanise saw him play,
from age 68 (2010) to age 82 (2024). Same data source as the 13-shows
post, recombined with his birth date to compute age per show.
Dado: dados/meus_13_shows.csv + dados/meus_13_shows_musicas.csv.
"""
import pandas as pd
import matplotlib.dates as mdates
from beatlenomics_style import make_canvas, VERMELHO, PRETO, CINZA

shows = pd.read_csv("dados/meus_13_shows.csv", parse_dates=["data"])
songs = pd.read_csv("dados/meus_13_shows_musicas.csv")
counts = songs.groupby("show_num").size()
BIRTH = pd.Timestamp("1942-06-18")
shows["idade"] = (shows["data"] - BIRTH).dt.days / 365.25
shows["n_musicas"] = shows["show_num"].map(counts)
shows = shows.sort_values("data")

fig, ax = make_canvas(
    "Turning 80 didn't shorten the set",
    "Songs played per show Tanise attended, by Paul McCartney's age on that night.",
    figsize=(11, 7))
ax.set_position([0.09, 0.16, 0.86, 0.55])

x = shows["idade"]
y = shows["n_musicas"]
ax.scatter(x, y, s=90, color=VERMELHO, zorder=3)
z = pd.Series(y.values).rolling(3, center=True, min_periods=1).mean()
ax.plot(x, z, color=CINZA, lw=2, ls=(0, (4, 3)), zorder=2)

for _, r in shows.iterrows():
    ax.annotate(f"{r['cidade']}\n{r['data'].year}", (r["idade"], r["n_musicas"]),
                textcoords="offset points", xytext=(0, 10), ha="center",
                fontsize=8, color=CINZA, family="DejaVu Sans")

ax.axvline(80, color=PRETO, lw=1.1, ls=":", zorder=1)
ax.text(80.1, y.min() - 1, "turns 80", fontsize=9.5, color=PRETO,
        family="DejaVu Sans", va="top")

ax.set_xlabel("Paul's age on the night", color=CINZA, fontsize=10.5)
ax.set_ylabel("Songs played", color=CINZA, fontsize=10.5)
ax.set_ylim(min(y) - 3, max(y) + 4)

pre80 = shows[shows["idade"] < 80]["n_musicas"].mean()
post80 = shows[shows["idade"] >= 80]["n_musicas"].mean()
fig.text(0.09, 0.085,
         f"Average setlist before 80: {pre80:.0f} songs. At 80 or older: {post80:.0f} songs.",
         color=PRETO, fontsize=11, family="DejaVu Sans")
fig.text(0.09, 0.055,
         "Thirteen shows, fourteen years, no fatigue discount in the data.",
         color=PRETO, fontsize=11, family="DejaVu Sans")

out = "visuais/09_paul80.png"
fig.savefig(out, dpi=200)
print("salvo:", out, f"| media pre-80={pre80:.1f} | media 80+={post80:.1f}")
