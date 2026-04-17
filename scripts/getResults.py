import re
import numpy as np
import argparse
import sys
import os
from datetime import datetime

def parse_log_to_data(input_path):
    """Parses the log file, converts Bytes to MB, and returns numpy arrays."""
    try:
        with open(input_path, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File '{input_path}' not found.")
        sys.exit(1)

    # Regex Extraction
    real = [float(x) for x in re.findall(r'([\d\.]+)\s+real', content)]
    user = [float(x) for x in re.findall(r'([\d\.]+)\s+user', content)]
    sys_t = [float(x) for x in re.findall(r'([\d\.]+)\s+sys', content)]
    
    # Extract memory and divide by 1024 * 1024 to convert Bytes -> MB
    raw_mem = re.findall(r'(\d+)\s+maximum resident set size', content)
    mem = [round(float(m) / (1024 * 1024), 2) for m in raw_mem]

    return {
        'real_times': np.array(real),
        'user_times': np.array(user),
        'sys_times':  np.array(sys_t),
        'memory_mb':  np.array(mem)
    }

def write_py_file(data, base_output_path, input_file):
    """Writes the converted MB data to a timestamped .py file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    name, ext = os.path.splitext(base_output_path)
    final_path = f"{name}_{timestamp}{ext}"

    output_content = (
        f'"""\nGenerated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n'
        f'Source Log: {os.path.basename(input_file)}\n"""\n\n'
        "import numpy as np\n\n"
        f"meta_info = 'Source: {input_file}\\nDate: {timestamp}'\n"
        f"real_times = np.array({data['real_times'].tolist()})\n"
        f"user_times = np.array({data['user_times'].tolist()})\n"
        f"sys_times  = np.array({data['sys_times'].tolist()})\n"
        f"memory_mb  = np.array({data['memory_mb'].tolist()})\n"
    )
    
    with open(final_path, 'w') as f:
        f.write(output_content)
    
    print(f"Successfully saved converted data to: {final_path}")
    return final_path

def print_stats(data):
    """Calculates and prints Mean and Std using the converted MB values."""
    wait_times = data['real_times'] - (data['user_times'] + data['sys_times'])
    cpu_util = np.divide((data['user_times'] + data['sys_times']), data['real_times'], 
                         out=np.zeros_like(data['real_times']), where=data['real_times']!=0) * 100

    metrics = [
        ("Real Time", data['real_times'], "s"),
        ("User Time", data['user_times'], "s"),
        ("Sys Time",  data['sys_times'],  "s"),
        ("Wait Time", wait_times,        "s"),
        ("Memory",    data['memory_mb'],  "MB"),
        ("CPU Util",  cpu_util,          "%")
    ]

    print(f"\n{'METRIC':<15} | {'MEAN':>12} | {'STD DEV':>12} | {'UNIT'}")
    print("-" * 55)
    for name, arr, unit in metrics:
        if len(arr) > 0:
            print(f"{name:<15} | {np.mean(arr):>12.4f} | {np.std(arr):>12.4f} | {unit}")
    print("-" * 55)

    # --- NEW: LaTeX Table Generation ---
    print("\n# LaTeX Table Code:")
    print("\\begin{table}[h!]")
    print("    \\centering")
    print("    \\begin{tabular}{ccc}")
    print("        \\hline")
    print("        \\textbf{Results} & Test 1               & Test 2               \\\\ \\hline")
    
    for name, arr, unit in metrics:
        if len(arr) > 0:
            avg = np.mean(arr)
            std = np.std(arr)
            # LaTeX uses \% for the percent symbol to avoid comments
            display_unit = unit.replace("%", "\\%")
            
            # Printing the same values for both columns to match your 3-column format
            print(f"        {name} [{display_unit}]    & {avg:.3f} $\\pm$ {std:.3f} & {avg:.3f} $\\pm$ {std:.3f} \\\\")
    
    print("        \\hline")
    print("    \\end{tabular}")
    print("    \\caption{Variables compared from the \\texttt{ch330a.pc19790301-bnl.nc} file, for a maximum number of threads of 100, method applied is \\texttt{min} and the data file is retrieved from the \\texttt{s3} object store.}")
    print("    \\label{tab:ResultsTest1}")
    print("\\end{table}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Bytes to MB and save to .py.")
    parser.add_argument("-i", "--input", required=True, help="Path to raw log.output")
    parser.add_argument("-o", "--output", default="processed_data.py", help="Output .py filename")
    
    args = parser.parse_args()

    performance_data = parse_log_to_data(args.input)
    saved_at = write_py_file(performance_data, args.output, args.input)
    print_stats(performance_data)