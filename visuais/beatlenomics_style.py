"""Identidade visual da série #beatlenomics.
Uso:
    from beatlenomics_style import make_canvas, PALETA
    fig, ax = make_canvas("Título", "subtítulo")
    ax.plot(...)   # plota no eixo do gráfico
    fig.savefig(...)
"""
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
import matplotlib.font_manager as fm

# --- Paleta ---
CREME      = "#DFE1E2"   # fundo (cinza claro, levemente frio)
VERMELHO   = "#D62828"   # Beatles / destaque
AZUL       = "#003049"   # Wings / texto escuro
LARANJA    = "#F77F00"   # solo
PRETO      = "#1A1A1A"
CINZA      = "#6E6E6E"
PALETA = {"Beatles": VERMELHO, "Wings": AZUL, "Solo": LARANJA,
          "Quarrymen": CINZA, "Cover": "#B7B7B5"}

ASSINATURA = "Tanise Bussmann"          # <- byline da série
HANDLE     = "in/tanisebussmann"        # <- LinkedIn
MONOGRAMA  = "TB"


def _vinil(ax, cx, cy, r, face=PRETO, label=VERMELHO, monograma=None, aspect=1.0):
    """Desenha um disco de vinil em coords da figura (0-1).
    aspect = razão largura/altura da figura, p/ o disco sair redondo."""
    def circ(rr, **kw):
        from matplotlib.patches import Ellipse
        ax.add_patch(Ellipse((cx, cy), 2*rr/aspect, 2*rr, **kw))
    circ(r, color=face, zorder=1)
    for rr in (r*0.92, r*0.80, r*0.68, r*0.56):           # sulcos
        circ(rr, fill=False, edgecolor="#444", lw=0.6, zorder=2)
    circ(r*0.40, color=label, zorder=3)                    # etiqueta
    if monograma:
        ax.text(cx, cy, monograma, ha="center", va="center", zorder=5,
                color="white", fontsize=r*260, fontweight="bold",
                family="DejaVu Serif")
    else:
        circ(r*0.05, color=CREME, zorder=4)                # furo


def _abbey_road(ax, y, x0=0.0, x1=1.0, n=13, h=0.018):
    """Faixa de pedestre estilo Abbey Road como divisória (coords da figura)."""
    w = (x1 - x0) / (2*n)
    for i in range(n):
        ax.add_patch(Rectangle((x0 + 2*i*w, y), w, h,
                               color=AZUL, alpha=0.85, zorder=2))


def make_canvas(title, subtitle="", figsize=(9, 9)):
    fig = plt.figure(figsize=figsize, facecolor=CREME)
    aspect = figsize[0] / figsize[1]

    # camada de fundo/decoração (figura inteira)
    bg = fig.add_axes([0, 0, 1, 1]); bg.set_axis_off()
    bg.set_xlim(0, 1); bg.set_ylim(0, 1)
    bg.add_patch(Rectangle((0, 0), 1, 1, color=CREME, zorder=0))

    # vinil decorativo, recortado no canto superior direito
    _vinil(bg, cx=1.03, cy=1.05, r=0.17, aspect=aspect)

    # kicker + título + subtítulo
    bg.text(0.06, 0.945, "#BEATLENOMICS", color=VERMELHO, fontsize=13,
            fontweight="bold", family="DejaVu Sans")
    bg.text(0.06, 0.905, title, color=PRETO, fontsize=21, fontweight="bold",
            family="DejaVu Serif", va="top")
    if subtitle:
        bg.text(0.06, 0.845, subtitle, color=CINZA, fontsize=12,
                family="DejaVu Sans", va="top")

    # rodapé: lockup do logo (mini-vinil TB) + handle
    _vinil(bg, cx=0.075, cy=0.022, r=0.028, monograma=MONOGRAMA, aspect=aspect)
    bg.text(0.115, 0.022, "#beatlenomics", color=VERMELHO, fontsize=11,
            fontweight="bold", family="DejaVu Sans", va="center")
    bg.text(0.94, 0.022, f"{ASSINATURA} · {HANDLE}", color=AZUL, fontsize=10,
            ha="right", va="center", family="DejaVu Sans")

    # eixo do gráfico (deixa margem p/ título em cima e rodapé embaixo)
    ax = fig.add_axes([0.12, 0.13, 0.80, 0.62])
    ax.set_facecolor(CREME)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(CINZA)
    ax.tick_params(colors=CINZA, length=0)
    return fig, ax
