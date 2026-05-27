import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# ── LOAD ──
bollywood = pd.read_csv("data/bollywood_clean.csv")
hollywood = pd.read_csv("data/hollywood_clean.csv")

bollywood['usd'] = (bollywood['gross_crore_inr'] * 0.12).round(1)
hollywood['usd'] = hollywood['gross_usd_million']
bollywood = bollywood.dropna(subset=['usd'])
hollywood = hollywood.dropna(subset=['usd'])

top10_b = bollywood.nlargest(10, 'usd').reset_index(drop=True)
top10_h = hollywood.nlargest(10, 'usd').reset_index(drop=True)
top10_b['short'] = top10_b['title'].str[:24]
top10_h['short'] = top10_h['title'].str[:24]
avg_b = bollywood['usd'].mean()
avg_h = hollywood['usd'].mean()

# ── PALETTE ──
BG    = '#06060e'
PANEL = '#0d0d1a'
GOLD  = '#e8b84b'
GOLD2 = '#ffd97d'
GOLD3 = '#c9922a'
BLUE  = '#3a8fb5'
BLUE2 = '#6dc8e8'
BLUE3 = '#1a5f7a'
WHITE = '#f0e8d8'
GREY  = '#4a4a60'
GREY2 = '#6a6a80'
LINE  = '#1a1a2e'
RED2  = '#e74c3c'

plt.rcParams.update({
    'figure.facecolor' : BG,
    'axes.facecolor'   : PANEL,
    'text.color'       : WHITE,
    'axes.labelcolor'  : GREY2,
    'xtick.color'      : GREY2,
    'ytick.color'      : WHITE,
    'axes.edgecolor'   : LINE,
    'font.family'      : 'DejaVu Sans',
    'axes.grid'        : False,
    'axes.spines.top'  : False,
    'axes.spines.right': False,
    'axes.spines.left' : False,
    'axes.spines.bottom': False,
})

fig = plt.figure(figsize=(22, 16))
fig.patch.set_facecolor(BG)

# ── FILM STRIP TOP ──
for i in range(70):
    x = i / 70
    c = GOLD if i % 2 == 0 else BG
    fig.add_artist(plt.Rectangle((x, 1 - 0.025), 1/70, 0.025,
        transform=fig.transFigure, color=c, zorder=20))

# ── FILM STRIP BOTTOM ──
for i in range(70):
    x = i / 70
    c = BLUE if i % 2 == 0 else BG
    fig.add_artist(plt.Rectangle((x, 0), 1/70, 0.020,
        transform=fig.transFigure, color=c, zorder=20))

# ── VERTICAL DIVIDER ──
fig.add_artist(plt.Rectangle((0.495, 0.08), 0.002, 0.82,
    transform=fig.transFigure, color=GREY, alpha=0.15, zorder=5))

# ── TITLE ──
title = fig.text(0.5, 0.936,
    'LIGHTS, CAMERA, DATA',
    ha='center', fontsize=36, fontweight='bold',
    color=GOLD, fontfamily='DejaVu Sans', zorder=10)
title.set_path_effects([
    pe.withStroke(linewidth=8, foreground='#3a2800'),
    pe.Normal()
])

fig.text(0.5, 0.908,
    'Two film industries. One century of cinema. What the numbers actually reveal.',
    ha='center', fontsize=12, color=GREY2, style='italic')

# ── GRADIENT DIVIDER LINE ──
ax_line = fig.add_axes([0.08, 0.897, 0.84, 0.0018])
ax_line.set_facecolor(BG)
ax_line.axis('off')
grad = np.linspace(0, 1, 200).reshape(1, -1)
ax_line.imshow(grad, aspect='auto',
    cmap=LinearSegmentedColormap.from_list('', [GOLD3, GOLD2, BLUE2, BLUE3]),
    extent=[0, 1, 0, 1])

# ── INDUSTRY LABELS ──
fig.text(0.25, 0.885, '🎬  BOLLYWOOD',
    ha='center', fontsize=11, color=GOLD, fontweight='bold', alpha=0.9)
fig.text(0.75, 0.885, 'HOLLYWOOD  🎬',
    ha='center', fontsize=11, color=BLUE2, fontweight='bold', alpha=0.9)

# ── LAYOUT ──
gs = gridspec.GridSpec(2, 2,
    left=0.13, right=0.97,
    top=0.868, bottom=0.07,
    hspace=0.52, wspace=0.42)

# ════════════════════════════════
# CHART 1 — BOLLYWOOD TOP 10
# ════════════════════════════════
ax1 = fig.add_subplot(gs[0, 0])
ax1.set_facecolor(PANEL)

vals   = top10_b['usd'].values
labels = top10_b['short'].values

for i, v in enumerate(vals):
    alpha = max(1.0 - i * 0.06, 0.45)
    ax1.barh(i, v, height=0.62,
             color=GOLD2 if i == 0 else GOLD,
             alpha=alpha, zorder=3)
    if i == 0:
        ax1.barh(i, v, height=0.75,
                 color=GOLD2, alpha=0.12, zorder=2)
    label_color = GOLD2 if i == 0 else '#c8a040'
    ax1.text(v + vals.max() * 0.015, i, f'${v:.0f}M',
             va='center', fontsize=8,
             color=label_color,
             fontweight='bold' if i == 0 else 'normal')

ax1.set_yticks(range(10))
ax1.set_yticklabels(
    ['★ ' + labels[0]] + [f'{i+1}. {l}' for i, l in enumerate(labels[1:], 1)],
    fontsize=8.5)
ax1.invert_yaxis()

for i in range(10):
    if i % 2 == 0:
        ax1.axhspan(i - 0.4, i + 0.4, color=WHITE, alpha=0.012)

ax1.set_title('BOLLYWOOD  ·  All-Time Top 10',
    color=GOLD, fontsize=10.5, fontweight='bold', pad=12, loc='left')
ax1.set_xlabel('USD Million', fontsize=8, color=GREY2, labelpad=6)
ax1.set_xlim(0, vals.max() * 1.22)
ax1.tick_params(axis='x', colors=GREY2, labelsize=7.5)
ax1.tick_params(axis='y', length=0)
ax1.axhline(9.5, color=GOLD3, alpha=0.3, linewidth=0.8)

# ════════════════════════════════
# CHART 2 — HOLLYWOOD TOP 10
# ════════════════════════════════
ax2 = fig.add_subplot(gs[0, 1])
ax2.set_facecolor(PANEL)

vals_h   = top10_h['usd'].values
labels_h = top10_h['short'].values

for i, v in enumerate(vals_h):
    alpha = max(1.0 - i * 0.06, 0.45)
    ax2.barh(i, v, height=0.62,
             color=BLUE2 if i == 0 else BLUE,
             alpha=alpha, zorder=3)
    if i == 0:
        ax2.barh(i, v, height=0.75,
                 color=BLUE2, alpha=0.12, zorder=2)
    label_color = BLUE2 if i == 0 else '#4a9ebb'
    ax2.text(v + vals_h.max() * 0.015, i, f'${v:.0f}M',
             va='center', fontsize=8,
             color=label_color,
             fontweight='bold' if i == 0 else 'normal')

ax2.set_yticks(range(10))
ax2.set_yticklabels(
    ['★ ' + labels_h[0]] + [f'{i+1}. {l}' for i, l in enumerate(labels_h[1:], 1)],
    fontsize=8.5)
ax2.invert_yaxis()

for i in range(10):
    if i % 2 == 0:
        ax2.axhspan(i - 0.4, i + 0.4, color=WHITE, alpha=0.012)

ax2.set_title('HOLLYWOOD  ·  All-Time Top 10',
    color=BLUE2, fontsize=10.5, fontweight='bold', pad=12, loc='left')
ax2.set_xlabel('USD Million', fontsize=8, color=GREY2, labelpad=6)
ax2.set_xlim(0, vals_h.max() * 1.22)
ax2.tick_params(axis='x', colors=GREY2, labelsize=7.5)
ax2.tick_params(axis='y', length=0)
ax2.axhline(9.5, color=BLUE3, alpha=0.3, linewidth=0.8)

# ════════════════════════════════
# CHART 3 — SCALE GAP
# ════════════════════════════════
ax3 = fig.add_subplot(gs[1, 0])
ax3.set_facecolor(PANEL)

categories = ['Bollywood\nAvg', 'Hollywood\nAvg', 'Bollywood\nPeak', 'Hollywood\nPeak']
values     = [avg_b, avg_h, bollywood['usd'].max(), hollywood['usd'].max()]
bar_colors = [GOLD, BLUE, GOLD2, BLUE2]
bar_alpha  = [0.8, 0.8, 1.0, 1.0]

for i, (v, c, a) in enumerate(zip(values, bar_colors, bar_alpha)):
    ax3.bar(i, v, width=0.6, color=c, alpha=a, zorder=3)
    if i in [0, 1]:
        ax3.bar(i, v, width=0.72, color=c, alpha=0.08, zorder=2)
    yoff = values[2] * 0.025
    ax3.text(i, v + yoff, f'${v:,.0f}M',
             ha='center', fontsize=9.5, color=c, fontweight='bold')

mid_y = (avg_b + avg_h) / 2
ax3.annotate('', xy=(1, avg_h * 0.92), xytext=(0, avg_b * 1.08),
    arrowprops=dict(arrowstyle='<->', color=RED2, lw=2.0))
ax3.text(0.5, mid_y * 1.15, f'{avg_h/avg_b:.0f}×',
    ha='center', va='center', color=RED2,
    fontsize=16, fontweight='bold',
    bbox=dict(boxstyle='round,pad=0.3', facecolor=BG,
              edgecolor=RED2, linewidth=1.2))

ax3.set_xticks(range(4))
ax3.set_xticklabels(categories, fontsize=9)
ax3.set_title('THE SCALE GAP  ·  Average & Peak Earnings',
    color=WHITE, fontsize=10.5, fontweight='bold', pad=12, loc='left')
ax3.set_ylabel('USD Million', fontsize=8, color=GREY2)
ax3.tick_params(axis='x', colors=WHITE, length=0)
ax3.tick_params(axis='y', colors=GREY2, labelsize=7.5)
ax3.set_ylim(0, hollywood['usd'].max() * 1.22)
ax3.spines['left'].set_visible(True)
ax3.spines['left'].set_color(LINE)

for yv in [500, 1000, 1500, 2000, 2500, 3000]:
    ax3.axhline(yv, color=GREY, alpha=0.12, linewidth=0.7, zorder=1)

# ════════════════════════════════
# CHART 4 — FACT CARDS
# ════════════════════════════════
ax4 = fig.add_subplot(gs[1, 1])
ax4.set_facecolor(PANEL)
ax4.set_xlim(0, 10)
ax4.set_ylim(0, 10)
ax4.axis('off')

facts = [
    (GOLD,  '★', 'Biggest Bollywood Hit',
             f"{top10_b.iloc[0]['title'][:22]}",
             f"${top10_b.iloc[0]['usd']:.0f}M worldwide"),
    (BLUE2, '★', 'Biggest Hollywood Hit',
             f"{top10_h.iloc[0]['title'][:22]}",
             f"${top10_h.iloc[0]['usd']:.0f}M worldwide"),
    (GOLD,  '◈', 'Bollywood Average',
             f"Top {len(bollywood)} films",
             f"${avg_b:.0f}M per film"),
    (BLUE2, '◈', 'Hollywood Average',
             f"Top {len(hollywood)} films",
             f"${avg_h:.0f}M per film"),
    (RED2,  '▲', 'The Gap',
             f"Hollywood earns {avg_h/avg_b:.0f}× more",
             f"on average per blockbuster"),
]

y_positions = [8.8, 7.0, 5.2, 3.4, 1.5]
for (color, icon, heading, line1, line2), y in zip(facts, y_positions):
    ax4.add_patch(mpatches.FancyBboxPatch(
        (0.15, y - 0.6), 9.7, 1.5,
        boxstyle="round,pad=0.15",
        facecolor=color, alpha=0.07,
        edgecolor=color, linewidth=0.8, zorder=2))
    ax4.add_patch(mpatches.FancyBboxPatch(
        (0.15, y - 0.6), 0.22, 1.5,
        boxstyle="round,pad=0.05",
        facecolor=color, alpha=0.6, zorder=3))
    ax4.text(0.68, y + 0.28, icon, fontsize=12,
             color=color, va='center', fontweight='bold')
    ax4.text(1.25, y + 0.28, heading, fontsize=9.5,
             color=color, fontweight='bold', va='center')
    ax4.text(1.25, y - 0.08, line1, fontsize=9,
             color=WHITE, va='center')
    ax4.text(1.25, y - 0.42, line2, fontsize=8.5,
             color=GREY2, va='center', style='italic')

ax4.set_title('KEY FACTS  ·  At a Glance',
    color=WHITE, fontsize=10.5, fontweight='bold', pad=12, loc='left')

# ── FOOTER ──
fig.text(0.5, 0.038,
    'Data scraped live from Wikipedia  ·  '
    'Python · BeautifulSoup · Pandas · Matplotlib  ·  WhenDataTalks',
    ha='center', fontsize=8, color=GREY, style='italic')

plt.savefig('dashboard.png', dpi=160,
            bbox_inches='tight', facecolor=BG)
print("✅ Dashboard saved!")
plt.show()