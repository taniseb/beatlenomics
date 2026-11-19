"""Post — Price per song (McCartney Index por música)
dias = preço mais barato inteira / salário mínimo mensal x 30 (mesma unidade do McCartney Index)
horas = preço / salário-hora mínimo. EUA 1965: US$1,25/h (federal). Brasil: mensal / 220 h (jornada CLT).
horas_por_musica = horas / número de músicas no setlist daquele show.
Dado: dados/preco_por_musica.csv
"""
import pandas as pd
from beatlenomics_style import make_canvas, VERMELHO, LARANJA, CINZA, PRETO

df = pd.read_csv("dados/preco_por_musica.csv")
df["dias"] = df.preco_min_inteira / df.salario_min_mensal * 30
df["dias_musica"] = df.dias / df.musicas
df["sal_hora"] = df.apply(lambda r: 1.25 if r.moeda == "USD" else r.salario_min_mensal / 220, axis=1)
df["horas"] = df.preco_min_inteira / df.sal_hora
df["horas_musica"] = df.horas / df.musicas
rot = ["Beatles\nShea, 1965\n12 songs", "Paul\nRio, 2011\n34 songs", "Paul\nRecife, 2012\n38 songs",
       "Paul\nPorto Alegre, 2017\n39 songs", "Paul\nSão Paulo, 2024\n37 songs"]
cores = [VERMELHO] + [LARANJA] * 4

fig, ax = make_canvas("Price per song",
                      "Cheapest full-price ticket divided by songs played,\nin hours of minimum-wage work.",
                      figsize=(10, 9))
ax.bar(range(len(df)), df.horas_musica, width=0.6, color=cores)
for i, h in enumerate(df.horas_musica):
    m = round(h * 60)
    lab = f"{m} min" if m < 60 else f"{m//60}h{m%60:02d}"
    ax.text(i, h + 0.05, lab, ha="center", va="bottom", fontsize=15,
            fontweight="bold", color=PRETO, family="DejaVu Sans")
ax.set_xticks(range(len(df)))
ax.set_xticklabels(rot, fontsize=10, color=CINZA)
ax.set_ylim(0, df.horas_musica.max() * 1.25)
ax.set_ylabel("Hours of minimum wage per song", color=CINZA, fontsize=10.5)

out = "visuais/preco_por_musica.png"
fig.savefig(out, dpi=200)
print("salvo:", out)
print(df[["show", "ano", "preco_min_inteira", "musicas", "horas", "horas_musica"]].round(3).to_string(index=False))
print("razao ingresso SP2024/Shea (horas):", round(df.horas[4] / df.horas[0], 1),
      "| razao por musica:", round(df.horas_musica[4] / df.horas_musica[0], 1))
