#!/usr/bin/env bash
set -euo pipefail

PY_VERSIONS=("3.10" "3.11" "3.12" "3.13" "3.14")

run_job () {
  local PY_VER=$1

  (
    echo "=== [macOS | Python $PY_VER] START ==="

    ENV_NAME="activestorage-${PY_VER}"

    conda activate activestorage
    # NOTE: Your macOS workflow does NOT run pytest
    # If you actually want tests, uncomment below:
    pytest -n 2 -m "not slow" \
      --ignore=tests/test_real_https.py \
      --ignore=tests/test_real_s3.py

    echo "=== [macOS | Python $PY_VER] DONE ==="
  ) &
}

# Launch all versions in parallel
for py in "${PY_VERSIONS[@]}"; do
  run_job "$py"
done

# Wait for all jobs to finish
wait

echo "🎉 All macOS jobs completed"
