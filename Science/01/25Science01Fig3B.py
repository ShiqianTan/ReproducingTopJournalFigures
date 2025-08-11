import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# -----------------------------
# Example synthetic data
# Replace with your real experimental data
# -----------------------------
time = np.linspace(0, 6, 15)  # time points

# Simulate data for different concentrations
concentrations = [8, 4, 2, 1, 0.5, 0.25, 0.125]  # µM
colors = plt.cm.Blues(np.linspace(1, 0.3, len(concentrations)))

# Function to simulate % crosslinking
def simulate_curve(t, conc):
    k = 1.2 * conc / (conc + 1)   # rate constant increases with conc
    max_val = 100 * conc / (conc + 0.5)
    return max_val * (1 - np.exp(-k * t))

# Create fake experimental points with noise
np.random.seed(0)
data = []
errors = []
for conc in concentrations:
    y = simulate_curve(time, conc)
    noise = np.random.normal(0, 5, len(time))
    y_noisy = y + noise
    y_noisy[y_noisy < 0] = 0
    err = np.random.uniform(2, 5, len(time))
    data.append(y_noisy)
    errors.append(err)

# -----------------------------
# Figure settings for publication
# -----------------------------
mpl.rcParams.update({
    'font.size': 14,
    'axes.linewidth': 1.5,
    'xtick.major.width': 1.2,
    'ytick.major.width': 1.2,
    # 'xtick.direction': 'in',
    # 'ytick.direction': 'in',
    'xtick.top': False,
    'ytick.right': False
})

fig, ax = plt.subplots(figsize=(6, 4.5), dpi=300)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
# -----------------------------
# Plot curves with error bars
# -----------------------------
for conc, color, yvals, err in zip(concentrations, colors, data, errors):
    # Scatter points with error bars
    ax.errorbar(
        time, yvals, yerr=err, fmt='o', ms=4,
        color=color, ecolor=color, elinewidth=1, capsize=2, alpha=0.9
    )
    # Fit smooth curve
    t_fit = np.linspace(0, 6, 200)
    y_fit = simulate_curve(t_fit, conc)
    ax.plot(t_fit, y_fit, color=color, lw=2, label=f"{conc} µM")

# -----------------------------
# Axis labels and limits
# -----------------------------
ax.set_xlim(0, 6)
ax.set_ylim(0, 110)
ax.set_xlabel("Time (hours)")
ax.set_ylabel("% Crosslinking\n(biochemical)")

# Legend
ax.legend(
    frameon=False,
    loc='center left',
    bbox_to_anchor=(1.02, 0.5),
    handlelength=1.2
)

# Tight layout for publication
plt.tight_layout()
plt.savefig("25Science01Fig3B.png", dpi=300)
plt.savefig("25Science01Fig3B.pdf", dpi=300)
plt.show()
