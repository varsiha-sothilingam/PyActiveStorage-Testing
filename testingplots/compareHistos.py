import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import argparse
import importlib.util
import sys

def load_data_file(file_path):
    spec = importlib.util.spec_from_file_location("data_module", file_path)
    data_module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(data_module)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        sys.exit(1)
    return data_module

def parse_meta(meta1, meta2):
    """Convert meta_info strings into aligned rows"""
    lines1 = meta1.strip().split("\n")
    lines2 = meta2.strip().split("\n")

    max_len = max(len(lines1), len(lines2))
    lines1 += [""] * (max_len - len(lines1))
    lines2 += [""] * (max_len - len(lines2))

    rows = []
    for l1, l2 in zip(lines1, lines2):
        key = l1.split(":")[0] if ":" in l1 else ""
        val1 = l1.split(":", 1)[1].strip() if ":" in l1 else l1
        val2 = l2.split(":", 1)[1].strip() if ":" in l2 else l2
        rows.append([key, val1, val2])
    return rows

def add_overlay_hist(ax, data1, data2, title, color, xlabel):
    mean1, std1 = np.mean(data1), np.std(data1)
    mean2, std2 = np.mean(data2), np.std(data2)

    lower = min(mean1 - 2*std1, mean2 - 2*std2)
    upper = max(mean1 + 2*std1, mean2 + 2*std2)

    bins = np.linspace(lower, upper, 15)

    # Plot Test Setting 1 (filled)
    ax.hist(data1, bins=bins, color=color, alpha=0.6, label="Test Setting 1")

    # Plot Test Setting 2 (outline + hatch)
    ax.hist(data2, bins=bins,
            histtype='bar',
            edgecolor=color,
            linewidth=2,
            facecolor='none',
            hatch='//',
            label="Test Setting 2")

    ax.set_title(title, fontsize=10, fontweight='bold')
    ax.set_xlabel(xlabel, fontsize=9)
    ax.set_ylabel("Counts", fontsize=8)
    ax.tick_params(labelsize=8)

    # Stats above
    stats = (
        f"T1 μ={mean1:.3f}, σ={std1:.3f}\n"
        f"T2 μ={mean2:.3f}, σ={std2:.3f}"
    )
    ax.text(0.5, 1.15, stats, transform=ax.transAxes,
            ha='center', va='bottom', fontsize=8,
            bbox=dict(facecolor='white', alpha=0.9, edgecolor='none'))

    ax.legend(fontsize=8)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i1", required=True)
    parser.add_argument("-i2", required=True)
    parser.add_argument("-o", required=True)
    args = parser.parse_args()

    d1 = load_data_file(args.i1)
    d2 = load_data_file(args.i2)

    # Data
    real1, user1, sys1, mem1 = d1.real_times, d1.user_times, d1.sys_times, d1.memory_mb
    real2, user2, sys2, mem2 = d2.real_times, d2.user_times, d2.sys_times, d2.memory_mb

    wait1 = real1 - (user1 + sys1)
    cpu1 = ((user1 + sys1) / real1) * 100

    wait2 = real2 - (user2 + sys2)
    cpu2 = ((user2 + sys2) / real2) * 100

    # Figure
    fig = plt.figure(figsize=(8.27, 11.69))
    gs = fig.add_gridspec(4, 2, height_ratios=[1.2, 1, 1, 1], hspace=0.7)

    # ===== META TABLE =====
    ax_table = fig.add_subplot(gs[0, :])
    ax_table.axis('off')

    # Prepare the rows
    rows = parse_meta(d1.meta_info, d2.meta_info)

    # Create the table with centered cells
    table = ax_table.table(
    cellText=rows,
    colLabels=["Setting", "Test Setting 1", "Test Setting 2"],
    loc='center',
    cellLoc='center'   # centers text in all cells
    )

    # Adjust font size and scaling
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1, 1.3)

    # Center all cells
    for (row, col), cell in table.get_celld().items():
       cell.set_text_props(ha='center', va='center')

    # Bold the header row
    for col in range(len(["Setting", "Test Setting 1", "Test Setting 2"])):
       table[(0, col)].set_text_props(fontweight='bold')

    # Bold the first column, skipping top-left corner
    for row in range(1, len(rows)+1):  # +1 because row 0 is header
       table[(row, 0)].set_text_props(fontweight='bold')


    # ===== HISTOGRAMS =====
    colors = ['#004d40', '#1a9850', '#0077b6', '#f6b203', '#8e44ad']

    add_overlay_hist(fig.add_subplot(gs[1, 0]), user1, user2, "User Time", colors[0], "Seconds")
    add_overlay_hist(fig.add_subplot(gs[2, 0]), sys1, sys2, "Sys Time", colors[1], "Seconds")
    add_overlay_hist(fig.add_subplot(gs[3, 0]), mem1, mem2, "Memory", colors[4], "MB")

    add_overlay_hist(fig.add_subplot(gs[1, 1]), cpu1, cpu2, "CPU %", colors[2], "%")
    add_overlay_hist(fig.add_subplot(gs[2, 1]), wait1, wait2, "Wait Time", colors[3], "Seconds")

    fig.add_subplot(gs[3, 1]).axis('off')

    with PdfPages(args.o) as pdf:
        pdf.savefig(fig)
        plt.close()

    print(f"Saved: {args.o}")

if __name__ == "__main__":
    main()