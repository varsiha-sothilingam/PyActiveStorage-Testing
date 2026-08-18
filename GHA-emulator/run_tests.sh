#!/usr/bin/env bash
set -euo pipefail

PY_VERSIONS=("3.10" "3.11" "3.12" "3.13" "3.14")
LOG_DIR="logs"

mkdir -p "$LOG_DIR"

# Track PIDs and versions
PIDS_LIST=()
PY_FOR_PID=()
STATUS_KEYS=()
STATUS_VALUES=()

run_job () {
  local PY_VER=$1
  local LOG_FILE="$LOG_DIR/python-${PY_VER}.log"

  (
    set +e  # allow pytest to fail without killing subshell

    echo "=== [Python $PY_VER] START ==="
    echo "Log file: $LOG_FILE"

    source "$(conda info --base)/etc/profile.d/conda.sh"
    conda activate "activestorage-$PY_VER"

    echo "--- Python version ---"
    python -V

    echo "--- Running pytest ---"
    pytest -n 2 -m "not slow" /Users/dh935740@reading.ac.uk/PyActiveStorage/tests/ \
      --ignore=/Users/dh935740@reading.ac.uk/PyActiveStorage/tests/test_real_https.py \
      --ignore=/Users/dh935740@reading.ac.uk/PyActiveStorage/tests/test_real_s3.py

    EXIT_CODE=$?

    echo "=== [Python $PY_VER] EXIT CODE: $EXIT_CODE ==="
    exit $EXIT_CODE
  ) 2>&1 | tee "$LOG_FILE" &

  PIDS[$!]=$PY_VER
}

# Launch all jobs in parallel
for py in "${PY_VERSIONS[@]}"; do
  run_job "$py"
done

# Wait for all and collect results
FAIL=0

for pid in "${!PIDS[@]}"; do
  py=${PIDS[$pid]}

  if wait "$pid"; then
    STATUS[$py]="PASS"
  else
    STATUS[$py]="FAIL"
    FAIL=1
  fi
done

# Final summary
echo ""
echo "================ SUMMARY ================"
for py in "${PY_VERSIONS[@]}"; do
  printf "Python %-6s : %s\n" "$py" "${STATUS[$py]}"
done
echo "========================================="

if [[ $FAIL -ne 0 ]]; then
  echo "❌ One or more jobs failed"
  exit 1
else
  echo "🎉 All jobs passed"
fi