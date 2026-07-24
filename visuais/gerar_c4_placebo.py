"""Post C4 — placebo test (robustez, não vira post: fica no repo + 1o comentário).
Mesma lógica do C6 (placebo do C3), adaptada à janela mais curta de dados do C4
(~40 semanas, mai/2023-fev/2024, contra ~2 anos do Get Back). Duas checagens:

1) Placebo no tempo: desloca a data de tratamento para semanas sem lançamento
   (excluindo a janela em torno do evento real p/ não vazar o efeito verdadeiro
   no "nulo") e recalcula o DiD. Como a série é curta, sobram poucas datas
   candidatas (todas pré-teaser, jul-set/2023) e a janela pré/pós usada aqui é
   menor (8 pré / 6 pós) que a do post principal (12 pré / 8 pós) só para caber
   mais candidatos — é um n pequeno, reportado como tal, não escondido.
2) Placebo no grupo: cada banda-controle tratada como se fosse a "atingida" na
   data real, contra as outras duas.

Dado: dados/nowandthen_trends_raw.csv. Fontes: posts/c4-nowandthen-halo/referencias.md
"""
import numpy as np
import pandas as pd

df = pd.read_csv("dados/nowandthen_trends_raw.csv", parse_dates=["date"]).set_index("date").drop(columns=["isPartial"])
CTRL = ["The Rolling Stones", "Led Zeppelin", "Pink Floyd"]
df["gap"] = df["The Beatles"] - df[CTRL].mean(axis=1)
weeks = df.index
release = pd.Timestamp("2023-11-02")
real_week = weeks[weeks.get_indexer([release], method="ffill")[0]]

# --- 1) placebo no tempo ---------------------------------------------------
PRE, POST = 8, 6


def did_time(t, pre=PRE, post=POST):
    pre_win = df["gap"].reindex([t - pd.Timedelta(weeks=k) for k in range(1, pre + 1)])
    post_win = df["gap"].reindex([t + pd.Timedelta(weeks=k) for k in range(0, post)])
    return post_win.mean() - pre_win.mean()


lo = weeks.min() + pd.Timedelta(weeks=PRE)
hi = weeks.max() - pd.Timedelta(weeks=POST)
excl = (release - pd.Timedelta(weeks=6), release + pd.Timedelta(weeks=12))
placebo_dates = [w for w in weeks if lo <= w <= hi and not (excl[0] <= w <= excl[1])]

real_did = did_time(real_week)
placebo_dids = np.array([did_time(t) for t in placebo_dates])
z = (real_did - placebo_dids.mean()) / placebo_dids.std(ddof=1)
beat_real = int((placebo_dids >= real_did).sum())

# --- 2) placebo no grupo (data real, janela do post principal: 12 pré / 8 pós) ---
PRE2, POST2 = 12, 8


def did_space(target, others, t):
    tr, co = df[target], df[others].mean(axis=1)
    pre_t = tr.reindex([t - pd.Timedelta(weeks=k) for k in range(1, PRE2 + 1)]).mean()
    pre_c = co.reindex([t - pd.Timedelta(weeks=k) for k in range(1, PRE2 + 1)]).mean()
    post_t = tr.reindex([t + pd.Timedelta(weeks=k) for k in range(0, POST2)]).mean()
    post_c = co.reindex([t + pd.Timedelta(weeks=k) for k in range(0, POST2)]).mean()
    return (post_t - pre_t) - (post_c - pre_c)


space_results = {band: did_space(band, [c for c in CTRL if c != band], real_week) for band in CTRL}

print(f"placebo no tempo: n={len(placebo_dates)} datas falsas ({placebo_dates[0].date()} a {placebo_dates[-1].date()})")
print(f"  DiD real (janela {PRE}pré/{POST}pós) = {real_did:+.2f} pts")
print(f"  placebo média={placebo_dids.mean():+.2f} dp={placebo_dids.std(ddof=1):.2f} -> real está a {z:.1f} dp da média placebo")
print(f"  {beat_real}/{len(placebo_dates)} placebos >= efeito real")
print("placebo no grupo (banda-controle como tratada, data real, janela 12pré/8pós):")
for band, val in space_results.items():
    print(f"  {band}: {val:+.2f} pts")
