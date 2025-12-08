import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Ellipse
import numpy as np
from matplotlib import rcParams

# Use serif font to match original
rcParams['font.family'] = 'serif'
rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif', 'serif']

# Set up the figure
fig, ax = plt.subplots(figsize=(10, 9))

# Draw shaded regions first (behind data points)
# Green region (aligned performance) - diagonal ellipse
green_ellipse = Ellipse((60, 60), width=75, height=38, angle=45, 
                         facecolor='#90EE90', alpha=0.35, edgecolor='none')
ax.add_patch(green_ellipse)

# Red region (overfitting) - ellipse in upper left area  
red_ellipse = Ellipse((42, 72), width=45, height=28, angle=30,
                       facecolor='#FFB6C1', alpha=0.35, edgecolor='none')
ax.add_patch(red_ellipse)

# Define all models with their data
# Stars - closed-access models
stars = [
    ('GPT-4-Turbo', 83, 88, 'black', (0, 3)),
    ('GPT-3.5-Turbo', 55, 68, '#1E90FF', None),
    ('GPT-4', 75, 80, '#FF8C00', (3, 1)),
    ('Gemini-Pro-1.5', 72, 72, '#CD853F', (2, -5)),
    ('Gemini-Flash-1.5', 43, 72, '#90EE90', None),
    ('Claude-3-O', 73, 75, '#FFD700', (2, 0)),
    ('Claude-3-S', 70, 65, '#FF6347', (2, -2)),
    ('Claude-Ins-1', 58, 48, '#FF69B4', (2, -3)),
    ('Mistral-L', 50, 68, '#FF1493', None),
    ('Mix-8x22B-Ins', 48, 70, '#6B8E23', None),
    ('Phind-34B', 45, 58, '#8B0000', None),
    ('MC-6.7B', 38, 68, '#DAA520', None),
]

# Diamonds
diamonds = [
    ('Command-R+', 52, 55, '#008B8B', None),
]

# Inverted triangles - LLama3 models
inverted_triangles = [
    ('Llama3-70B-Ins', 68, 75, '#DC143C', (2, 2)),
    ('LLama3-8b-Ins', 55, 57, '#FF69B4', None),
    ('LLama3-8b-Base', 38, 27, '#FFB6C1', None),
]

# Empty squares - DS-Base and SC2-Base
empty_squares = [
    ('DS-Base-33B', 52, 43, 'white', 'black', (3, 0)),
    ('DS-Base-6.7B', 35, 38, 'white', '#4169E1', (-13, 2)),
    ('DS-Base-1.3B', 28, 30, 'white', '#FF6B6B', (-13, 2)),
    ('SC2-Base-15B', 48, 37, 'white', '#FFB6C1', (3, -3)),
]

# Filled squares - DS-Ins and CodeQwen
filled_squares = [
    ('DS-33B', 55, 80, '#CD853F', (2, 1)),
    ('DS-6.7B', 47, 73, '#0000CD', (-10, 2)),
    ('DS-1.3B', 27, 60, '#DC143C', (-10, 2)),
    ('CodeQwen-Chat', 45, 78, '#00008B', (-12, 3)),
]

# Plot stars
for name, x, y, color, label_offset in stars:
    ax.scatter(x, y, marker='*', s=350, c=color, edgecolors='none', zorder=5)
    if label_offset:
        ax.annotate(name, (x, y), xytext=(x + label_offset[0], y + label_offset[1]), 
                    fontsize=8, color=color if color != 'black' else 'black')

# Plot diamonds
for name, x, y, color, label_offset in diamonds:
    ax.scatter(x, y, marker='D', s=180, c=color, edgecolors='none', zorder=5)

# Plot inverted triangles
for name, x, y, color, label_offset in inverted_triangles:
    ax.scatter(x, y, marker='v', s=220, c=color, edgecolors='none', zorder=5)
    if label_offset:
        ax.annotate(name, (x, y), xytext=(x + label_offset[0], y + label_offset[1]), 
                    fontsize=8, color=color)

# Plot empty squares
for name, x, y, facecolor, edgecolor, label_offset in empty_squares:
    ax.scatter(x, y, marker='s', s=180, c=facecolor, edgecolors=edgecolor, linewidths=1.5, zorder=5)
    if label_offset:
        ax.annotate(name, (x, y), xytext=(x + label_offset[0], y + label_offset[1]), 
                    fontsize=8, color=edgecolor if edgecolor != 'black' else 'gray')

# Plot filled squares
for name, x, y, color, label_offset in filled_squares:
    ax.scatter(x, y, marker='s', s=180, c=color, edgecolors='none', zorder=5)
    if label_offset:
        ax.annotate(name, (x, y), xytext=(x + label_offset[0], y + label_offset[1]), 
                    fontsize=8, color=color)

# Set axis labels with small caps style formatting
ax.set_xlabel(r'P$\mathsf{ASS}$@1 on LCB-Easy', fontsize=12)
ax.set_ylabel(r'P$\mathsf{ASS}$@1 on H$\mathsf{UMAN}$E$\mathsf{VAL}$+', fontsize=12)
ax.set_title(r'LCB-Easy vs H$\mathsf{UMAN}$E$\mathsf{VAL}$+', fontsize=14)

# Set axis limits and ticks
ax.set_xlim(15, 95)
ax.set_ylim(15, 95)
ax.set_xticks([20, 40, 60, 80])
ax.set_yticks([20, 40, 60, 80])

# Add box around plot area
for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_linewidth(0.5)

# Create legend elements in order matching the original (4 rows x 6 columns)
legend_elements = [
    # Row 1
    plt.Line2D([0], [0], marker='*', color='w', markerfacecolor='black', markersize=12, label='GPT-4-Turbo'),
    plt.Line2D([0], [0], marker='*', color='w', markerfacecolor='#90EE90', markersize=12, label='Gemini-Flash-1.5'),
    plt.Line2D([0], [0], marker='*', color='w', markerfacecolor='#FF1493', markersize=12, label='Mistral-L'),
    plt.Line2D([0], [0], marker='D', color='w', markerfacecolor='#008B8B', markersize=8, label='Command-R+'),
    plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='white', markeredgecolor='black', markersize=8, linewidth=0.5, label='DS-Base-33B'),
    plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='#CD853F', markersize=8, label='DS-Ins-33b'),
    # Row 2
    plt.Line2D([0], [0], marker='*', color='w', markerfacecolor='#1E90FF', markersize=12, label='GPT-3.5-Turbo'),
    plt.Line2D([0], [0], marker='*', color='w', markerfacecolor='#FFD700', markersize=12, label='Claude-3-O'),
    plt.Line2D([0], [0], marker='*', color='w', markerfacecolor='#6B8E23', markersize=12, label='Mix-8x22B-Ins'),
    plt.Line2D([0], [0], marker='v', color='w', markerfacecolor='#DC143C', markersize=10, label='LLama3-70b-Ins'),
    plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='white', markeredgecolor='#4169E1', markersize=8, label='DS-Base-6.7B'),
    plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='#0000CD', markersize=8, label='DS-Ins-6.7b'),
    # Row 3
    plt.Line2D([0], [0], marker='*', color='w', markerfacecolor='#FF8C00', markersize=12, label='GPT-4'),
    plt.Line2D([0], [0], marker='*', color='w', markerfacecolor='#FF6347', markersize=12, label='Claude-3-S'),
    plt.Line2D([0], [0], marker='*', color='w', markerfacecolor='#8B0000', markersize=12, label='Phind-34B'),
    plt.Line2D([0], [0], marker='v', color='w', markerfacecolor='#FF69B4', markersize=10, label='LLama3-8b-Ins'),
    plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='white', markeredgecolor='#FF6B6B', markersize=8, label='DS-Base-1.3B'),
    plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='#DC143C', markersize=8, label='DS-Ins-1.3b'),
    # Row 4
    plt.Line2D([0], [0], marker='*', color='w', markerfacecolor='#CD853F', markersize=12, label='Gemini-Pro-1.5'),
    plt.Line2D([0], [0], marker='*', color='w', markerfacecolor='#FF69B4', markersize=12, label='Claude-Ins-1'),
    plt.Line2D([0], [0], marker='D', color='w', markerfacecolor='#DAA520', markersize=8, label='MC-6.7B'),
    plt.Line2D([0], [0], marker='v', color='w', markerfacecolor='#FFB6C1', markersize=10, label='LLama3-8b-Base'),
    plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='white', markeredgecolor='#FFB6C1', markersize=8, label='SC2-Base-15B'),
    plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='#00008B', markersize=8, label='CodeQwen-Chat'),
]

# Create legend with 6 columns
ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.06),
          ncol=6, fontsize=8, frameon=False, columnspacing=0.5, handletextpad=0.2)

plt.tight_layout()
plt.subplots_adjust(bottom=0.18)

# Save the figure
plt.savefig('/mnt/user-data/outputs/lcb_humaneval_plot.png', dpi=150, bbox_inches='tight', 
            facecolor='white', edgecolor='none')
plt.savefig('/mnt/user-data/outputs/lcb_humaneval_plot.pdf', bbox_inches='tight',
            facecolor='white', edgecolor='none')
print("Figure saved successfully!")
