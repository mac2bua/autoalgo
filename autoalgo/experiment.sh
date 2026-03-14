#!/bin/bash
# Helper script to run a single experiment

set -e

cd "$(dirname "$0")"

if [ ! -f "results.tsv" ]; then
    echo "ERROR: results.tsv not found. Run manually first to establish baseline."
    exit 1
fi

# Generate a short description from the commit message
COMMIT_MSG=$(git log -1 --pretty=%B | head -n 1)
DESCRIPTION="${COMMIT_MSG:0:100}"

echo "Running experiment: $DESCRIPTION"
echo "Branch: $(git rev-parse --abbrev-ref HEAD)"

# Run and capture output
uv run evaluate.py > run.log 2>&1
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo "=== Results ==="
    grep "^total_time_ms:\|^memory_mb:" run.log
    echo ""
    echo "=== To log this experiment: ==="
    echo "1. Get the total_time_ms from above"
    echo "2. Get peak memory from run.log"
    echo "3. Update results.tsv with the commit hash and details"
else
    echo "CRASHED! See run.log for details."
    tail -n 50 run.log
    exit 1
fi
