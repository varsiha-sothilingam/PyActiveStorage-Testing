import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from matplotlib.lines import Line2D
import sys
sys.path.append("..") 
plt.rcParams['font.family'] = 'Arial'

import importlib.util
from pathlib import Path


def getVals(path, array_name="real_times"):
    """
    Load a Python file at 'path' as a module and return the specified array.
    
    Parameters:
        path (str): Path to the Python file
        array_name (str): Name of the array variable to import (default 'real_times')
    
    Returns:
        np.array: The requested array from the file
    """
    file_path = Path(path)
    spec = importlib.util.spec_from_file_location("module_from_file", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    return getattr(module, array_name)

# --- 1. INPUT YOUR INDIVIDUAL NP ARRAYS HERE ---
# (Replace these placeholders with your actual numpy arrays)

t1_Local   = getVals("Local_v_Active/Target1_Local_f_ch330a.pc19790301_bnl.nc_var_UM_m01s16i202_vn1106_slice_0_8_0_413_0_551_20260330_131924.py"      , "real_times") 
t1_Active  = getVals("Local_v_Active/Target1_Active_f_ch330a.pc19790301_bnl.nc_var_UM_m01s16i202_vn1106_slice_0_8_0_413_0_551_20260330_130305.py"     , "real_times")
t5_Local   = getVals("Local_v_Active/Target5_Local_f_ch330a.pc19790301_bnl.nc_var_UM_m01s16i202_vn1106_slice_0_14_0_707_0_942_20260330_134057.py"     , "real_times")  
t5_Active  = getVals("Local_v_Active/Target5_Active_f_ch330a.pc19790301_bnl.nc_var_UM_m01s16i202_vn1106_slice_0_14_0_707_0_942_20260330_135715.py"    , "real_times")  
t10_Local  = getVals("Local_v_Active/Target10_Local_f_ch330a.pc19790301_bnl.nc_var_UM_m01s16i202_vn1106_slice_0_18_0_891_0_1188_20260330_142336.py"   , "real_times")  
t10_Active = getVals("Local_v_Active/Target10_Active_f_ch330a.pc19790301_bnl.nc_var_UM_m01s16i202_vn1106_slice_0_18_0_891_0_1188_20260330_140024.py"  , "real_times") 
t25_Local  = getVals("Local_v_Active/Target25_Local_f_ch330a.pc19790301_bnl.nc_var_UM_m01s16i202_vn1106_slice_0_25_0_1209_0_1612_20260330_145609.py"  , "real_times")  
t25_Active = getVals("Local_v_Active/Target25_Active_f_ch330a.pc19790301_bnl.nc_var_UM_m01s16i202_vn1106_slice_0_25_0_1209_0_1612_20260330_165917.py" , "real_times")  
t50_Local  = getVals("Local_v_Active/Target50_Local_f_ch330a.pc19790301_bnl.nc_var_UM_m01s16i202_vn1106_slice_0_31_0_1525_0_2032_20260330_154812.py"  , "real_times")  
t50_Active = getVals("Local_v_Active/Target50_Active_f_ch330a.pc19790301_bnl.nc_var_UM_m01s16i202_vn1106_slice_0_31_0_1525_0_2032_20260330_165647.py" , "real_times")  
t75_Local  = getVals("Local_v_Active/Target75_Local_f_ch330a.pc19790301_bnl.nc_var_UM_m01s16i202_vn1106_slice_0_36_0_1753_0_2337_20260330_164934.py"  , "real_times")  
t75_Active = getVals("Local_v_Active/Target75_Active_f_ch330a.pc19790301_bnl.nc_var_UM_m01s16i202_vn1106_slice_0_36_0_1753_0_2337_20260330_165353.py" , "real_times")   

arr_L4_on,  arr_L4_off = np.array([7, 8, 9]),    np.array([12, 13, 14])

# --- 2. STRUCTURE INTO CUSTOM DATA ---
# Format: [ [Data_ON], [Data_OFF], "Label" ] -> Position Swapped per request
custom_data = [
    ((np.array([]), np.array([]), "")) ,
    (t1_Active  ,t1_Local   ,  "1%  "),
    (t5_Active  ,t5_Local   ,  "5%  "),
    (t10_Active ,t10_Local  ,  "10% "),
    (t25_Active ,t25_Local  ,  "25% "),
    (t50_Active ,t50_Local  ,  "50% "),
    (t75_Active ,t75_Local  ,  "75% "),
    (arr_L4_on, arr_L4_off, "100% ")
    ]

SHOW_VIOLINS = True 

def plot_dual_hybrid_row(ax, y_pos, data_on, data_off, show_violins=SHOW_VIOLINS):
    # Swapped order: ON is first (lower), OFF is second (higher)
    colors = ["#fd5400", "#939393"] 
    datasets = [data_on, data_off]
    
    if len(data_on) == 0 or len(data_off) == 0:
        return  # skip empty row

    for i, data in enumerate(datasets):
        color = colors[i]
        # Offset 0.1 for the first element (ON), 0.5 for the second (OFF)
        offset = 0.1 if i == 0 else 0.5
        
        mean = np.mean(data)
        std = np.std(data)
        
        if show_violins:
            kde = stats.gaussian_kde(data)
            x_range = np.linspace(min(data) - std, max(data) + std, 100)
            kde_values = (kde(x_range) / max(kde(x_range))) * 0.35 
            
            ax.fill_between(x_range, y_pos + offset, y_pos + offset + kde_values, alpha=0.2, color=color)
            ax.plot(x_range, y_pos + offset + kde_values, color=color, lw=1)

        # Plot Error Bars
        ax.errorbar(mean, y_pos + offset, xerr=std, fmt='o', color=color, 
                    elinewidth=2.5, capsize=4, markersize=8, zorder=3)

# --- Plotting Logic ---
fig, ax = plt.subplots(figsize=(10, 8))

y_ticks, y_labels = [], []

for i, (d_on, d_off, label) in enumerate(custom_data):
    if i == 0:
        y_pos = (len(custom_data) - i) * 1.5 + 1.5  # extra 1.5 units for empty row
    else:
        y_pos = (len(custom_data) - i) * 1.5
    plot_dual_hybrid_row(ax, y_pos, d_on, d_off)
    
    y_ticks.append(y_pos + 0.3)
    y_labels.append(label)
    

    y_pos = (len(custom_data) - i) * 1.5
    # Pass ON then OFF
    plot_dual_hybrid_row(ax, y_pos, d_on, d_off)
    
    y_ticks.append(y_pos + 0.3)
    y_labels.append(label)
    
    if i < len(custom_data) - 1:
        ax.axhline(y_pos - 0.25, color="#bbbbbb", lw=1.5, linestyle=':')

# Styling
ax.set_yticks(y_ticks)
ax.set_yticklabels(y_labels, fontsize=12,ha='right')
ax.tick_params(axis='y', length=0, pad=20)
ax.set_xlabel('Execution Time (seconds)', fontsize=12)
ax.spines[['top', 'right', 'left']].set_visible(True)

# Legend (Updated to match the new order)
legend_elements = [
    Line2D([0], [0], color="#fd5400", marker='o', lw=2, label='Active Storage'),
    Line2D([0], [0], color='#939393', marker='o', lw=2, label='Local Storage ')
]
ax.legend(handles=legend_elements, loc='upper right', frameon=False, fontsize=12, bbox_to_anchor=(0.95, 0.96) )

# Bold first line
ax.text(
    0.01, 0.98,
    "Reduction time relative to slice size",
    fontsize=12,
    fontweight='bold',
    va='top', ha='left',
    linespacing=1.5,
    transform=ax.transAxes
)

# Normal subsequent lines
ax.text(
    0.01, 0.945,  # slightly lower to match spacing
    "File: ch330a.pc19790301-bnl.nc\n"
    "Variable: UM_m01s16i202_vn1106\n"
    "3400 Chunks, 17.96 GB",
    fontsize=12,
    fontweight='normal',
    va='top', ha='left',
    linespacing=1.5,
    transform=ax.transAxes
)



plt.tight_layout()
plt.savefig("tmp.pdf")