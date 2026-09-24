"""Post C9 - The effect I could not detect (poder / MDE por simulacao)
Usa o MESMO desenho e dado do C5 (5 cidades tratadas x 5 controle, Google
Trends, leva Brasil da turne Got Back, nov-dez/2023), so que a pergunta muda:
nao "qual foi o efeito", mas "esse desenho teria poder pra detectar QUALQUER
efeito, dado o ruido semana-a-semana observado no dado real?"

Metodo: bootstrap de residuos. Estima o desvio-padrao semanal (ruido) de cada
unidade no periodo pre-turne (sem efeito conhecido), depois simula milhares de
paineis sinteticos com esse mesmo ruido, injetando um efeito artificial DELTA
(constante, em pontos de indice) nas unidades tratadas na janela pos. Repete
para varios tamanhos de DELTA e mede a taxa de deteccao (DiD estimado > limiar
critico do nulo, one-sided) -- isso E a curva de poder.
Dado: dados/paul_geolift_trends_raw.csv (mesmo do C5/C6).
"""
import numpy as np
import pandas as pd
from beatlenomics_style import make_canvas, VERMELHO, AZUL, PRETO, CINZA

RNG = np.random.default_rng(42)

# --- 1. Reconstroi o painel do C5 (mesmo filtro, mesmo indice) ---
df = pd.read_csv("dados/paul_geolift_trends_raw.csv", parse_dates=["date", "event_date"])
br = df[(df.country == "BR") & (df.geo != "BR-SC")].copy()
br["idx"] = br.groupby("geo")["interest"].transform(lambda s: 100 * s / s.mean())
piv = br.pivot_table(index="date", columns=["is_treated", "geo"], values="idx")
w = piv.loc["2023-10-01":"2024-02-25"]

pre = w.loc[:"2023-11-29"]
post_real = w.loc["2023-11-30":"2023-12-16"]
n_pre, n_post = len(pre), len(post_real)  # 9, 2
treated_cols = [c for c in w.columns if c[0]]
control_cols = [c for c in w.columns if not c[0]]
n_treat, n_ctrl = len(treated_cols), len(control_cols)

# --- 2. Ruido semanal: residuo de cada unidade em torno da propria media PRE ---
pre_demeaned = pre - pre.mean()
sigma_unit = float(np.nanstd(pre_demeaned.to_numpy(), ddof=1))  # pooled, 10 unidades x 9 semanas
print(f"n_pre={n_pre} n_post={n_post} n_treat={n_treat} n_ctrl={n_ctrl} sigma_unit={sigma_unit:.1f}")

# --- 2b. ONDE o ruido pooled vem: sigma por unidade (achado da revisao 31/08/2026) ---
# Brasilia (menor volume absoluto de busca, media~3.9 no Trends bruto) domina o
# sigma pooled porque idx = 100*interest/media_da_regiao -- denominador pequeno
# infla qualquer pico absoluto pequeno em oscilacao de indice gigante.
sigma_por_unidade = pre_demeaned.std(ddof=1).sort_values(ascending=False)
print("sigma por unidade (pre-periodo, ordenado):")
print(sigma_por_unidade.round(1).to_string())

# --- 3. DiD real observado (para referencia, dado contaminado -- ver C5/C6) ---
did_real = (post_real[treated_cols].mean().mean() - pre[treated_cols].mean().mean()) - \
           (post_real[control_cols].mean().mean() - pre[control_cols].mean().mean())
print(f"DiD real observado (contaminado, ver C5): {did_real:.1f} pontos de indice")


def simula_did(delta, n_sims=4000):
    """Simula n_sims paineis com ruido ~ N(0, sigma_unit), injeta `delta` nas
    unidades tratadas na janela pos, retorna array de estimativas DiD."""
    treat_pre = RNG.normal(0, sigma_unit, size=(n_sims, n_treat, n_pre)).mean(axis=(1, 2))
    treat_post = RNG.normal(delta, sigma_unit, size=(n_sims, n_treat, n_post)).mean(axis=(1, 2))
    ctrl_pre = RNG.normal(0, sigma_unit, size=(n_sims, n_ctrl, n_pre)).mean(axis=(1, 2))
    ctrl_post = RNG.normal(0, sigma_unit, size=(n_sims, n_ctrl, n_post)).mean(axis=(1, 2))
    return (treat_post - treat_pre) - (ctrl_post - ctrl_pre)


# --- 4. Limiar critico sob H0 (delta=0), one-sided 5% ---
null_dist = simula_did(0, n_sims=20000)
threshold = np.quantile(null_dist, 0.95)
print(f"limiar critico (H0, alpha=0.05 one-sided): {threshold:.1f} pontos de indice")

# --- 5. Curva de poder ---
deltas = np.arange(0, 421, 10)
power = np.array([(simula_did(d) > threshold).mean() for d in deltas])

mde_idx = np.argmax(power >= 0.80)
mde_80 = deltas[mde_idx] if power[mde_idx] >= 0.80 else None
print(f"MDE a 80% de poder: {mde_80} pontos de indice" if mde_80 is not None
      else "MDE a 80% de poder: fora da faixa simulada")

pd.DataFrame({"delta": deltas, "power": power}).to_csv(
    "dados/paul_c9_power_curve.csv", index=False)

# --- 5b. Robustez: sigma HETEROGENEO por unidade (em vez de pooled) ---
# Testa se a MDE sobrevive quando cada unidade usa seu proprio ruido, em vez do
# sigma medio pooled -- ou seja, se o achado do 2b muda a conclusao ou so a
# explicacao do porque do ruido ser grande.
sigma_arr_treat = sigma_por_unidade.reindex(treated_cols).to_numpy()
sigma_arr_ctrl = sigma_por_unidade.reindex(control_cols).to_numpy()


def simula_did_heterog(delta, n_sims=4000):
    treat_pre = (RNG.normal(0, 1, size=(n_sims, n_treat, n_pre)) * sigma_arr_treat[None, :, None]).mean(axis=(1, 2))
    treat_post = (delta + RNG.normal(0, 1, size=(n_sims, n_treat, n_post)) * sigma_arr_treat[None, :, None]).mean(axis=(1, 2))
    ctrl_pre = (RNG.normal(0, 1, size=(n_sims, n_ctrl, n_pre)) * sigma_arr_ctrl[None, :, None]).mean(axis=(1, 2))
    ctrl_post = (RNG.normal(0, 1, size=(n_sims, n_ctrl, n_post)) * sigma_arr_ctrl[None, :, None]).mean(axis=(1, 2))
    return (treat_post - treat_pre) - (ctrl_post - ctrl_pre)


null_heterog = simula_did_heterog(0, n_sims=20000)
threshold_heterog = np.quantile(null_heterog, 0.95)
power_heterog = np.array([(simula_did_heterog(d) > threshold_heterog).mean() for d in deltas])
mde_heterog_idx = np.argmax(power_heterog >= 0.80)
mde_heterog = deltas[mde_heterog_idx] if power_heterog[mde_heterog_idx] >= 0.80 else None
print(f"[robustez, sigma heterogeneo] limiar critico: {threshold_heterog:.1f} | "
      f"poder em delta=350: {power_heterog[deltas == 350][0]:.3f} | "
      f"MDE a 80%: {mde_heterog}")

# --- 6. Grafico ---
fig, ax = make_canvas(
    "The effect I could not detect",
    "Power curve for the Brazil geo-lift design (C5): detection rate by injected effect size",
)
ax.plot(deltas, power * 100, color=VERMELHO, lw=2.6)
ax.axhline(80, color=CINZA, lw=1, ls="--", zorder=1)
ax.text(deltas[-1], 81, "80% power", color=CINZA, fontsize=9, ha="right", va="bottom")
if mde_80 is not None:
    ax.axvline(mde_80, color=AZUL, lw=1, ls=":", zorder=1)
    ax.annotate(f"MDE = {mde_80} idx pts", xy=(mde_80, 80), xytext=(mde_80 + 15, 55),
                color=AZUL, fontsize=10, fontweight="bold", family="DejaVu Sans",
                arrowprops=dict(arrowstyle="-", color=AZUL, lw=1))
ax.axvline(did_real, color=PRETO, lw=1.4, ls="-", zorder=1)
ax.annotate("C5 estimate\n(contaminated)", xy=(did_real, 15), xytext=(did_real + 15, 15),
            color=PRETO, fontsize=9, va="center", family="DejaVu Sans")

ax.set_xlabel("Injected effect size (index points, weekly search interest)", color=CINZA, fontsize=10)
ax.set_ylabel("Detection rate (%)", color=CINZA, fontsize=10)
ax.set_ylim(0, 100)
ax.set_xlim(0, deltas[-1])

out = "visuais/c9_power_curve.png"
fig.savefig(out, dpi=200, facecolor=fig.get_facecolor())
print("salvo:", out)
