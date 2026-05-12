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
    file_path = Path(path)
    if not file_path.exists():
        return np.array([])
    spec = importlib.util.spec_from_file_location("module_from_file", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, array_name)

def calculate_stats(data_eth, data_wifi):
    """Calculates statistics comparing Ethernet (on) and WiFi (off)."""
    if len(data_eth) == 0 or len(data_wifi) == 0:
        return None
    m_eth, s_eth = np.mean(data_eth), np.std(data_eth)
    m_wifi, s_wifi = np.mean(data_wifi), np.std(data_wifi)
    ratio = m_wifi / m_eth # How much slower is WiFi?
    ratio_std = ratio * np.sqrt((s_wifi/m_wifi)**2 + (s_eth/m_eth)**2)
    return {
        "m1": m_eth, "s1": s_eth,
        "m2": m_wifi, "s2": s_wifi,
        "ratio": ratio, "ratio_std": ratio_std
    }

def plot_network_row(ax, y_pos, data_eth, data_wifi):
    """Plots Ethernet vs WiFi distributions."""
    colors = ["#004e92", "#fd5400"] # Blue for Eth, Orange for WiFi
    datasets = [data_eth, data_wifi]
    
    for i, data in enumerate(datasets):
        if len(data) == 0: continue
        color = colors[i]
        offset = 0.1 if i == 0 else 0.5
        
        mean, std = np.mean(data), np.std(data)
        kde = stats.gaussian_kde(data)
        x_range = np.linspace(min(data) - std, max(data) + std, 100)
        kde_values = (kde(x_range) / max(kde(x_range))) * 0.35 
        
        ax.fill_between(x_range, y_pos + offset, y_pos + offset + kde_values, alpha=0.2, color=color)
        ax.plot(x_range, y_pos + offset + kde_values, color=color, lw=1)
        ax.errorbar(mean, y_pos + offset, xerr=std, fmt='o', color=color, 
                    elinewidth=2.5, capsize=4, markersize=8, zorder=3)

# --- PRIMARY PLOTTING FUNCTION ---

def generate_network_comparison_plot(custom_data, meta_text, save_path):
    fig, ax = plt.subplots(figsize=(12, 8))
    y_ticks, y_labels = [], []

    for i, (d_eth, d_wifi, label) in enumerate(custom_data):
        y_pos = i * ROW_SPACING
        plot_network_row(ax, y_pos, d_eth, d_wifi)
        
        y_ticks.append(y_pos + 0.3)
        y_labels.append(label)

        if i < len(custom_data) - 1:
            ax.axhline(y_pos + 1.15, color="#bbbbbb", lw=1, linestyle=':')

        s = calculate_stats(d_eth, d_wifi)
        
        if s:
            labels_text = "Ethernet:\nWiFi:\nRatio:"
            values_text = (
                f"{s['m1']:>7.2f} ± {s['s1']:>5.2f}\n"
                f"{s['m2']:>7.2f} ± {s['s2']:>5.2f}\n"
                f"{s['ratio']:>7.2f} ± {s['ratio_std']:>5.2f}"
            )
            ax.text(0.835, y_pos + 0.3, labels_text, transform=ax.get_yaxis_transform(),
                    fontsize=11, va='center', ha='right')
            ax.text(0.84, y_pos + 0.3, values_text, transform=ax.get_yaxis_transform(),
                    fontsize=11, va='center', ha='left', family='monospace')
        print("CHECK vals",label, values_text)

    # Formatting - Log scale is usually best for network variability
    ax.set_xscale('symlog', linthresh=10)
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_labels, fontsize=12)
    ax.set_xlabel('Execution Time (seconds)', fontsize=12)
    ax.set_ylabel('Target File Size (%)', fontsize=12)
    ax.set_ylim(-0.5, (len(custom_data) * ROW_SPACING) + 0.6)
    ax.set_xlim(0, 200) # Linear scale as per your request
    
    ax.text(0.01, 0.98, "Network Impact on Active Storage Execution Time", fontweight='bold', transform=ax.transAxes, fontsize=12, va='top')
    ax.text(0.01, 0.945, meta_text, transform=ax.transAxes, fontsize=11, va='top')
    
    legend_el = [Line2D([0], [0], color="#004e92", marker='o', lw=2, label='Ethernet (Active)'),
                 Line2D([0], [0], color='#fd5400', marker='o', lw=2, label='WiFi (Active)')]
    ax.legend(handles=legend_el, loc='upper right', frameon=False, bbox_to_anchor=(0.95, 0.98))

    plt.tight_layout()
    plt.savefig(save_path)

# --- MAIN EXECUTION ---

def main():

    # Define the two separate directories
    base_wifi = "../output/UoREduroam/"
    base_eth = "../output/Local_v_Active/f_ch330a.pc19790301-def_64Chunk/"

    file_registry = [
        ("Target1_Active_f_ch330a.pc19790301-def.nc_var_UM_m01s16i202_vn1106_slice_0_8_0_413_0_551_20260407_133856.py"      , "test_s3_Target1-Active-UoR_f_ch330a.pc19790301-def.nc_var_UM_m01s16i202_vn1106_slice_0_8_0_413_0_551_20260420_110630.py"     , "1%"),
        ("Target5_Active_f_ch330a.pc19790301-def.nc_var_UM_m01s16i202_vn1106_slice_0_14_0_707_0_942_20260407_134641.py"     , "test_s3_Target5-Active-UoR_f_ch330a.pc19790301-def.nc_var_UM_m01s16i202_vn1106_slice_0_14_0_707_0_942_20260420_110422.py"    , "5"),
        ("Target10_Active_f_ch330a.pc19790301-def.nc_var_UM_m01s16i202_vn1106_slice_0_18_0_891_0_1188_20260407_134816.py"   , "test_s3_Target10-Active-UoR_f_ch330a.pc19790301-def.nc_var_UM_m01s16i202_vn1106_slice_0_18_0_891_0_1188_20260420_110224.py"  , "10%"),
        ("Target25_Active_f_ch330a.pc19790301-def.nc_var_UM_m01s16i202_vn1106_slice_0_25_0_1209_0_1612_20260407_140511.py"  , "test_s3_Target25-Active-UoR_f_ch330a.pc19790301-def.nc_var_UM_m01s16i202_vn1106_slice_0_25_0_1209_0_1612_20260420_105830.py" , "25%"),
        ("Target50_Active_f_ch330a.pc19790301-def.nc_var_UM_m01s16i202_vn1106_slice_0_31_0_1525_0_2032_20260407_142644.py"  , "test_s3_Target50-Active-UoR_f_ch330a.pc19790301-def.nc_var_UM_m01s16i202_vn1106_slice_0_31_0_1525_0_2032_20260420_105502.py" , "50%"),
        ("Target75_Active_f_ch330a.pc19790301-def.nc_var_UM_m01s16i202_vn1106_slice_0_36_0_1753_0_2337_20260407_142850.py"  , "test_s3_Target75-Active-UoR_f_ch330a.pc19790301-def.nc_var_UM_m01s16i202_vn1106_slice_0_36_0_1753_0_2337_20260420_105233.py" , "75%"),
        ("Target100_Active_f_ch330a.pc19790301-def.nc_var_UM_m01s16i202_vn1106_slice_0_40_0_1920_0_2560_20260407_151811.py" , "test_s3_Target100-Active-UoR_f_ch330a.pc19790301-def.nc_var_UM_m01s16i202_vn1106_slice_0_40_0_1920_0_2560_20260420_104428.py", "100%")
    ]


    # Use both bases in the list comprehension
    custom_data = [
        (getVals(f"{base_eth}{eth}"), getVals(f"{base_wifi}{wifi}"), lbl) 
        for eth, wifi, lbl in file_registry
    ]
    meta_label = (
        "File: ch330a.pc19790301-def.nc\n"
        "Variable: UM_m01s16i202_vn1106\n"
        "64 Chunks, 17.81 GB"
    )

    generate_network_comparison_plot(custom_data, meta_label, "Network_Active_Comparison.pdf")

if __name__ == "__main__":
    main()
