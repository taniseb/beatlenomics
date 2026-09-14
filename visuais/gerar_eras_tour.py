"""Post - McCartney Index vs Eras Tour (Sao Paulo, 2023)
Mesma regua do McCartney Index: dias de salario minimo brasileiro pelo ticket
mais barato SEM visao restrita, mesma cidade (Sao Paulo, Allianz Parque), mesmo
ano (2023). McCartney (Got Back, dez/2023): R$420 (Cadeira Superior). Eras Tour
(nov/2023): R$500 inteira / Cadeira Superior (tiers de visao parcial excluidos
pela mesma regra do McCartney Index). Pista Premium adicionada so como
contraste do tier mais caro.
Dado: dados/paul_brasil_ao_longo_tempo.csv (McCartney) + pesquisa nova (Eras
Tour), ver posts/mccartney-index-eras-tour/referencias.md.
"""
from beatlenomics_style import make_canvas, VERMELHO, AZUL, PRETO, CINZA

salario_min_2023 = 1320.0

itens = [
    ("Paul McCartney\n(Cadeira Superior, R$420)", 420.0, AZUL),
    ("Eras Tour\n(Cadeira Superior, R$500)", 500.0, VERMELHO),
    ("Paul McCartney\n(Cadeira Inferior, R$780)", 780.0, "#5588AA"),
    ("Eras Tour\n(Cadeira Inferior, R$750)", 750.0, "#E06666"),
    ("Paul McCartney\n(Pista Premium, R$990)", 990.0, "#7FA8C9"),
    ("Eras Tour\n(Pista Premium, R$1.050)", 1050.0, "#F2A9A9"),
]
dias = [(nome, (preco / salario_min_2023) * 30, cor) for nome, preco, cor in itens]

fig, ax = make_canvas(
    "McCartney Index vs Eras Tour",
    "Sao Paulo, 2023: all three matching ticket tiers, days of Brazilian minimum wage",
    figsize=(11, 9))
ax.set_position([0.32, 0.20, 0.62, 0.55])

y = range(len(dias))
ax.barh(y, [d for _, d, _ in dias], color=[c for _, _, c in dias], height=0.55, zorder=3)
ax.set_yticks(list(y))
ax.set_yticklabels([n for n, _, _ in dias], fontsize=10.5, family="DejaVu Sans")

for yi, (_, val, _) in enumerate(dias):
    ax.text(val + 0.3, yi, f"{val:.1f}", va="center", fontsize=11,
            fontweight="bold", color=PRETO, family="DejaVu Sans")

ax.set_xlabel("Days of minimum wage (R$1,320/month, 2023)", color=CINZA, fontsize=10.5)
ax.set_xlim(0, 27)
for spine in ("top", "right"):
    ax.spines[spine].set_visible(False)

fig.text(0.09, 0.10,
         "Upper seats: Eras 19% pricier. Lower seats: Eras 4% cheaper. Standing floor: Eras 6% pricier.",
         color=PRETO, fontsize=11, family="DejaVu Sans")
fig.text(0.09, 0.065,
         "No consistent premium either way. Same city, same year, no stable price gap.",
         color=PRETO, fontsize=11, family="DejaVu Sans")

out = "visuais/eras_tour_mccartney.png"
fig.savefig(out, dpi=200)
print("salvo:", out)
for n, v, _ in dias:
    print(n.replace(chr(10), " "), f"{v:.2f} dias")
