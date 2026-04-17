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

def add_dual_hists(fig, data1, data2, title, color, xlabel):
    """Creates two side-by-side histograms on the provided figure."""
    # Split the figure into two subplots
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2)
    
    axes = [ax1, ax2]
    datasets = [data1, data2]
    labels = ["Test Setting 1", "Test Setting 2"]
    # Setting 2 gets a hatch to differentiate if printed in B&W
    styles = [{'alpha': 1, 'hatch': ''}, {'alpha': 1, 'hatch': ''}]

    for ax, data, label, style in zip(axes, datasets, labels, styles):
        mean, std = np.mean(data), np.std(data)
        
        # Plot individual histogram
        ax.hist(data, bins=10, color=color, alpha=style['alpha'], 
                edgecolor='black', hatch=style['hatch'], label=label)
        
        # Add Mean Line
        ax.axvline(mean, color='red', linestyle='dashed', linewidth=1.5, label=f'Mean: {mean:.2f}')
        
        # Formatting
        ax.set_title(f"{label}", fontsize=12, fontweight='bold')
        ax.set_xlabel(f"{xlabel}", fontsize=10)
        ax.set_ylabel("Counts", fontsize=10)
        ax.grid(axis='y', alpha=0.3)
        
        # Individual Stats box for each plot
        stats_text = f"Avg: {mean:.3f} {xlabel}\nStd: {std:.3f}"
        ax.text(0.95, 0.90, stats_text, transform=ax.transAxes, fontsize=9,
                verticalalignment='top', horizontalalignment='right',
                bbox=dict(boxstyle='round', facecolor='white', alpha=1, edgecolor='gray'))
        ax.legend(loc='upper left', fontsize=8)

    fig.suptitle(f"Comparison: {title}", fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # Adjust for suptitle

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i1", required=True)
    parser.add_argument("-i2", required=True)
    parser.add_argument("-o", required=True)
    args = parser.parse_args()

    d1 = load_data_file(args.i1)
    d2 = load_data_file(args.i2)

    # Derived Data
    wait1 = d1.real_times - (d1.user_times + d1.sys_times)
    cpu1 = ((d1.user_times + d1.sys_times) / d1.real_times) * 100
    wait2 = d2.real_times - (d2.user_times + d2.sys_times)
    cpu2 = ((d2.user_times + d2.sys_times) / d2.real_times) * 100

    plot_items = [
        (d1.user_times, d2.user_times, "User Time", '#004d40', "Seconds"),
        (d1.sys_times, d2.sys_times, "Sys Time", '#1a9850', "Seconds"),
        (d1.memory_mb, d2.memory_mb, "Memory Usage", '#8e44ad', "MB"),
        (cpu1, cpu2, "CPU Utilization", '#0077b6', "%"),
        (wait1, wait2, "Wait Time", '#f6b203', "Seconds")
    ]

    with PdfPages(args.o) as pdf:
        # --- PAGE 1: METADATA TABLE ---
        fig_table = plt.figure(figsize=(11.69, 8.27))
        ax_table = fig_table.add_subplot(1, 1, 1)
        ax_table.axis('off')
        
        rows = parse_meta(d1.meta_info, d2.meta_info)
        table = ax_table.table(cellText=rows, colLabels=["Property", "Test Setting 1", "Test Setting 2"],
                               loc='center', cellLoc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 1.5)
        for (row, col), cell in table.get_celld().items():
            if row == 0 or col == 0: cell.set_text_props(fontweight='bold')

        plt.title("Metadata Comparison", fontsize=16, pad=20)
        pdf.savefig(fig_table)
        plt.close()

        # --- SUBSEQUENT PAGES: SIDE-BY-SIDE HISTOGRAMS ---
        for data1, data2, title, color, units in plot_items:
            fig = plt.figure(figsize=(11.69, 8.27)) 
            add_dual_hists(fig, data1, data2, title, color, units)
            pdf.savefig(fig)
            plt.close()

    print(f"Successfully saved multi-page side-by-side report to: {args.o}")

if __name__ == "__main__":
    main()