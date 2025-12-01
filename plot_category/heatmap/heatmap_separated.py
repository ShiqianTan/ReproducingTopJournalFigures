import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.cm as cm
import seaborn as sns
import numpy as np

# --- 1. Data Preparation ---
# Row labels (EG concentrations and Conditions)
eg_labels_major = ['100.0', '75.0', '56.2', '31.6']
condition_labels = ['Pp-T + Pp-E', 'Pp-TE'] * 4

# Column labels (TPA concentrations)
tpa_labels = ['31.6', '56.2', '75.0', '100.0']

# Mean values data (Transcribed from image)
data_means = np.array([
    [42, 59, 70, 84],  # EG 100, Cond 1
    [49, 64, 91, 132], # EG 100, Cond 2
    [36, 52, 62, 80],  # EG 75, Cond 1
    [43, 59, 75, 117], # EG 75, Cond 2
    [32, 49, 54, 74],  # EG 56.2, Cond 1
    [41, 53, 69, 99],  # EG 56.2, Cond 2
    [25, 42, 51, 65],  # EG 31.6, Cond 1
    [34, 47, 60, 84]   # EG 31.6, Cond 2
])

# Standard Deviation values data (Transcribed from image)
data_sds = np.array([
    [2, 3, 2, 0],
    [1, 0, 4, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 0],
    [0, 2, 2, 0],
    [0, 0, 1, 0],
    [1, 1, 1, 2],
    [1, 0, 0, 0]
])

rows, cols = data_means.shape

# --- 2. Custom Colormap Definition ---
# Define colors to match the visual gradient from Green -> Beige -> Orange -> Red
# We define nodes based on the colorbar ticks (20, 50, 80, 110, 140) mapped to 0-1 range.
# Vmin=20, Vmax=140 span=120.
# 20->0.0, 50->0.25, 80->0.5, 110->0.75, 140->1.0
colors_list = ["#2ca25f", "#a1d99b", "#fdedb3", "#fd8d3c", "#e31a1c"]
nodes = [0.0, 0.25, 0.5, 0.75, 1.0]
custom_cmap = mcolors.LinearSegmentedColormap.from_list("custom_green_red", list(zip(nodes, colors_list)))
vmin, vmax = 20, 140

# --- 3. Plotting Setup ---
# Set up figure size and layout to accommodate side labels and colorbar
fig = plt.figure(figsize=(10, 9))
# Define a grid area for the main heatmap
gs = fig.add_gridspec(1, 2, width_ratios=[1, 0.05], wspace=0.25)
ax = fig.add_subplot(gs[0])

# --- 4. Draw Heatmap ---
# We use seaborn heatmap for the base tiles
sns.heatmap(data_means, cmap=custom_cmap, vmin=vmin, vmax=vmax,
            annot=False, cbar=False, linewidths=3, linecolor='white', ax=ax, square=True)

# --- 5. Annotate Cells with Mean ± SD ---
font_size_cell = 14
for i in range(rows):
    for j in range(cols):
        text_val = f"{data_means[i, j]:.0f}±{data_sds[i, j]:.0f}"
        # Depending on background color density, switch text color to white for readability
        # A simple threshold check on the mean value works reasonably well here
        text_color = 'white' if data_means[i, j] > 110 or data_means[i, j] < 45 else 'black'
        ax.text(j + 0.5, i + 0.5, text_val,
                 ha='center', va='center', color=text_color, fontsize=font_size_cell)

# --- 6. Axis Formatting ---

# X-Axis (TPA mM)
ax.set_xticks(np.arange(cols) + 0.5)
ax.set_xticklabels(tpa_labels, fontsize=16)
ax.set_xlabel("TPA (mM)", fontsize=18, labelpad=10)
# Thicken the bottom spine (axis line)
ax.spines['bottom'].set_linewidth(2.5)
ax.spines['bottom'].set_color('black')

# Remove standard Y-axis ticks and labels
ax.set_yticks([])
for spine in ['left', 'right', 'top']:
    ax.spines[spine].set_visible(False)

# --- 7. Custom Layout & Labels (Replicating image style) ---

# A. Add 'f' title in top left corner
ax.text(-0.25, -0.05, 'f', transform=ax.transAxes, fontsize=28, fontweight='bold', va='top', ha='right')

# B. Add right-side condition labels for every row
for i in range(rows):
    ax.text(cols + 0.1, i + 0.5, condition_labels[i], ha='left', va='center', fontsize=16)

# C. Build the custom grouped Left Y-Axis (EG mM)
# 1. Draw the thick vertical axis line manually on the left
line_x_pos = -0.05
ax.plot([line_x_pos, line_x_pos], [0, rows], color='black', linewidth=2.5, 
        transform=ax.get_yaxis_transform(), clip_on=False)

# 2. Add grouped EG labels (centered vertically for each pair of rows)
group_centers = [1, 3, 5, 7] # y-coordinates for centers of row pairs
for pos, label in zip(group_centers, eg_labels_major):
    ax.text(line_x_pos - 0.1, pos, label, rotation=90, ha='center', va='center', fontsize=16)

# 3. Add the main Y-axis label "EG (mM)"
ax.text(line_x_pos - 0.25, rows / 2, 'EG (mM)', rotation=90, ha='center', va='center', fontsize=18)

# --- 8. Colorbar Customization ---
# Add a new axes for the colorbar to place it precisely
cbar_ax = fig.add_subplot(gs[1])
# Adjust position manually to sit lower, matching the image
pos1 = cbar_ax.get_position() # get the original position
pos2 = [pos1.x0 + 0.02, pos1.y0 + 0.2,  pos1.width * 0.6, pos1.height * 0.5]
cbar_ax.set_position(pos2) # set a new position

norm = mcolors.Normalize(vmin=vmin, vmax=vmax)
cb = fig.colorbar(cm.ScalarMappable(norm=norm, cmap=custom_cmap), cax=cbar_ax, orientation='vertical')

# Set specific ticks and labels for colorbar
cb_ticks = [20, 50, 80, 110, 140]
cb.set_ticks(cb_ticks)
cb.ax.set_yticklabels(cb_ticks, fontsize=14)
# Place label at the bottom of the colorbar
cb.set_label('Time (h)', rotation=0, labelpad=30, y=-0.05, ha='center', fontsize=16)

# Final layout adjustments to prevent clipping
plt.subplots_adjust(left=0.2, right=0.9, top=0.95, bottom=0.15)

# Save high quality image
plt.savefig('reproduced_heatmap.png', dpi=300, bbox_inches='tight')

# plt.show()
