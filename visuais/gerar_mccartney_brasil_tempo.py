"""Post — The McCartney Index, Brazil edition over time
Paul McCartney ticket price in Brazil across 5 tour stops (2011-2024),
indexed against Brazilian minimum wage and The Economist's own Big Mac
price for Brazil (public raw data, github.com/TheEconomist/big-mac-data).
Base 100 = 2011. All three grew at nearly the same rate over 13 years;
2017 is the one year the ticket badly outpaced both.
Dado: dados/paul_brasil_ao_longo_tempo.csv. Fontes por linha:
posts/mccartney-index/pesquisa_notas.md.
"""
import pandas as pd
from beatlenomics_style import make_canvas, VERMELHO, AZUL, LARANJA, PRETO, CINZA

df = pd.read_csv("dados/paul_brasil_ao_longo_tempo.csv").sort_values("ano")
base = df.iloc[0]
df["ticket_idx"] = df["preco_inteira_brl"] / base["preco_inteira_brl"] * 100
df["salario_idx"] = df["salario_minimo_mensal_brl"] / base["salario_minimo_mensal_brl"] * 100
df["bigmac_idx"] = df["bigmac_brl"] / base["bigmac_brl"] * 100

fig, ax = make_canvas(
    "The Beatle, the burger and the minimum wage",
    "Paul McCartney's Brazil ticket price vs. minimum wage vs. the Big Mac price, indexed (2011 = 100).",
    figsize=(11, 7.2))
ax.set_position([0.09, 0.17, 0.86, 0.52])

x = df["ano"]
ax.plot(x, df["ticket_idx"], color=VERMELHO, lw=2.8, marker="o", ms=8, zorder=4, label="Paul ticket")
ax.plot(x, df["salario_idx"], color=AZUL, lw=2.2, marker="o", ms=7, zorder=3, label="Minimum wage")
ax.plot(x, df["bigmac_idx"], color=LARANJA, lw=2.2, marker="o", ms=7, zorder=3, label="Big Mac (Brazil)")

ax.annotate("2017: ticket jumps\nahead of both",
            xy=(2017, df.loc[df["ano"] == 2017, "ticket_idx"].iloc[0]),
            xytext=(2013.6, 220), fontsize=10, color=PRETO, fontweight="bold",
            family="DejaVu Sans", arrowprops=dict(arrowstyle="-", color=CINZA, lw=1))

ax.set_xticks(x)
ax.set_ylabel("Index (2011 = 100)", color=CINZA, fontsize=10.5)
ax.legend(loc="upper left", frameon=False, fontsize=10.5)
for spine in ("top", "right"):
    ax.spines[spine].set_visible(False)

end = df.iloc[-1]
fig.text(0.09, 0.09,
         f"By 2024: ticket +{end['ticket_idx']-100:.0f}%, minimum wage +{end['salario_idx']-100:.0f}%, "
         f"Big Mac +{end['bigmac_idx']-100:.0f}%.",
         color=PRETO, fontsize=11, family="DejaVu Sans")
fig.text(0.09, 0.06,
         "Thirteen years, and the Beatle basically tracked the burger. 2017 was the one year it didn't.",
         color=PRETO, fontsize=11, family="DejaVu Sans")

out = "visuais/mccartney_brasil_tempo.png"
fig.savefig(out, dpi=200)
print("salvo:", out)
print(df[["ano", "ticket_idx", "salario_idx", "bigmac_idx"]].round(1).to_string(index=False))
