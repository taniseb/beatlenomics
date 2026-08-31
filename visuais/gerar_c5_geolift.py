"""Post C5 - Geo-lift dos shows do Paul (o desenho que quebrou)
Tentativa de geo-lift/DiD geografico: cidades com show da turne Got Back
(Brasilia, Belo Horizonte, Sao Paulo, Curitiba, Rio de Janeiro) vs. cidades
sem show (Salvador, Recife, Fortaleza, Porto Alegre, Manaus), leva Brasil
nov-dez/2023. Cada regiao normalizada pela sua propria media na janela
completa (18 meses) -- indice 100 = media da regiao, nao comparavel em nivel
absoluto entre regioes, so a FORMA da curva importa aqui.
O achado real: as duas curvas (tratado e controle) sobem JUNTAS na semana da
turne. Isso e o oposto do que um geo-lift limpo precisa (controle plano
enquanto tratado sobe) -- e a razao do post: cobertura de imprensa nacional
contamina o "controle" quando o evento e grande o bastante.
Dado: dados/paul_geolift_trends_raw.csv. Fontes: posts/c5-geolift-shows/referencias.md
"""
import pandas as pd, numpy as np
import matplotlib.dates as mdates
from beatlenomics_style import make_canvas, VERMELHO, AZUL, PRETO, CINZA

CINZA_LINHA = "#B7B7B5"

df = pd.read_csv("dados/paul_geolift_trends_raw.csv", parse_dates=["date", "event_date"])
# BR-SC (Florianopolis) e is_treated=True mas com event_date de 19/out/2024,
# a leva SEGUINTE da turne -- fora da janela nov-dez/2023 analisada aqui.
# Sem excluir, ela dilui a media do grupo tratado com uma cidade sem show na janela.
br = df[(df.country == "BR") & (df.geo != "BR-SC")].copy()
br["idx"] = br.groupby("geo")["interest"].transform(lambda s: 100 * s / s.mean())
piv = br.pivot_table(index="date", columns="is_treated", values="idx", aggfunc="mean")
piv.columns = ["Control", "Treated"]
piv = piv.loc["2023-10-01":"2024-02-25"]

fig, ax = make_canvas(
    "The control group was never really a control",
    "Paul McCartney search interest: Brazilian cities with a show vs. without. Geo-lift.",
    figsize=(11, 8))
ax.set_position([0.09, 0.15, 0.86, 0.52])

x = piv.index
ax.plot(x, piv["Control"], color=CINZA_LINHA, lw=2.2, ls=(0, (4, 3)), zorder=3)
ax.plot(x, piv["Treated"], color=VERMELHO, lw=2.6, zorder=4)

tour_start, tour_end = pd.Timestamp("2023-11-30"), pd.Timestamp("2023-12-16")
ax.axvspan(tour_start, tour_end, color=AZUL, alpha=0.08, zorder=1)
ax.annotate("Brazil leg\n(5 host cities,\nNov 30-Dec 16)", xy=(tour_start, 900),
            xytext=(x[6], 1060), color=AZUL, fontsize=10, fontweight="bold",
            va="top", ha="left", family="DejaVu Sans",
            arrowprops=dict(arrowstyle="-", color=AZUL, lw=1))

ax.text(x[1], piv["Treated"].iloc[1] + 90, "Host cities (observed)",
        color=VERMELHO, fontsize=11, fontweight="bold", family="DejaVu Sans")
ax.text(x[1], piv["Control"].iloc[1] - 55, "No-show cities (control)",
        color="#7A7A7A", fontsize=10, family="DejaVu Sans")

ax.set_ylim(0, 1150)
ax.set_ylabel("Search interest (index, own 18-month avg = 100)", color=CINZA, fontsize=10.5)
ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=3))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
for label in ax.get_xticklabels():
    label.set_rotation(45)
    label.set_ha("right")

peak_treat = piv["Treated"].max()
peak_ctrl = piv["Control"].max()
fig.text(0.09, 0.085,
         f"Host cities peak at {peak_treat/100:.1f}x their own average during the tour.",
         color=PRETO, fontsize=11, family="DejaVu Sans")
fig.text(0.09, 0.055,
         "No-show cities peak nearly as high the week it ends.",
         color=PRETO, fontsize=11, family="DejaVu Sans")

out = "visuais/c5_geolift.png"
fig.savefig(out, dpi=200)
print("salvo:", out, f"| peak treated={peak_treat:.0f} | peak control={peak_ctrl:.0f}")
