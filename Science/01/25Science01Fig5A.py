import matplotlib.pyplot as plt
import numpy as np

import matplotlib as mpl


mpl.rcParams.update({
    'font.size': 14,
    'axes.linewidth': 1.5,
    'xtick.major.width': 1.2,
    'ytick.major.width': 1.2,
    'xtick.direction': 'in',
    'ytick.direction': 'in',
    # 'xtick.top': True,
    # 'ytick.right': True
})

# Data (example values extracted from the figure)
cell_lines = [
    'KP-4','CRC1013','CTG-2383','LUR243','CRC054','LUR0264','CRC004','PAN020','CRA','CRC024','GPD24','CRC012',
    'CTG-0338','PAN0325','LXF0257','STO0597','PAN0417','STO0417','LXF0250','PAN0310','LXF2489','PAN0089','AGS',
    'CTG-2283','LUN1307','LUN1201','PAN0001'
]
mean_change = [
    200, 190, 170, 130, 110, 100, 90, 50, 40, 30, 15, 5,
    -10, -30, -35, -40, -45, -50, -55, -60, -65, -70, -80,
    -85, -90, -95, -95
]
error = [
    10, 20, 25, 20, 20, 15, 10, 15, 10, 5, 8, 7,
    8, 10, 8, 7, 10, 8, 10, 9, 8, 6, 5,
    5, 4, 3, 3
]
# Group mapping
group_labels = [
    'PDAC','CRC','NSCLC','CRC','NSCLC','CRC','CRC','GAC','PDAC','CRC','GAC','CRC',
    'NSCLC','GAC','PDAC','NSCLC','GAC','NSCLC','GAC','PDAC','GAC','NSCLC','GAC',
    'NSCLC','NSCLC','NSCLC','PDAC'
]
group_colors = {
    'PDAC': '#004c4c',
    'NSCLC': '#808080',
    'CRC': '#a6d8d4',
    'GAC': '#33a384'
}
colors = [group_colors[g] for g in group_labels]

# Plot
fig, ax = plt.subplots(figsize=(9, 6), dpi=300)

bars = ax.bar(range(len(cell_lines)), mean_change, yerr=error, capsize=3,
              color=colors, edgecolor='black', linewidth=0.5)

# Horizontal reference lines
thresholds = [0, -30, -50, -90]
for y in thresholds:
    ax.axhline(y, color='black', linestyle=':', linewidth=1)

# Y-axis
ax.set_ylabel('Mean tumor volume\n% change from baseline', fontsize=12)
ax.set_ylim(-100, 210)
ax.set_xticks(range(len(cell_lines)))
ax.set_xticklabels(cell_lines, rotation=90, fontsize=8)

# Remove top and right spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Add right side labels for mPD, mSD, mPR, mCR
label_positions = [100, -15, -40, -70]
labels = ['mPD', 'mSD', 'mPR', 'mCR']
for y, label in zip(label_positions, labels):
    ax.text(len(cell_lines) + 0.5, y, label, va='center', fontsize=10)

# Legend
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=color, edgecolor='black', label=grp) for grp, color in group_colors.items()]
ax.legend(handles=legend_elements, title='', loc='upper right', frameon=False)

plt.tight_layout()
plt.savefig("25Science01Fig5A.png", dpi=300)
plt.savefig("25Science01Fig5A.pdf", dpi=300)
plt.show()
