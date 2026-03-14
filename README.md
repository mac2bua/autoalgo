# autoalgo

Autonomous algorithm optimization — an experiment to have the LLM do its own research on algorithm performance.

## Overview

This system autonomously optimizes algorithm implementations for runtime performance. Each experiment runs for a **fixed time budget of 5 minutes**. The goal is to achieve the lowest total execution time across a fixed benchmark suite.

## Setup

To set up a new experiment:

1. **Agree on a run tag**: propose a tag based on today's date (e.g., `mar5`). The branch `autoalgo/<tag>` must not already exist — this is a fresh run.
2. **Create the branch**: `git checkout -b autoalgo/<tag>` from current master.
3. **Read the in-scope files**:
   - `README.md` — this file.
   - `evaluate.py` — fixed evaluation harness, benchmark suite, timing code. Do not modify.
   - `algorithms.py` — the file you modify. Implement algorithm optimizations here.
4. **Verify benchmarks work**: Run `uv run evaluate.py` to ensure the benchmark suite works.
5. **Initialize results.tsv**: Create `results.tsv` with header row and baseline entry. Run `uv run evaluate.py` once to establish YOUR baseline on this hardware.
6. **Confirm and go**: Confirm setup looks good.

## Experimentation

Each experiment runs for a **fixed time budget of 5 minutes** (wall clock time for running experiments).

**What you CAN do:**
- Modify `algorithms.py` — this is the only file you edit. Everything is fair game: algorithm approach, data structures, caching strategies, loop optimizations, batching, etc.

**What you CANNOT do:**
- Modify `evaluate.py`. It is read-only. It contains the fixed benchmark suite and timing harness.
- Install new packages or add dependencies. You can only use what's already in `pyproject.toml`.
- Modify the benchmark inputs or expected outputs.

**The goal is simple: get the lowest total_time_ms.** Since the time budget is fixed, you don't need to worry about experiment time — it's always 5 minutes. Everything is fair game: change the algorithm, data structures, caching, precomputation, etc.

**Memory** is a soft constraint. Some increase is acceptable for meaningful time gains, but it should not blow up dramatically.

**Simplicity criterion**: All else being equal, simpler is better. A small improvement that adds ugly complexity is not worth it. Conversely, removing something and getting equal or better results is a great outcome — that's a simplification win.

**The first run**: Your very first run should always be to establish the baseline, so you will run the evaluation script as is.

## Output format

Once the script finishes it prints a summary like this:

```
---
total_time_ms:    1234.5
best_time_ms:     45.2
worst_time_ms:    89.1
avg_time_ms:      61.7
memory_mb:        128.4
benchmarks_run:   20
```

## Logging results

When an experiment is done, log it to `results.tsv` (tab-separated).

The TSV has a header row and 5 columns:

```
commit	total_time_ms	memory_mb	status	description
```

1. git commit hash (short, 7 chars)
2. total_time_ms achieved (e.g., 1234.567) — use 0.0 for crashes
3. peak memory in MB (e.g., 128.4) — use 0.0 for crashes
4. status: `keep`, `discard`, or `crash`
5. short text description of what this experiment tried

## The experiment loop

The experiment runs on a dedicated branch (e.g., `autoalgo/mar5`).

LOOP FOREVER:

1. Look at the git state: the current branch/commit we're on
2. Tune `algorithms.py` with an experimental idea
3. `git add algorithms.py && git commit -m "experiment: <description>"`
4. Run the experiment: `uv run evaluate.py > run.log 2>&1`
5. Read out the results: `grep "^total_time_ms:\|^memory_mb:" run.log`
6. If the grep output is empty, the run crashed. Run `tail -n 50 run.log` to read the stack trace.
7. Record the results in the TSV
8. If total_time_ms improved (lower), `git add results.tsv && git commit --amend --no-edit`
9. If total_time_ms is equal or worse, record the discard commit, then `git reset --hard <previous kept commit>`

**Timeout**: Each experiment should take ~5 minutes. If a run exceeds 15 minutes, kill it and treat it as a failure.

**Crashes**: If a run crashes, use your judgment. If it's something easy to fix, fix it. If the idea is fundamentally broken, skip it and move on.

**NEVER STOP**: Once the experiment loop has begun, do NOT pause to ask the human if you should continue. You are autonomous.
