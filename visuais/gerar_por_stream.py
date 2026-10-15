"""Post quinta — "How many plays pay a minimum wage?" (beatles-por-stream, técnico leve)
Streams necessários pra pagar 1 salário mínimo mensal, Brasil 2026 vs EUA (federal),
artista independente (fica com ~100% do payout) vs artista com contrato de gravadora
(~15% do payout, faixa reportada 10-20%). Barra = ponto médio US$0,004/stream;
traço = intervalo US$0,003-0,005 (estimativa de mercado, NÃO tarifa oficial: o
Spotify diz que não paga por stream, paga por streamshare).
Não repete o post 11 (volume de streams). Aqui é preço unitário.
Fontes em posts/beatles-por-stream/referencias.md.
"""
import pandas as pd
from beatlenomics_style import make_canvas, VERMELHO, AZUL, CINZA, PRETO

PAYOUT = (0.003, 0.004, 0.005)          # US$/stream, baixo/meio/alto
SHARE_SIGNED = 0.15                     # fatia do artista com gravadora (10-20%)
FX_BRL = 5.005                          # frankfurter, 2026-10-09
SM = {"Brazil": 1621 / FX_BRL,          # Decreto 12.797/2025, R$1.621
      "US (federal)": 1256.67}          # US$7,25/h x 40h x 52/12

rows = []
for pais, sm in SM.items():
    for quem, share in (("independent artist", 1.0), ("artist on a label deal", SHARE_SIGNED)):
        lo, mid, hi = (sm / (p * share) for p in PAYOUT[::-1])
        rows.append(dict(pais=pais, quem=quem, sm_usd=round(sm, 2), share=share,
                         streams_min=round(lo), streams_mid=round(mid), streams_max=round(hi)))
df = pd.DataFrame(rows)
df.to_csv("dados/por_stream.csv", index=False)

fig, ax = make_canvas(
    "How many plays pay a minimum wage?",
    "Streams needed to earn one month of minimum wage, 2026. Bar = US$0.004 per stream,\nline = US$0.003 to 0.005.",
    figsize=(10, 9))

ax.set_position([0.30, 0.13, 0.62, 0.62])
fmt = lambda n: f"{n/1e6:.1f}M" if n >= 1e6 else f"{n/1e3:,.0f}k"
labels = [f"{r.pais}\n{r.quem}" for r in df.itertuples()]
ys = list(range(len(df)))[::-1]
cores = [CINZA if r.quem.startswith("indep") else VERMELHO for r in df.itertuples()]
ax.barh(ys, df["streams_mid"] / 1e6, color=cores, height=0.55)
for y, r in zip(ys, df.itertuples()):
    ax.plot([r.streams_min / 1e6, r.streams_max / 1e6], [y, y], color=PRETO, lw=1.6)
    ax.text(r.streams_max / 1e6 + 0.06, y, fmt(r.streams_mid),
            va="center", fontsize=13, fontweight="bold", color=PRETO, family="DejaVu Sans")
ax.set_yticks(ys)
ax.set_yticklabels(labels, fontsize=10.5, color=CINZA)
ax.set_xlabel("Millions of streams", color=CINZA, fontsize=10.5)
ax.set_xlim(0, 3.4)

out = "visuais/por_stream.png"
fig.savefig(out, dpi=200)
print("salvo:", out)
print(df.to_string(index=False))
