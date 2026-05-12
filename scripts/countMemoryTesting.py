import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Arial'

# 1. Generate some dummy data
np.random.seed(42)
#data = [np.random.normal(loc, 1, 1000) for loc in [5, 10, 15, 20]]

count_collapse_false_memory_mb           = np.array([ 312.58, 300.72, 294.31, 298.5, 325.61, 301.27, 326.69, 315.28, 297.58, 304.66, 315.3, 315.42, 308.89, 298.22, 305.73, 313.39, 321.34, 300.06, 295.55])
count_collapse_true_memory_mb            = np.array([304.59, 315.25, 309.62, 294.44, 307.98, 308.34, 309.3, 298.44, 290.47, 294.58, 295.7, 296.72, 311.88, 293.97, 309.66, 291.38, 268.56, 316.3, 305.45, 298.48])

count_as_bytes_collapse_false_memory_mb  = np.array([306.09, 293.28, 321.59, 290.44, 296.95, 298.2, 292.97, 309.14, 298.59, 305.84, 305.47, 289.39, 295.12, 321.28, 304.34, 294.8, 322.62, 297.42, 305.36, 301.16])
count_as_bytes_collapse_true_memory_mb   = np.array([302.47, 297.81, 292.66, 320.36, 298.84, 303.19, 302.61, 292.38, 290.03, 306.19, 292.64, 323.19, 293.3, 303.09, 323.25, 302.95, 305.45, 312.8, 294.11, 318.56])


count_collapse_false_memory_mb           = np.array([305.02, 291.88, 304.19, 291.84, 309.69, 303.48, 287.69, 300.31, 302.17, 318.05, 298.3, 317.52, 300.19, 293.77, 295.09, 305.73, 303.52, 289.06, 309.02, 294.97])
count_collapse_true_memory_mb            = np.array([309.33, 311.75, 302.92, 304.94, 291.52, 302.97, 307.58, 301.25, 292.86, 296.62, 303.12, 302.95, 310.27, 297.05, 294.08, 304.62, 308.06, 302.38, 306.02, 291.53])

count_as_bytes_collapse_false_memory_mb  = np.array([270.48, 301.19, 292.83, 308.31, 291.86, 302.66, 296.34, 268.61, 325.56, 309.67, 298.56, 291.27, 303.5, 289.78, 315.62, 302.89, 304.78, 262.08, 318.52, 295.88])
count_as_bytes_collapse_true_memory_mb   = np.array([324.36, 291.84, 309.38, 309.83, 294.36, 315.17, 295.31, 295.75, 302.12, 309.19, 307.09, 310.42, 304.78, 302.5, 301.98, 321.66, 310.2, 295.67, 298.41, 298.95])

# Data order: [ (0,0), (0,1), (1,0), (1,1) ]
data = [
    count_collapse_false_memory_mb,    # Top-Left
    count_collapse_true_memory_mb,     # Top-Right
    count_as_bytes_collapse_false_memory_mb,    # Bottom-Left
    count_as_bytes_collapse_true_memory_mb       # Bottom-Right
]

fig, axs = plt.subplots(2, 2, figsize=(10, 8), sharex=False, sharey=False)

# Labels for the grid
rows = ['count', 'count_as_bytes']
cols = ['No collapse', 'Axis Collapsed']


# 2. Plotting the Histograms
for i, ax in enumerate(axs.flat):
    current_data = data[i]
    mean_val = np.mean(current_data)
    std_val = np.std(current_data)
    
    
    # Plot Histogram
    ax.hist(current_data, bins=30, color="#1a76d1", alpha=0.7, edgecolor='white')

    # Add a single label for the whole x-axis and y-axis
    ax.set_xlabel('Memory (MB)', fontsize=10)

    # 3. Show Mean Value
    ax.axvline(mean_val, color="#ffaa00", linestyle='--', lw=2, label=f'Mean: {mean_val:.2f}± {std_val:.2f}')

    ax.legend(frameon=False, loc='upper right')
    
    print("mean +/- std_Dev" , mean_val, std_val)
    
ax.tick_params(labelleft=True, labelbottom=True)

# 4. Applying Row and Column Labels
# Labeling the columns (Top row)
for ax, col in zip(axs[0], cols):
    ax.set_title(col, fontweight='bold', size=14, pad=10)

# Labeling the rows (Left side)
for ax, row in zip(axs[:,0], rows):
    ax.set_ylabel(row, fontweight='bold', size=14, labelpad=10)

# Clean up layout
plt.tight_layout()
#plt.show()
plt.savefig("count_memorytest.pdf")