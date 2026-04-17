import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import argparse
import importlib.util
import sys
import os
from datetime import datetime


def load_data_file(file_path):
    """Dynamically imports the .py data file."""
    spec = importlib.util.spec_from_file_location("data_module", file_path)
    data_module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(data_module)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        sys.exit(1)
    return data_module

def add_subplot_pair(fig, gs_spec, data, title, color, xlabel):
    """Creates a nested Histogram + Stats plot pair."""
    inner_gs = gs_spec.subgridspec(2, 1, height_ratios=[3, 1], hspace=0.05)
    ax_hist = fig.add_subplot(inner_gs[0, 0])
    ax_stats = fig.add_subplot(inner_gs[1, 0], sharex=ax_hist)

    mean, std = np.mean(data), np.std(data)
    l_bound, u_bound = mean - (2 * std), mean + (2 * std)
    clipped = np.clip(data, l_bound, u_bound)

    ax_hist.hist(clipped, bins=15, range=(l_bound, u_bound), color=color, edgecolor='white', alpha=0.8)
    ax_hist.set_title(title, fontsize=10, fontweight='bold', loc='left', pad=5)
    ax_hist.set_ylabel('Counts', fontsize=8)
    ax_hist.tick_params(labelsize=8, labelbottom=False)
    ax_hist.text(0.98, 0.75, f'Mean: {mean:.3f}\nStd Dev: {std:.3f}', 
                 transform=ax_hist.transAxes, ha='right', fontsize=8,
                 bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))

    ax_stats.errorbar(mean, 0, xerr=std, fmt='o', color='black', capsize=4)
    ax_stats.set_yticks([])
    ax_stats.set_xlabel(xlabel, fontsize=9)
    ax_stats.tick_params(labelsize=8, labelbottom=True)

def main():
    parser = argparse.ArgumentParser(description="Generate A4 Performance Report")
    parser.add_argument("-i", "--input", required=True, help="Input .py data file")
    parser.add_argument("-o", "--output", required=True, help="Output PDF name")
    args = parser.parse_args()

    # --- DYNAMIC DATA LOADING ---
    data = load_data_file(args.input)
    
    # Map variables from the module to local names
    real = data.real_times
    user = data.user_times
    sys_t = data.sys_times
    mem = data.memory_mb
    meta = data.meta_info

    # Secondary Calculations
    wait = real - (user + sys_t)
    cpu_pct = ((user + sys_t) / real) * 100

    # Palette
    colors = ['#004d40', '#1a9850', '#0077b6', '#f6b203', '#8e44ad']

    # Plotting setup
    fig = plt.figure(figsize=(8.27, 11.69))
    gs_main = fig.add_gridspec(4, 2, height_ratios=[0.5, 2, 2, 2], hspace=0.4, wspace=0.3, 
                               left=0.12, right=0.92, top=0.92, bottom=0.08)
#-----
    #ax_meta = fig.add_subplot(gs_main[0, :])
    #ax_meta.axis('off')
    #ax_meta.text(0, 1.1, "TEST CONDITIONS", fontsize=14, fontweight='bold')
    #ax_meta.text(0, 0.1, meta, fontsize=9, family='monospace', linespacing=1.4)


    created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    input_filename = os.path.basename(args.input)

# 2. Append new info to the existing meta_info from the file
# If your 'data' object already has meta_info, we can combine them:
    full_meta = (
        f"Testing plots generated: {created_date}\n"
        f"{data.meta_info}"
    )

    # 3. Adjust the header plotting to prevent overlap
    # Use a higher Y coordinate for the title and a lower one for the text
    ax_meta = fig.add_subplot(gs_main[0, :])
    ax_meta.axis('off')

    # Move the Title further up
    #ax_meta.text(0, 1.4, "TEST CONDITIONS", fontsize=14, fontweight='bold')

    # Place the full metadata below it with safe spacing
    ax_meta.text(0, 0.05, full_meta, fontsize=9, family='monospace', linespacing=1.5, verticalalignment='bottom')



#----



    # Column 1
    add_subplot_pair(fig, gs_main[1, 0], user, "User Time", colors[0], "Seconds")
    add_subplot_pair(fig, gs_main[2, 0], sys_t, "Sys Time", colors[1], "Seconds")
    add_subplot_pair(fig, gs_main[3, 0], mem, "Max Memory Usage (RSS)", colors[4], "MB")

    # Column 2
    add_subplot_pair(fig, gs_main[1, 1], cpu_pct, "CPU Usage Percentage", colors[2], "Percentage (%)")
    add_subplot_pair(fig, gs_main[2, 1], wait, "Waiting Time (I/O Bound)", colors[3], "Seconds")

    with PdfPages(args.output) as pdf:
        pdf.savefig(fig)
        plt.close()
    
    print(f"Report generated: {args.output}")

if __name__ == "__main__":
    main()

