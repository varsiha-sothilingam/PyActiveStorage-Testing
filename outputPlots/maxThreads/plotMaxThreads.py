import json
import glob
import re
import numpy as np
import matplotlib.pyplot as plt


def extract_thread_count(filename):
    match = re.search(r"MT(\d+)", filename)
    return int(match.group(1)) if match else None


def load_hyperfine_times(path):
    """
    Extract per-run times from hyperfine JSON, filtering only successful runs (exit code == 0).
    """
    with open(path, "r") as f:
        data = json.load(f)

    results = data.get("results", [])
    valid_times = []

    for run in results:
        times = run.get("times", [])
        exit_codes = run.get("exit_codes", [])

        # Keep only successful runs
        for t, code in zip(times, exit_codes):
            if code == 0:
                valid_times.append(t)

    return valid_times


def main():
    files = glob.glob("/Users/dh935740@reading.ac.uk/testing_PyActiveStorage/tests_Varsiha/output/MaxThreadsTest/ESFG-NG/results-MT*.json")

    thread_data = {}

    for file in files:
        threads = extract_thread_count(file)
        if threads is None:
            continue

        times = load_hyperfine_times(file)
        if len(times) == 0:
            continue

        thread_data[threads] = np.array(times)

    if not thread_data:
        print("No valid data found.")
        return

    # Sort by thread count
    thread_counts = sorted(thread_data.keys())
    data = [thread_data[t] for t in thread_counts]

    # Stats
    for t in thread_counts:
        arr = thread_data[t]
        print(
            f"MT{t}: mean={np.mean(arr):.4f}, std={np.std(arr):.4f}, max={np.max(arr):.4f}"
        )

    # Plot boxplot
    plt.figure(figsize=(10, 6))
    plt.boxplot(data, labels=[str(t) for t in thread_counts])

    plt.xlabel("Max Threads")
    plt.ylabel("Execution Time (s)")
    plt.title("Hyperfine Benchmark Results by Max Threads")
    plt.grid(True, axis="y", linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
