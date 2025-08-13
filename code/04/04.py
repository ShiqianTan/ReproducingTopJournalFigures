import matplotlib.pyplot as plt
import numpy as np

# Set up the figure with publication-ready styling
plt.rcParams.update({
    'font.size': 12,
    'font.family': 'Arial',
    'axes.linewidth': 1.2,
    'axes.labelsize': 14,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'legend.fontsize': 11,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight'
})

# Set random seed for reproducible data
np.random.seed(42)

# Generate synthetic data points
x_labels = ['Test', 'Hyp. 1*', 'Hyp. 2*']
x_positions = [0, 1, 2]

# Generate similar but new data for each series
large_ring = [0.18 + np.random.normal(0, 0.01), 0.21 + np.random.normal(0, 0.01), 0.45 + np.random.normal(0, 0.02)]
medium_ring = [0.17 + np.random.normal(0, 0.01), 0.20 + np.random.normal(0, 0.01), 0.33 + np.random.normal(0, 0.01)]
small_ring = [0.08 + np.random.normal(0, 0.005), 0.11 + np.random.normal(0, 0.005), 0.16 + np.random.normal(0, 0.01)]
large_d10 = [0.19 + np.random.normal(0, 0.01), 0.25 + np.random.normal(0, 0.01), 0.41 + np.random.normal(0, 0.02)]
medium_d10 = [0.17 + np.random.normal(0, 0.01), 0.23 + np.random.normal(0, 0.01), 0.34 + np.random.normal(0, 0.01)]
small_d10 = [0.09 + np.random.normal(0, 0.005), 0.13 + np.random.normal(0, 0.005), 0.19 + np.random.normal(0, 0.01)]
very_small_d10 = [0.015 + np.random.normal(0, 0.003), 0.012 + np.random.normal(0, 0.003), 0.018 + np.random.normal(0, 0.003)]

# Create the figure and axis
fig, ax = plt.subplots(1, 1, figsize=(8, 6))

import matplotlib.colors as mcolors

# Define colors for each series (markers)
marker_colors = {
    'large_ring': 'black',
    'medium_ring': 'darkblue', 
    'small_ring': 'brown',
    'large_d10': 'lightcoral',
    'medium_d10': 'red',
    'small_d10': 'orange',
    'very_small_d10': 'tan'
}

# Define lighter line colors (same hue but with transparency)
line_colors = {
    'large_ring': mcolors.to_rgba('black', alpha=0.5),
    'medium_ring': mcolors.to_rgba('darkblue', alpha=0.5), 
    'small_ring': mcolors.to_rgba('brown', alpha=0.5),
    'large_d10': mcolors.to_rgba('lightcoral', alpha=0.6),
    'medium_d10': mcolors.to_rgba('red', alpha=0.5),
    'small_d10': mcolors.to_rgba('orange', alpha=0.6),
    'very_small_d10': mcolors.to_rgba('tan', alpha=0.6)
}

# Plot lines with different markers and lighter line colors
ax.plot(x_positions, large_ring, '-s', markersize=8, linewidth=2, 
        color=line_colors['large_ring'], markerfacecolor=marker_colors['large_ring'], 
        markeredgecolor=marker_colors['large_ring'], label='Large ring')
ax.plot(x_positions, medium_ring, '-o', markersize=8, linewidth=2, 
        color=line_colors['medium_ring'], markerfacecolor=marker_colors['medium_ring'], 
        markeredgecolor=marker_colors['medium_ring'], label='Medium ring')
ax.plot(x_positions, small_ring, '-^', markersize=8, linewidth=2, 
        color=line_colors['small_ring'], markerfacecolor=marker_colors['small_ring'], 
        markeredgecolor=marker_colors['small_ring'], label='Small ring')
ax.plot(x_positions, large_d10, '-s', markersize=8, linewidth=2, 
        color=line_colors['large_d10'], markerfacecolor=marker_colors['large_d10'], 
        markeredgecolor=marker_colors['large_d10'], label='Large D₁₀')
ax.plot(x_positions, medium_d10, '-o', markersize=8, linewidth=2, 
        color=line_colors['medium_d10'], markerfacecolor=marker_colors['medium_d10'], 
        markeredgecolor=marker_colors['medium_d10'], label='Medium D₁₀')
ax.plot(x_positions, small_d10, '-^', markersize=8, linewidth=2, 
        color=line_colors['small_d10'], markerfacecolor=marker_colors['small_d10'], 
        markeredgecolor=marker_colors['small_d10'], label='Small D₁₀')
ax.plot(x_positions, very_small_d10, '-s', markersize=8, linewidth=2, 
        color=line_colors['very_small_d10'], markerfacecolor=marker_colors['very_small_d10'], 
        markeredgecolor=marker_colors['very_small_d10'], label='Very small D₁₀')

# Set axis properties
ax.set_xlim(-0.2, 2.2)
ax.set_ylim(0, 0.5)
ax.set_xticks(x_positions)
ax.set_xticklabels(x_labels)
ax.set_ylabel('d₁₀ (Å mol⁻¹ S)', fontsize=14)
ax.set_xlabel('Molecular set', fontsize=14)

# Add grid
ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
ax.set_axisbelow(True)

# Set y-axis ticks
ax.set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5])

# Add legend
ax.legend(loc='upper left', frameon=True, fancybox=False, shadow=False, 
          bbox_to_anchor=(0.02, 0.98), fontsize=11)

# Remove top and right spine tick marks but keep the spines
ax.tick_params(top=False, right=False)

# Keep all spines visible
for spine in ax.spines.values():
    spine.set_visible(True)

# Adjust layout
plt.tight_layout()

# Save the figure
plt.savefig('04_figure_reproduction.png', dpi=300, bbox_inches='tight', 
            facecolor='white', edgecolor='none')
plt.savefig('04_figure_reproduction.pdf', dpi=300, bbox_inches='tight', 
            facecolor='white', edgecolor='none')

# Display the figure
plt.show()

# Print summary
print("Figure reproduced successfully!")
print("Files saved as:")
print("- figure_reproduction.png (high-resolution PNG)")
print("- figure_reproduction.pdf (vector PDF for publications)")
