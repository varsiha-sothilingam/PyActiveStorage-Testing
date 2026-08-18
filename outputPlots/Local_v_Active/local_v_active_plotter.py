import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.lines import Line2D
from scipy import stats
from pathlib import Path
import importlib.util

# --- GLOBAL CONFIGURATION ---
plt.rcParams['font.family'] = 'Arial'
ROW_SPACING = 1.5

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
    colors = ["#028F00", "#939393"] 
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

def generate_execution_plot(custom_data,meta_text, save_path):
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
    ax.set_xlim(10, 2700)
    ax.xaxis.set_major_locator(ticker.FixedLocator([10, 20, 30, 100, 1000, 2700]))
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_labels, fontsize=12)
    ax.set_xlabel('Execution Time (seconds)', fontsize=12)
    ax.set_ylabel('Target (%)', fontsize=12)
    
    # Header & Legend
    ax.text(0.01, 0.98, "Reduction execution time relative to slice size", fontweight='bold', transform=ax.transAxes, fontsize=12, va='top')
    ax.text(0.01, 0.945, meta_text, transform=ax.transAxes, fontsize=12, va='top', linespacing=1.5)
    
    legend_el = [Line2D([0], [0], color="#028F00", marker='o', lw=2, label='Active Storage'),
                 Line2D([0], [0], color='#939393', marker='o', lw=2, label='Local Storage ')]
    ax.legend(handles=legend_el, loc='upper right',fontsize=12, frameon=False, bbox_to_anchor=(0.95, 0.98))

    plt.tight_layout()
    plt.savefig(save_path)
    return summary_stats


def generate_execution_plot_64chunk(custom_data, meta_64,save_path):
    # Note: Use linear scale and specific x-limits for this version
    fig, ax = plt.subplots(figsize=(12, 8))
    y_ticks, y_labels = [], []

    for i, (d_on, d_off, label) in enumerate(custom_data):
        # Skip empty placeholder if index 0 is empty
        if len(d_on) == 0: continue
        
        y_pos = i * ROW_SPACING
        plot_dual_hybrid_row(ax, y_pos, d_on, d_off)
        
        y_ticks.append(y_pos + 0.3)
        y_labels.append(label)

        if i < len(custom_data) - 1:
            ax.axhline(y_pos + 1.15, color="#bbbbbb", lw=1.5, linestyle=':')

        summary_stats = {"on_means": [], "on_stds": [], "off_means": [], "off_stds": []}

        # Stats Text using the helper
        s = calculate_stats(d_on, d_off)
        #print(label, len(d_on), len(d_off))
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

            #print(f"\nLabel: {label}")
            #print(f"  Active: {s['mean_on']:.2f} ± {s['std_on']:.2f}")
            #print(f"  Local : {s['mean_off']:.2f} ± {s['std_off']:.2f}")
            #print(f"  Ratio : {s['ratio']:.2f} ± {s['ratio_std']:.2f}")

            ax.text(0.835, y_pos + 0.3, labels_text, transform=ax.get_yaxis_transform(),
                    fontsize=12, va='center', ha='right')
            ax.text(0.84, y_pos + 0.3, values_text, transform=ax.get_yaxis_transform(),
                    fontsize=12, va='center', ha='left', family='monospace')

    # Specific limits for the 64-chunk plot
    ax.set_ylim(-0.5, (len(custom_data) * ROW_SPACING) + 0.6)
    ax.set_xlim(0, 50) # Linear scale as per your request
    
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_labels, fontsize=12)
    ax.set_xlabel('Execution Time (seconds)', fontsize=12)
    ax.set_ylabel('Target (%)', fontsize=12)
    
    # Header 
    ax.text(0.01, 0.98, "Reduction execution time relative to slice size", 
            fontweight='bold', transform=ax.transAxes, fontsize=12, va='top')
    ax.text(0.01, 0.945, meta_64, transform=ax.transAxes, 
            fontsize=12, va='top', linespacing=1.5)
    
    # Legend - Adjusted upward slightly (1.02)
    legend_el = [Line2D([0], [0], color="#028F00", marker='o', lw=2, label='Active Storage'),
                 Line2D([0], [0], color='#939393', marker='o', lw=2, label='Local Storage ')]
    ax.legend(handles=legend_el, loc='upper right', frameon=False, fontsize=12,  
              bbox_to_anchor=(0.95, 1.0))

    plt.tight_layout()
    plt.savefig(save_path)
    return summary_stats


def generate_ratio_plot(custom_data, meta_text, upper_xlim, save_path):
    fig, ax = plt.subplots(figsize=(10, 8))
    
    labels, ratios, errors = [], [], []
    for d_on, d_off, lbl in custom_data:
        s = calculate_stats(d_on, d_off)
        if s:
            labels.append(lbl)
            ratios.append(s['ratio'])
            errors.append(s['ratio_std'])

    y_pos = np.arange(len(labels)) * ROW_SPACING
    eb = ax.errorbar(ratios, y_pos, xerr=errors, fmt='o', color="#0019da", elinewidth=2, capsize=5, markersize=8)

    for i, (ratio, err) in enumerate(zip(ratios, errors)):
        ax.text(ratio-0.3, y_pos[i]-0.4, f"{ratio:.2f} ± {err:.2f}", fontsize=10, color="#062568", ha='left')

    for y in y_pos[:-1]:
        ax.axhline(y + (ROW_SPACING/2), color="#eeeeee", lw=1, zorder=0)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels)
    ax.set_ylim(y_pos[0] - 1, y_pos[-1] + 2.5)
    ax.set_xlim(-1, upper_xlim)
    ax.set_xlabel("Execution Time Ratio (Local / Active)")
    ax.set_ylabel('Target (%)', fontsize=12)
    
    
    ax.text(0.01, 0.98, "Execution Time Ratio (Local/Active) relative to Slice Size", fontweight='bold', transform=ax.transAxes, fontsize=12, va='top')
    ax.text(0.01, 0.945, meta_text, transform=ax.transAxes, fontsize=12, va='top', linespacing=1.5)
    ax.legend(handles=[eb], labels=['Local/Active Ratio'], loc='upper right', fontsize=12, frameon=False, bbox_to_anchor=(0.98, 0.96))

    plt.tight_layout()
    plt.savefig(save_path)


def generate_ratio_chunk_comparison_plot(ratio_vals, meta_text, upper_xlim,  save_path, myColor="#062568", myTitle = "Execution Time Ratio (3400 Chunk/ 64 Chunk) relative to Slice Size"):
    fig, ax = plt.subplots(figsize=(10, 8))
    
    labels = ["1", "5", "10", "25", "50", "75"]
    ratios = ratio_vals[0]
    errors = ratio_vals[1]

    y_pos = np.arange(len(labels)) * ROW_SPACING
    eb = ax.errorbar(ratios, y_pos, xerr=errors, fmt='o', color=myColor, elinewidth=2, capsize=5, markersize=8)

    for i, (ratio, err) in enumerate(zip(ratios, errors)):
        ax.text(ratio-0.3, y_pos[i]-0.4, f"{ratio:.2f} ± {err:.2f}", fontsize=10,  ha='left', color=myColor)

    for y in y_pos[:-1]:
        ax.axhline(y + (ROW_SPACING/2), color="#eeeeee", lw=1, zorder=0)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels)
    ax.set_ylim(y_pos[0] - 1, y_pos[-1] + 2.5)
    ax.set_xlim(-1, upper_xlim)
    ax.set_xlabel("Execution Time Ratio")
    ax.set_ylabel('Target (%)', fontsize=12)
    
    ax.text(0.01, 0.98, myTitle, fontweight='bold', transform=ax.transAxes, fontsize=12, va='top')
    ax.text(0.01, 0.945, meta_text, transform=ax.transAxes, fontsize=12, va='top', linespacing=1.5)
    ax.legend(handles=[eb], labels=['Ratio'], loc='upper right', fontsize=12, frameon=False, bbox_to_anchor=(0.98, 0.96))

    plt.tight_layout()
    plt.savefig(save_path)


# --- MAIN EXECUTION ---

def main():

    # --- 3400 Chunk: Local v Active  ---
    base = "../output/Local_v_Active/f_ch330a.pc19790301-bnl_3400Chunk/"
    
    file_registry = [
        ("Target1_Active_f_ch330a.pc19790301_bnl.nc_var_UM_m01s16i202_vn1106_slice_0_8_0_413_0_551_20260330_130305.py"     , "Target1_Local_f_ch330a.pc19790301_bnl.nc_var_UM_m01s16i202_vn1106_slice_0_8_0_413_0_551_20260330_131924.py", "1"),
        ("Target5_Active_f_ch330a.pc19790301_bnl.nc_var_UM_m01s16i202_vn1106_slice_0_14_0_707_0_942_20260330_135715.py"    , "Target5_Local_f_ch330a.pc19790301_bnl.nc_var_UM_m01s16i202_vn1106_slice_0_14_0_707_0_942_20260330_134057.py","5"),
        ("Target10_Active_f_ch330a.pc19790301_bnl.nc_var_UM_m01s16i202_vn1106_slice_0_18_0_891_0_1188_20260330_140024.py"  , "Target10_Local_f_ch330a.pc19790301_bnl.nc_var_UM_m01s16i202_vn1106_slice_0_18_0_891_0_1188_20260330_142336.py","10"),
        ("Target25_Active_f_ch330a.pc19790301_bnl.nc_var_UM_m01s16i202_vn1106_slice_0_25_0_1209_0_1612_20260330_165917.py" , "Target25_Local_f_ch330a.pc19790301_bnl.nc_var_UM_m01s16i202_vn1106_slice_0_25_0_1209_0_1612_20260330_145609.py","25"),
        ("Target50_Active_f_ch330a.pc19790301_bnl.nc_var_UM_m01s16i202_vn1106_slice_0_31_0_1525_0_2032_20260330_165647.py" , "Target50_Local_f_ch330a.pc19790301_bnl.nc_var_UM_m01s16i202_vn1106_slice_0_31_0_1525_0_2032_20260330_154812.py","50"),
        ("Target75_Active_f_ch330a.pc19790301_bnl.nc_var_UM_m01s16i202_vn1106_slice_0_36_0_1753_0_2337_20260330_165353.py" , "Target75_Local_f_ch330a.pc19790301_bnl.nc_var_UM_m01s16i202_vn1106_slice_0_36_0_1753_0_2337_20260330_164934.py","75")
    ]

    custom_data = [(getVals(f"{base}{act}"), getVals(f"{base}{loc}"), lbl) for act, loc, lbl in file_registry]
    custom_data.append((np.array([1, 2, 3]), np.array([1, 2, 3]), "100"))

    meta_label = (
        "File: ch330a.pc19790301-bnl.nc\n"
        "Variable: UM_m01s16i202_vn1106\n"
        "3400 Chunks, 17.96 GB"
    )

    stats_3400 = generate_execution_plot(custom_data, meta_label, "ExecutionTime_Local_v_Active_3400Chunk.pdf")
    generate_ratio_plot(custom_data, meta_label, 45, "Ratio_Analysis_Local_v_Active_3400Chunk.pdf")

    #plt.show()
    # --- 64 Chunk: Local v Active  ---
    base_coarse = "../output/Local_v_Active/f_ch330a.pc19790301-def_64Chunk/"

    file_registry_coarse = [
        ("Target1_Active_f_ch330a.pc19790301-def.nc_var_UM_m01s16i202_vn1106_slice_0_8_0_413_0_551_20260407_133856.py"     , "Target1_Local_f_ch330a.pc19790301-def.nc_var_UM_m01s16i202_vn1106_slice_0_8_0_413_0_551_20260407_134059.py"     , "1"),
        ("Target5_Active_f_ch330a.pc19790301-def.nc_var_UM_m01s16i202_vn1106_slice_0_14_0_707_0_942_20260407_134641.py"    , "Target5_Local_f_ch330a.pc19790301-def.nc_var_UM_m01s16i202_vn1106_slice_0_14_0_707_0_942_20260407_134423.py"    , "5"),
        ("Target10_Active_f_ch330a.pc19790301-def.nc_var_UM_m01s16i202_vn1106_slice_0_18_0_891_0_1188_20260407_134816.py"  , "Target10_Local_f_ch330a.pc19790301-def.nc_var_UM_m01s16i202_vn1106_slice_0_18_0_891_0_1188_20260407_135427.py"  ,"10"),
        ("Target25_Active_f_ch330a.pc19790301-def.nc_var_UM_m01s16i202_vn1106_slice_0_25_0_1209_0_1612_20260407_140511.py" , "Target25_Local_f_ch330a.pc19790301-def.nc_var_UM_m01s16i202_vn1106_slice_0_25_0_1209_0_1612_20260407_141132.py" ,"25"),
        ("Target50_Active_f_ch330a.pc19790301-def.nc_var_UM_m01s16i202_vn1106_slice_0_31_0_1525_0_2032_20260407_142644.py" , "Target50_Local_f_ch330a.pc19790301-def.nc_var_UM_m01s16i202_vn1106_slice_0_31_0_1525_0_2032_20260407_142408.py" ,"50"),
        ("Target75_Active_f_ch330a.pc19790301-def.nc_var_UM_m01s16i202_vn1106_slice_0_36_0_1753_0_2337_20260407_142850.py" , "Target75_Local_f_ch330a.pc19790301-def.nc_var_UM_m01s16i202_vn1106_slice_0_36_0_1753_0_2337_20260407_144115.py" ,"75"),
        ("Target100_Active_f_ch330a.pc19790301-def.nc_var_UM_m01s16i202_vn1106_slice_0_40_0_1920_0_2560_20260407_151811.py", "Target100_Local_f_ch330a.pc19790301-def.nc_var_UM_m01s16i202_vn1106_slice_0_40_0_1920_0_2560_20260407_150224.py","100")
    ]
    custom_data_coarse = [(getVals(f"{base_coarse}{act}"), getVals(f"{base_coarse}{loc}"), lbl) for act, loc, lbl in file_registry_coarse]
    meta_label_coarse = (
        "File: ch330a.pc19790301-def.nc\n"
        "Variable: UM_m01s16i202_vn1106\n"
        "64 Chunks, 17.81 GB"
    )
    
    generate_ratio_plot(custom_data_coarse, meta_label_coarse, 10, "Ratio_Analysis_Local_v_Active_64Chunk.pdf")
    stats_64 = generate_execution_plot_64chunk(custom_data_coarse, meta_label_coarse,"ExecutionTime_Local_v_Active_64Chunk.pdf")

    #    --- AUTOMATED: Active Storage 3400 v 64 ---
    # We use the 'on' values (Active) from both sets
    # Note: We slice [:6] to ensure both have the same length if 3400 is missing the "100" target
    ratio_values_active = calculate_array_ratios(
        stats_3400["on_means"][:6], stats_3400["on_stds"][:6], 
        stats_64["on_means"][:6],   stats_64["on_stds"][:6]
    )
    
    generate_ratio_chunk_comparison_plot(
        ratio_values_active, "Comparing Active Storage", 5, 
        "ActiveChunkingRatio.pdf", myColor="#028F00"
    )

    # --- AUTOMATED: Local Storage 3400 v 64 ---
    # We use the 'off' values (Local) from both sets
    ratio_values_local = calculate_array_ratios(
        stats_3400["off_means"][:6], stats_3400["off_stds"][:6], 
        stats_64["off_means"][:6],   stats_64["off_stds"][:6]
    )

    generate_ratio_chunk_comparison_plot(
        ratio_values_local, "Comparing Local Storage", 25, 
        "LocalChunkingRatio.pdf", myColor="#028F00"
    )

if __name__ == "__main__":
    main()

