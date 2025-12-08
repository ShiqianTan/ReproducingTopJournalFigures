import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
from matplotlib.patches import Rectangle

# Font setup for serif style
rcParams['font.family'] = 'serif'
rcParams['font.serif'] = ['DejaVu Serif', 'Times New Roman', 'Computer Modern Roman']
rcParams['mathtext.fontset'] = 'cm'

# Set up the figure
fig, ax = plt.subplots(figsize=(10, 6.5))

# Data for the plot
months = ['May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb']
x = np.arange(len(months))

# Approximate data extracted from the figure (refined)
ds_ins_33b = [28, 37, 25, 27, 32, 27, 35, 35, 30, 25]
gemini_flash = [13, 25, 25, 26, 38, 26, 30, 38, 35, 30]
gpt4 = [25, 40, 30, 30, 40, 40, 48, 47, 40, 35]
gpt4_o = [40, 52, 40, 35, 50, 48, 42, 35, 40, 47]

# Define three distinct but similar colors (red -> yellow -> green transition)
color1 = '#ffcccc'  # Light red/pink
color2 = '#ffffcc'  # Light yellow
color3 = '#ccffcc'  # Light green

# Create three colored background regions
# Region 1: May-Jul (indices 0-2, so x from -0.5 to 2.5)
rect1 = Rectangle((-0.5, 0), 3.5, 100, facecolor=color1, zorder=0)
ax.add_patch(rect1)

# Region 2: Aug-Oct (indices 3-5, so x from 2.5 to 5.5)
rect2 = Rectangle((3.0, 0), 3.5, 100, facecolor=color2, zorder=0)
ax.add_patch(rect2)

# Region 3: Nov-Feb (indices 6-9, so x from 5.5 to 9.5)
rect3 = Rectangle((6.5, 0), 3, 100, facecolor=color3, zorder=0)
ax.add_patch(rect3)

# Plot the lines with markers
ax.plot(x, ds_ins_33b, 'o-', color='#1f77b4', label='DS-Ins-33B', linewidth=1.8, markersize=6, zorder=3)
ax.plot(x, gemini_flash, 'o-', color='#2ca02c', label='Gemini-Flash-1.5', linewidth=1.8, markersize=6, zorder=3)
ax.plot(x, gpt4, 'o-', color='#ff7f0e', label='GPT4', linewidth=1.8, markersize=6, zorder=3)
ax.plot(x, gpt4_o, 'o-', color='#c44e52', label='GPT4-O', linewidth=1.8, markersize=6, zorder=3)

# Configure axes
ax.set_xlim(-0.5, len(months) - 0.5)
ax.set_ylim(0, 100)
ax.set_xticks(x)
ax.set_xticklabels(months, fontsize=11)
ax.set_yticks([0, 20, 40, 60, 80, 100])
ax.tick_params(axis='y', labelsize=11)

# Add grid lines (both horizontal and vertical)
ax.yaxis.grid(True, linestyle='-', alpha=0.5, color='gray', zorder=1)
ax.xaxis.grid(True, linestyle='-', alpha=0.5, color='gray', zorder=1)

# Title
ax.set_title('Code Generation Live Evaluation', fontsize=14, fontweight='bold', pad=10)

# Y-axis label: PASS@1 with small caps simulation using Unicode
ax.set_ylabel('Pᴀss@1', fontsize=13)

# X-axis label: ATCODER with small caps simulation using Unicode
ax.set_xlabel('AᴛCᴏᴅᴇʀ Problem Release Month', fontsize=13)

# Legend - positioned in upper area, 2 columns
legend = ax.legend(loc='upper center', ncol=2, frameon=True, fancybox=False, 
                   edgecolor='black', fontsize=10, bbox_to_anchor=(0.32, 0.98),
                   handlelength=2, columnspacing=1.5)
legend.get_frame().set_linewidth(0.8)

# Keep all spines visible
for spine in ax.spines.values():
    spine.set_linewidth(0.8)

# Add figure caption below with small caps
fig.text(0.5, 0.02, 'Figure 11: Performance on problems released over different months for AᴛCᴏᴅᴇʀ',
         ha='center', fontsize=12, style='italic')

plt.tight_layout()
plt.subplots_adjust(bottom=0.13)

# Save the figure
plt.savefig('/mnt/user-data/outputs/code_generation_figure.png', dpi=150, bbox_inches='tight', 
            facecolor='white', edgecolor='none')
plt.close()

print("Figure saved to /mnt/user-data/outputs/code_generation_figure.png")
