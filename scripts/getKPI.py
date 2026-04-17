import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.lines import Line2D
from scipy import stats
from pathlib import Path
import importlib.util

# --- GLOBAL CONFIGURATION ---
plt.rcParams['font.family'] = 'Arial'
ROW_SPACING = 1.0

# --- HELPER FUNCTIONS ---

def getVals(path, array_name="real_times"):
    """Load a Python file at 'path' as a module and return the specified array."""
    file_path = Path(path)
    if not file_path.exists():
        print(f"DEBUG: File not found at {file_path}") # This will tell you why it's empty
        return np.array([])
    spec = importlib.util.spec_from_file_location("module_from_file", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, array_name)

def get_wait_t(user_times, sys_times,real_times):
    wait = real_times - (user_times + sys_times)
    return wait

def get_cpu(user_times, sys_times,real_times):
    cpu_pct = ((user_times + sys_times) / real_times) * 100
    return cpu_pct

def calculate_stats(data_on, data_off):
    """Returns a dictionary of statistics for Active (on) and Local (off) data."""
    if len(data_on) == 0 or len(data_off) == 0:
        return None
        
    m_on, s_on = np.mean(data_on), np.std(data_on)
    m_off, s_off = np.mean(data_off), np.std(data_off)
    ratio = m_off / m_on

    # Propagation of error formula for a quotient
    ratio_std = ratio * np.sqrt((s_off/m_off)**2 + (s_on/m_on)**2)
    return {
        "mean_on": m_on, "std_on": s_on,
        "mean_off": m_off, "std_off": s_off,
        "ratio": ratio, "ratio_std": ratio_std
    }


def calculate_array_ratios(val1_arr, err1_arr, val2_arr, err2_arr):
    """
    Calculates ratios and propagated uncertainties for arrays of data.
    
    Returns:
        tuple: (ratio_array, uncertainty_array)
    """
    # Convert inputs to numpy arrays for vectorized math
    v1, e1 = np.array(val1_arr), np.array(err1_arr)
    v2, e2 = np.array(val2_arr), np.array(err2_arr)
    
    # 1. Calculate the ratios
    ratios = v1 / v2
    
    # 2. Calculate propagated uncertainty: R * sqrt((e1/v1)^2 + (e2/v2)^2)
    # np.sqrt and **2 work element-wise across the entire array
    uncertainties = np.abs(ratios) * np.sqrt((e1 / v1)**2 + (e2 / v2)**2)
    
    return ratios, uncertainties


def plot_dual_hybrid_row(ax, y_pos, data_on, data_off, show_violins=True):
    """Plots the violin and error bars for a single row."""
    colors = ["#fd5400", "#939393"] 
    datasets = [data_on, data_off]
    
    for i, data in enumerate(datasets):
        if len(data) == 0: continue
        color = colors[i]
        offset = 0.1 if i == 0 else 0.5
        
        mean, std = np.mean(data), np.std(data)
        
        if show_violins:
            kde = stats.gaussian_kde(data)
            x_range = np.linspace(min(data) - std, max(data) + std, 100)
            kde_values = (kde(x_range) / max(kde(x_range))) * 0.35 
            ax.fill_between(x_range, y_pos + offset, y_pos + offset + kde_values, alpha=0.2, color=color)
            ax.plot(x_range, y_pos + offset + kde_values, color=color, lw=1)

        ax.errorbar(mean, y_pos + offset, xerr=std, fmt='o', color=color, 
                    elinewidth=2.5, capsize=4, markersize=8, zorder=3)

# --- PRIMARY PLOTTING FUNCTIONS ---
def generate_execution_plot_old(custom_data,meta_text, save_path):
    fig, ax = plt.subplots(figsize=(12, 8))
    y_ticks, y_labels = [], []

    summary_stats = {"on_means": [], "on_stds": [], "off_means": [], "off_stds": []}

    for i, (d_on, d_off, label) in enumerate(custom_data):
        y_pos = i * ROW_SPACING
        plot_dual_hybrid_row(ax, y_pos, d_on, d_off)
        
        y_ticks.append(y_pos + 0.3)
        y_labels.append(label)

        if i < len(custom_data) - 1:
            ax.axhline(y_pos + 1.15, color="#bbbbbb", lw=1.5, linestyle=':')

        # Stats Text
        s = calculate_stats(d_on, d_off)
        if s:
            labels_text = "Active:\nLocal:\nRatio:"
            values_text = (
                f"{s['mean_on']:>7.2f} ± {s['std_on']:>5.2f}\n"
                f"{s['mean_off']:>7.2f} ± {s['std_off']:>5.2f}\n"
                f"{s['ratio']:>7.2f} ± {s['ratio_std']:>5.2f}"
            )
            summary_stats["on_means"].append(s['mean_on'])
            summary_stats["on_stds"].append(s['std_on'])
            summary_stats["off_means"].append(s['mean_off'])
            summary_stats["off_stds"].append(s['std_off'])

            ax.text(0.835, y_pos + 0.3, labels_text, transform=ax.get_yaxis_transform(),
                    fontsize=12, va='center', ha='right')
            ax.text(0.84, y_pos + 0.3, values_text, transform=ax.get_yaxis_transform(),
                    fontsize=12, va='center', ha='left', family='monospace')



    # Formatting
    ax.set_ylim(-0.5, (len(custom_data) * ROW_SPACING) + 0.5)
    ax.set_xscale('symlog', linthresh=35)
    ax.set_xlim(10, 3500)
    #ax.xaxis.set_major_locator(ticker.FixedLocator([10, 20, 30, 100, 1000, 2700]))
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_labels, fontsize=12)
    ax.set_xlabel('Execution Time (seconds)', fontsize=12)
    ax.set_ylabel('Target (%)', fontsize=12)
    
    # Header & Legend
    ax.text(0.01, 0.98, "Reduction execution time relative to slice size", fontweight='bold', transform=ax.transAxes, fontsize=12, va='top')
    ax.text(0.01, 0.945, meta_text, transform=ax.transAxes, fontsize=12, va='top', linespacing=1.5)
    
    legend_el = [Line2D([0], [0], color="#fd5400", marker='o', lw=2, label='Active Storage'),
                 Line2D([0], [0], color='#939393', marker='o', lw=2, label='Local Storage ')]
    ax.legend(handles=legend_el, loc='upper right',fontsize=12, frameon=False, bbox_to_anchor=(0.95, 0.98))

    plt.tight_layout()
    plt.savefig(save_path)
    return summary_stats

def generate_execution_plot(custom_data, meta_text, save_path):
    # 1. Create subplots with a reduced height (6) to prevent vertical stretching
    fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True, figsize=(12, 6), 
                                   gridspec_kw={'width_ratios': [1, 2]})
    fig.subplots_adjust(wspace=0.05)  # Close the gap between the broken axes

    # 2. Configuration for spacing
    ROW_SPACING = 1.0 
    y_ticks, y_labels = [], []

    for i, (d_on, d_off, label) in enumerate(custom_data):
        y_pos = i * ROW_SPACING
        
        # Plot data on both sides of the break
        plot_dual_hybrid_row(ax1, y_pos, d_on, d_off)
        plot_dual_hybrid_row(ax2, y_pos, d_on, d_off)
        
        # Align labels and ticks with the center of the two bars
        y_ticks.append(y_pos + 0.3)
        y_labels.append(label)

        # 3. Improved separator line logic (draws below the row, skipping the bottom)
        if i > 0:
            line_y = y_pos - 0.1
            ax1.axhline(line_y, color="#bbbbbb", lw=1.0, linestyle='--', alpha=0.4)
            ax2.axhline(line_y, color="#bbbbbb", lw=1.0, linestyle='--', alpha=0.4)

        # 4. Stats Text - Centered vertically with the bars
        s = calculate_stats(d_on, d_off)
        if s:
            labels_text = "Active:\n\n\n\n\nLocal:"
            values_text = (
                f"{s['mean_on']:>7.2f} ± {s['std_on']:>5.2f}\n\n\n\n\n"
                f"{s['mean_off']:>7.2f} ± {s['std_off']:>5.2f}"
            )
            text_y = y_pos + 0.3
            ax2.text(0.75, text_y, labels_text, transform=ax2.get_yaxis_transform(),
                    fontsize=10, va='center', ha='right')
            ax2.text(0.76, text_y, values_text, transform=ax2.get_yaxis_transform(),
                    fontsize=10, va='center', ha='left')

    # 5. Broken Axis Window Limits
    ax1.set_xlim(10, 60)     # The "fast" cluster
    ax2.set_xlim(950, 1100)  # The "slow" S3 Local outlier
    
    # Hide spines between ax1 and ax2
    ax1.spines['right'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    ax1.yaxis.tick_left()
    ax2.tick_params(left=False, labelright=False) 

    # 6. Draw the diagonal "break" marks (//)
    d = .015 
    kwargs = dict(transform=ax1.transAxes, color='k', clip_on=False, lw=1)
    ax1.plot((1-d, 1+d), (-d, +d), **kwargs) # bottom-left
    ax1.plot((1-d, 1+d), (1-d, 1+d), **kwargs) # top-left

    kwargs.update(transform=ax2.transAxes) 
    ax2.plot((-d/2, +d/2), (-d, +d), **kwargs) # bottom-right
    ax2.plot((-d/2, +d/2), (1-d, 1+d), **kwargs) # top-right

    # 7. Final Formatting
    ax1.set_ylim(0, (len(custom_data) * ROW_SPACING) +0.2)
    ax1.set_yticks(y_ticks)
    ax1.set_yticklabels(y_labels, fontsize=10)
    
    # Shared X-axis label
    fig.text(0.5, 0.02, 'Execution Time (seconds)', ha='center', fontsize=12)
    
    # Header using corrected fig.transFigure
    fig.text(0.13, 0.87, "Reduction execution time for different protocols", 
             fontweight='bold', transform=fig.transFigure, fontsize=12, va='top')
    fig.text(0.13, 0.83, meta_text, transform=fig.transFigure, fontsize=10, va='top', linespacing=1.3)
    
    # Legend
    legend_el = [Line2D([0], [0], color="#fd5400", marker='o', lw=2, label='Active Storage'),
                 Line2D([0], [0], color='#939393', marker='o', lw=2, label='Local Storage')]
    ax2.legend(handles=legend_el, loc='upper right', fontsize=10, frameon=False)

    plt.savefig(save_path, bbox_inches='tight')
# --- MAIN EXECUTION ---
def main():
    f_warm = "/Users/dh935740@reading.ac.uk/testing_PyActiveStorage/tests_Varsiha/output/Local_v_Active/f_ch330a.pc19790301-def_64Chunk/Target100_Active_f_ch330a.pc19790301-def.nc_var_UM_m01s16i202_vn1106_slice_0_40_0_1920_0_2560_20260407_151811.py"
    #f_warm = "/Users/dh935740@reading.ac.uk/testing_PyActiveStorage/tests_Varsiha/output/Local_v_Active/f_ch330a.pc19790301-bnl_3400Chunk/Target5_Active_f_ch330a.pc19790301-bnl.nc_var_UM_m01s16i202_vn1106_slice_0_14_0_707_0_942_20260330_135715.py"
    f_cold = "f_coldVals.py"

    real_times_warm = getVals(f_warm, array_name="real_times")
    user_times_warm = getVals(f_warm, array_name="user_times")
    sys_times_warm = getVals(f_warm, array_name="sys_times")
    memory_mb_warm = getVals(f_warm, array_name="memory_mb")

    real_times_cold = getVals(f_cold, array_name="real_times")
    user_times_cold = getVals(f_cold, array_name="user_times")
    sys_times_cold = getVals(f_cold, array_name="sys_times")
    memory_mb_cold = getVals(f_cold, array_name="memory_mb")

    wait_t_warm = get_wait_t(user_times_warm, sys_times_warm, real_times_warm)
    wait_t_cold = get_wait_t(user_times_cold, sys_times_cold, real_times_cold)

    cpu_warm = get_cpu(user_times_warm, sys_times_warm, real_times_warm)
    cpu_cold = get_cpu(user_times_cold, sys_times_cold, real_times_cold)

    print("COLD")
    print("Wait time (I/O) (s): ", np.average(wait_t_cold))
    print("CPU (%): ", cpu_cold)
    print("Memory (MB):  ", memory_mb_cold)


    print("WARM")
    print("Wait time (I/O) (s): ", np.average(wait_t_warm))
    print("CPU (%): ", np.average(cpu_warm))
    print("Memory (MB): ", np.average(memory_mb_warm))



if __name__ == "__main__":
    main()