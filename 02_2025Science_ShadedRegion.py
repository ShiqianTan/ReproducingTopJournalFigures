# Acoustic wave modulation of gap plasmon cavities, 10.1126/science.adv1728, 2025

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
import matplotlib.patches as mpatches

# Create figure and axis
fig, ax = plt.subplots(figsize=(8, 6))

# Define wavelength range
wavelength = np.linspace(500, 750, 1000)

# Define scattering cross section curves
# 4nm PDMS - peak around 540nm
sigma_4nm = 2.5 * np.exp(-((wavelength - 540)**2) / (2 * 30**2))

# 6nm PDMS - peak around 630nm  
sigma_6nm = 4.2 * np.exp(-((wavelength - 630)**2) / (2 * 25**2))

# Additional curve (appears to be another size) - peak around 680nm
sigma_additional = 3.5 * np.exp(-((wavelength - 680)**2) / (2 * 35**2))

# Plot the curves
ax.plot(wavelength, sigma_4nm, 'teal', linewidth=2.5, label='4nm PDMS')
ax.plot(wavelength, sigma_6nm, 'red', linewidth=2.5, label='6nm PDMS')
ax.plot(wavelength, sigma_additional, color='blue', linewidth=2.5, label='PDMS')

# Create gradient for "Invisible NIR" region
# Gray region that decays from right to left
x_gray = np.linspace(650, 750, 100)
y_top = 5
y_bottom = 0

# Create multiple rectangles with decreasing alpha to simulate gradient
# for i, x in enumerate(x_gray[:-1]):
for i, x in enumerate(x_gray[:-1]):
    width = x_gray[1] - x_gray[0]
    # Alpha decreases from right (0.6) to left (0.1)
    # alpha = 0.6 - (i / len(x_gray)) * 0.5
    alpha = (i / len(x_gray)) * 0.2 + 0.4
    rect = Rectangle((x, y_bottom), width, y_top - y_bottom, 
                    facecolor='gray', alpha=alpha, edgecolor='none')
    ax.add_patch(rect)

# Add particle illustrations (simplified representations)
# 4nm particle - smaller circles
circle1_small = plt.Circle((530, 3.0), 8, color='brown', alpha=0.8)
circle2_small = plt.Circle((530, 2.7), 6, color='gold', alpha=0.9)
# ax.add_patch(circle1_small)
# ax.add_patch(circle2_small)

# 6nm particle - larger representation  
circle1_large = plt.Circle((630, 4.0), 12, color='darkblue', alpha=0.8)
circle2_large = plt.Circle((630, 3.6), 10, color='blue', alpha=0.9)
# ax.add_patch(circle1_large)
# ax.add_patch(circle2_large)

# Set labels and title
ax.set_xlabel('Optical Wavelength (nm)', fontsize=12)
# ax.set_ylabel('σsca/σgeo', fontsize=12)
plt.ylabel(r'$\sigma_{sc} / \sigma_{ph}$', fontsize=12)
# ax.set_title('F        Scattering Cross Section', fontsize=14, fontweight='bold', loc='left')
ax.set_title('Scattering Cross Section', fontsize=14, fontweight='bold', loc='center')

# Set axis limits and ticks
ax.set_xlim(500, 750)
ax.set_ylim(0, 5)
ax.set_xticks([550, 600, 650, 700])
ax.set_yticks([0, 1, 2, 3, 4, 5])

# Add "Invisible NIR" text
ax.text(690, 4.5, 'Invisible\nNIR', fontsize=11, ha='center', va='center', 
        fontweight='bold', color='black')

# Add labels for particles
ax.text(520, 2.5, '4nm PDMS', fontsize=10, ha='center', color='teal', fontweight='bold')
ax.text(600, 3.3, '6nm\nPDMS', fontsize=10, ha='center', color='red', fontweight='bold')
ax.text(630, 0.75, 'PDMS', fontsize=10, ha='center', color='blue', fontweight='bold')

# Remove top and right spines
ax.spines['top'].set_visible(True)
# ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(True)
# ax.spines['right'].set_visible(False)

# Adjust layout and display
plt.tight_layout()
plt.savefig('fig1Fv2.png', dpi=300, bbox_inches='tight')
plt.savefig('fig1Fv2.pdf', dpi=300)
plt.show()
