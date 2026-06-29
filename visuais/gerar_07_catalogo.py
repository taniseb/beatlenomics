"""Post 7 — Who owns the Beatles? O catálogo como classe de ativos.
US$47,5M (Michael Jackson, 1985) -> US$1,5B (Sony, 2016) = 31x em 31 anos,
CAGR nominal de 11,8%, praticamente em linha com o S&P 500 (11,1%).
Compara o valuation do catálogo com o que os mesmos US$47,5M teriam virado
investidos no S&P 500 no mesmo período.
Fontes: ver posts/07-quem-e-dono/referencias.md
"""
import numpy as np
from beatlenomics_style import make_canvas, VERMELHO, AZUL, LARANJA, PRETO, CINZA

# --- Catálogo: valuations implícitos nas transações (US$ milhões, nominal) ---
cat_anos  = [1985, 1995, 2016]
cat_valor = [47.5, 187.5, 1500.0]   # 1995: Sony/ATV, MJ mantém 50% de um todo ~US$375M
cat_label = ["Michael Jackson\nbuys ATV Music\n$47.5M",
             "Sony/ATV\nformed",
             "Sony buys the\nrest  ·  $1.5B"]

# --- S&P 500: os mesmos US$47,5M compostos a 11,1% nominal/ano (1985-2016) ---
sp_anos  = np.arange(1985, 2017)
sp_valor = 47.5 * (1.111) ** (sp_anos - 1985)

fig, ax = make_canvas(
    "A songbook that tracked the S&P 500",
    "The Beatles catalogue grew 31x in 31 years (11.8% a year), in line with the US stock market",
    figsize=(9, 9))

# S&P como curva suave de fundo (a referência de mercado)
ax.plot(sp_anos, sp_valor, color=AZUL, lw=2.2, zorder=2,
        label="$47.5M in the S&P 500 (11.1%/yr)")
ax.scatter([2016], [sp_valor[-1]], color=AZUL, s=40, zorder=3)
ax.annotate(f"${sp_valor[-1]/1000:.2f}B", (2016, sp_valor[-1]),
            textcoords="offset points", xytext=(8, -14),
            color=AZUL, fontsize=10, fontweight="bold")

# Catálogo como pontos de transação conectados (lumpy, do mundo real)
ax.plot(cat_anos, cat_valor, color=VERMELHO, lw=2.6, zorder=4,
        marker="o", markersize=9, label="Beatles catalogue (transaction value)")

# Rótulos das transações
offs = [(14, -16), (6, -34), (-2, 18)]
has  = ["left", "left", "right"]
for (x, y, lab, off, ha) in zip(cat_anos, cat_valor, cat_label, offs, has):
    ax.annotate(lab, (x, y), textcoords="offset points", xytext=off,
                ha=ha, va="center", fontsize=9.5, color=PRETO,
                fontweight="bold", linespacing=1.15)

# Escala log: a única forma honesta de mostrar 47,5M -> 1,5B
ax.set_yscale("log")
ax.set_ylim(30, 3000)
ax.set_yticks([50, 100, 200, 500, 1000, 2000])
ax.set_yticklabels(["$50M", "$100M", "$200M", "$500M", "$1B", "$2B"])
ax.set_xlim(1983, 2019)
ax.set_xticks([1985, 1995, 2005, 2016])
ax.tick_params(labelsize=11)
ax.set_xlabel("", fontsize=11)
ax.grid(axis="y", color=CINZA, alpha=0.18, lw=0.7)

ax.legend(loc="upper left", frameon=False, fontsize=11)

out = "visuais/07_catalogo.png"
fig.savefig(out, dpi=200)
cagr = (1500 / 47.5) ** (1/31) - 1
print("salvo:", out, "| 31x | CAGR nominal:", round(100*cagr, 1), "%",
      "| S&P 2016:", round(sp_valor[-1]), "M")
