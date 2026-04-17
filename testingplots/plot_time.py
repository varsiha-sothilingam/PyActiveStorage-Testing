import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages

meta_info = (
    "File: bnl/ch330a.pc19790301-bnl.nc (18GB, 3400 HDF5 chunks)\n"
    "HDF5 dataset: 'UM_m01s16i202_vn1106'\n"
    "Max. Threads: 100 \n"
    "Network: UoR Ethernet\n"
    "Slice: active[0:30, 0:30, 0:30]"
)

real_times = np.array([18.16, 16.39, 13.94, 13.82, 14.58, 13.88, 13.75, 14.3, 14.55, 13.82, 13.68, 14.62, 14.16, 14.56, 14.07, 13.68, 14.42, 13.8, 15.85, 13.66, 13.71, 14.0, 13.61, 14.82, 14.31, 15.24, 14.02, 14.62, 15.42, 14.69, 14.06, 14.94, 14.66, 14.28, 14.89, 15.21, 15.07, 16.42, 13.9, 14.05, 15.03, 14.59, 13.64, 13.87, 16.04, 14.41, 17.32, 13.67, 13.63, 14.23, 15.04, 14.63, 13.64, 13.51, 14.83, 13.86, 15.68, 17.11, 14.55, 14.29])
user_times = np.array([1.87, 1.91, 1.51, 1.45, 1.5, 1.49, 1.48, 1.52, 1.54, 1.46, 1.43, 1.51, 1.46, 1.5, 1.46, 1.43, 1.5, 1.48, 1.76, 1.44, 1.43, 1.47, 1.44, 1.58, 1.5, 1.76, 1.47, 1.54, 1.86, 1.6, 1.53, 1.58, 1.51, 1.51, 1.55, 1.69, 1.57, 2.14, 1.52, 1.49, 1.56, 1.56, 1.42, 1.48, 1.93, 1.51, 2.0, 1.44, 1.43, 1.57, 1.68, 1.5, 1.44, 1.42, 1.53, 1.5, 1.8, 2.13, 1.53, 1.64])
sys_times = np.array([1.0, 1.07, 0.81, 0.8, 0.83, 0.78, 0.79, 0.82, 0.83, 0.79, 0.78, 0.82, 0.81, 0.81, 0.79, 0.77, 0.83, 0.81, 0.98, 0.79, 0.77, 0.78, 0.78, 0.87, 0.81, 0.95, 0.81, 0.84, 1.02, 0.89, 0.81, 0.89, 0.84, 0.82, 0.84, 0.94, 0.86, 1.2, 0.83, 0.82, 0.86, 0.84, 0.77, 0.8, 1.04, 0.82, 0.98, 0.78, 0.79, 0.86, 0.91, 0.82, 0.78, 0.79, 0.83, 0.8, 0.97, 1.09, 0.82, 0.9])
memory_mb = np.array([285.59375, 298.6875, 280.109375, 277.984375, 298.109375, 280.46875, 279.671875, 285.109375, 270.359375, 280.015625, 273.109375, 280.375, 269.328125, 277.21875, 274.859375, 287.796875, 278.546875, 277.125, 297.203125, 274.15625, 269.546875, 275.5, 270.4375, 296.765625, 281.546875, 295.5, 269.515625, 279.578125, 293.578125, 279.859375, 282.25, 297.859375, 294.0, 285.390625, 287.46875, 288.015625, 283.375, 297.59375, 284.734375, 273.984375, 284.265625, 293.921875, 271.03125, 280.515625, 313.8125, 288.28125, 291.609375, 275.859375, 286.265625, 286.921875, 304.75, 295.25, 274.640625, 284.65625, 290.046875, 278.21875, 298.328125, 316.390625, 284.703125, 297.796875])

# 2. Calculations
wait = real_times - (user_times + sys_times)
cpu_pct = ((user_times + sys_times) / real_times) * 100

def add_subplot_pair(fig, gs_spec, data, title, color, xlabel):
    """Creates a nested Histogram + Stats plot pair."""
    # Split the grid cell into Histogram (top) and Stats (bottom)
    inner_gs = gs_spec.subgridspec(2, 1, height_ratios=[3, 1], hspace=0.05)
    ax_hist = fig.add_subplot(inner_gs[0, 0])
    ax_stats = fig.add_subplot(inner_gs[1, 0], sharex=ax_hist)

    mean, std = np.mean(data), np.std(data)
    l_bound, u_bound = mean - (2 * std), mean + (2 * std)
    clipped = np.clip(data, l_bound, u_bound)

    # Histogram
    ax_hist.hist(clipped, bins=15, range=(l_bound, u_bound), color=color, edgecolor='white', alpha=0.8)
    ax_hist.set_title(title, fontsize=10, fontweight='bold', loc='left', pad=5)
    ax_hist.set_ylabel('Counts', fontsize=8)
    ax_hist.tick_params(labelsize=8, labelbottom=False)
    
    # Label stats on histogram
    ax_hist.text(0.98, 0.75, f'Mean: {mean:.3f}\nStd Dev: {std:.3f}', 
                 transform=ax_hist.transAxes, ha='right', fontsize=8,
                 bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))

    # Error Bar (Mean + Std Dev)
    ax_stats.errorbar(mean, 0, xerr=std, fmt='o', color='black', capsize=4)
    ax_stats.set_yticks([])
    ax_stats.set_xlabel(xlabel, fontsize=9)
    ax_stats.tick_params(labelsize=8, labelbottom=True)
    
    # Visual cues for clipping
    ax_stats.axvline(l_bound, color='gray', linestyle=':', alpha=0.5)
    ax_stats.axvline(u_bound, color='gray', linestyle=':', alpha=0.5)

def main():
    # Final Output Filename
    output_pdf = "performance_summary_report.pdf"
    
    # Accessible Palette
    colors = ['#004d40', '#1a9850', '#0077b6', '#f6b203', '#8e44ad']

    # Setup A4 Page
    fig = plt.figure(figsize=(8.27, 11.69))
    
    # Layout: Row 0 for Meta Info, Rows 1-3 for 2-column plots
    gs_main = fig.add_gridspec(4, 2, height_ratios=[0.5, 2, 2, 2], 
                               hspace=0.4, wspace=0.3, 
                               left=0.12, right=0.92, top=0.92, bottom=0.08)

    # Meta Info Header (Full Width)
    ax_meta = fig.add_subplot(gs_main[0, :])
    ax_meta.axis('off')
    ax_meta.text(0, 1.1, "TEST CONDITIONS", fontsize=14, fontweight='bold')
    ax_meta.text(0, 0.1, meta_info, fontsize=9, family='monospace', linespacing=1.4)

    # COLUMN 1 (Left)
    add_subplot_pair(fig, gs_main[1, 0], user_times, "User Time", colors[0], "Seconds")
    add_subplot_pair(fig, gs_main[2, 0], sys_times,  "Sys Time",  colors[1], "Seconds")
    add_subplot_pair(fig, gs_main[3, 0], memory_mb,  "Max Memory Usage (RSS)", colors[4], "MB")

    # COLUMN 2 (Right)
    add_subplot_pair(fig, gs_main[1, 1], cpu_pct,    "CPU Usage Percentage", colors[2], "Percentage (%)")
    add_subplot_pair(fig, gs_main[2, 1], wait,       "Waiting Time (I/O Bound)", colors[3], "Seconds")
    
    # Empty space at bottom right (gs_main[3, 1]) is left blank

    with PdfPages(output_pdf) as pdf:
        pdf.savefig(fig)
        plt.close()

    print(f"Report generated: {output_pdf}")

if __name__ == "__main__":
    main()
