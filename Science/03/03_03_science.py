import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle

# Set up the figure with high DPI for publication quality
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 12
# plt.rcParams['font.family'] = 'Arial'
plt.rcParams['axes.linewidth'] = 1.2

# Data
categories = ['PTVs', 'SpliceAI', 'PrimateAI-3D', 'PrimateAI']
values = [51, 29, 14, 6]
colors = ['#8B4513', '#2E7D32', '#D2691E', '#DC143C']  # Brown, Green, Orange, Red

# Create figure and axis
fig, ax = plt.subplots(figsize=(8, 8))

# Create the pie chart
wedges, texts, autotexts = ax.pie(values, 
                                  labels=None,  # We'll add custom labels
                                  colors=colors,
                                  autopct='%1.0f%%',
                                  startangle=90,
                                  wedgeprops=dict(width=0.6, edgecolor='white', linewidth=2),
                                  pctdistance=0.85,
                                  textprops={'fontsize': 14, 'fontweight': 'bold', 'color': 'white'})

# Add a white circle in the center to create a donut chart
centre_circle = Circle((0,0), 0.40, fc='white', linewidth=2, edgecolor='white')
ax.add_artist(centre_circle)

# Create custom legend
legend_elements = []
for i, (cat, color) in enumerate(zip(categories, colors)):
    legend_elements.append(plt.Rectangle((0, 0), 1, 1, facecolor=color, 
                                       edgecolor='black', linewidth=0.5))

# Position legend to the right
ax.legend(legend_elements, categories, 
          loc='center left', 
          bbox_to_anchor=(1.1, 0.5),
          fontsize=12,
          frameon=False)

# Add title
ax.set_title('Rare diseases', fontsize=16, fontweight='bold', pad=20)

# Ensure the pie chart is circular
ax.set_aspect('equal')

# Remove axes
ax.axis('off')

# Adjust layout to prevent legend cutoff
plt.tight_layout()

# Save the figure in multiple formats for publication
plt.savefig('03_03_rare_diseases_pie_chart.png', dpi=300, bbox_inches='tight', 
            facecolor='white', edgecolor='none')
plt.savefig('03_03_rare_diseases_pie_chart.pdf', dpi=300, bbox_inches='tight', 
            facecolor='white', edgecolor='none')
plt.savefig('03_03_rare_diseases_pie_chart.eps', dpi=300, bbox_inches='tight', 
            facecolor='white', edgecolor='none')

plt.show()

# Print summary statistics for verification
print("Data Summary:")
print("-" * 30)
for cat, val in zip(categories, values):
    print(f"{cat}: {val}%")
print(f"Total: {sum(values)}%")

# Optional: Create a publication-ready version with specific Science journal formatting
# fig2, ax2 = plt.subplots(figsize=(6, 6))

# # Science journal prefers sans-serif fonts and specific formatting
# plt.rcParams['font.family'] = 'sans-serif'
# plt.rcParams['font.sans-serif'] = ['Helvetica', 'Arial']

# wedges2, texts2, autotexts2 = ax2.pie(values, 
#                                       colors=colors,
#                                       autopct='%1.0f%%',
#                                       startangle=90,
#                                       wedgeprops=dict(width=0.6, edgecolor='white', linewidth=1.5),
#                                       pctdistance=0.85,
#                                       textprops={'fontsize': 12, 'fontweight': 'bold', 'color': 'white'})

# centre_circle2 = Circle((0,0), 0.40, fc='white', linewidth=1.5, edgecolor='white')
# ax2.add_artist(centre_circle2)

# # Create legend with boxes (Science journal style)
# legend_elements2 = []
# for color in colors:
#     legend_elements2.append(plt.Rectangle((0, 0), 1, 1, facecolor=color, 
#                                         edgecolor='black', linewidth=0.8))

# ax2.legend(legend_elements2, categories, 
#           loc='center left', 
#           bbox_to_anchor=(1.1, 0.5),
#           fontsize=11,
#           frameon=False)

# ax2.set_title('Rare diseases', fontsize=14, fontweight='bold', pad=15)
# ax2.set_aspect('equal')
# ax2.axis('off')

# plt.tight_layout()
# plt.savefig('03_03_rare_diseases_science_format.png', dpi=300, bbox_inches='tight', 
#             facecolor='white', edgecolor='none')
# plt.savefig('03_03_rare_diseases_science_format.pdf', dpi=300, bbox_inches='tight', 
#             facecolor='white', edgecolor='none')

# plt.show()