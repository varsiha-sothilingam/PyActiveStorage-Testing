#!/usr/bin/env bash
set -euo pipefail
export PYTHONWARNINGS="ignore:Unverified HTTPS request"
# Configuration
PY_VERSIONS=("3.10" "3.11" "3.12" "3.13" "3.14")
LOG_DIR="logs-StressTest-MT60"

mkdir -p "$LOG_DIR"

# We use an associative array to map PIDs to Python versions
# Requires Bash 4.0+
PIDS_LIST=()
PY_FOR_PID=()
STATUS_KEYS=()
STATUS_VALUES=()

run_job() {
  local PY_VER=$1
  local LOG_FILE="$LOG_DIR/python-${PY_VER}.log"
  local ENV_NAME="activestorage-${PY_VER}"

  # Subshell runs in the background
  (
    # Redirect all output for this subshell to the log file immediately
    exec > "$LOG_FILE" 2>&1
    
    echo "=== [Python $PY_VER] Execution Started ==="
    
    # Initialize conda for this subshell
    CONDA_BASE=$(conda info --base)
    source "$CONDA_BASE/etc/profile.d/conda.sh"
    
    if ! conda activate "$ENV_NAME"; then
      echo "ERROR: Could not activate environment $ENV_NAME"
      exit 1
    fi

    echo "Using Python: $(python -V)"
    echo "--- Running Test ---"
    
    # Run your script
    python scripts/test_debug_https.py
    
    EXIT_CODE=$?
    echo "=== [Python $PY_VER] Finished with code: $EXIT_CODE ==="
    exit $EXIT_CODE
  ) &

  # Store the background process ID
  PIDS[$!]=$PY_VER
  echo "🚀 Launched Python $PY_VER (PID: $!)"
}

# 1. Launch all jobs
echo "Starting concurrent tests in $LOG_DIR..."
for py in "${PY_VERSIONS[@]}"; do
  run_job "$py"
done

# 2. Wait and collect results
declare -A STATUS
FAIL_COUNT=0

echo "Waiting for jobs to complete..."
for pid in "${!PIDS[@]}"; do
  py=${PIDS[$pid]}
  
  # wait returns the exit code of the process
  if wait "$pid"; then
    STATUS["$py"]="✅ PASS"
  else
    STATUS["$py"]="❌ FAIL"
    ((FAIL_COUNT++))
  fi
done

# 3. Final summary
echo -e "\n================ SUMMARY ================"
for py in "${PY_VERSIONS[@]}"; do
  printf "Python %-6s : %s\n" "$py" "${STATUS[$py]}"
done
echo "========================================="

if [[ $FAIL_COUNT -ne 0 ]]; then
  echo "Result: $FAIL_COUNT job(s) failed. Check $LOG_DIR for details."
  exit 1
else
  echo "Result: All jobs passed successfully!"
  exit 0
fi