# autoalgo

Autonomous algorithm optimization — an experiment to have the LLM do its own research on algorithm performance.

## Acknowledgements

This project is inspired by [Andrej Karpathy's autoresearch](https://github.com/karpathy/autoresearch), which pioneered the concept of using LLMs to autonomously optimize machine learning models. This project adapts the same approach to algorithm performance optimization.

## What is this?

This is a weekend project that demonstrates how to use an LLM (via GitHub Actions) to autonomously optimize algorithm implementations for runtime performance. The system:

1. Runs a fixed set of algorithm benchmarks
2. Tries out different algorithmic approaches
3. Keeps improvements, discards regressions
4. Runs automatically every hour

## Who is this for?

**This is NOT a user-facing tool.** You should NOT try to use this if you're looking for:
- A library to install
- A service to run your own experiments
- Support for running on your own repository

**This IS for you if you're:**
- Curious about autonomous LLM-driven development
- Interested in algorithm optimization techniques
- Want to understand how to set up autonomous experimentation loops

The original autoresearch repo was designed to run while the human sleeps — you could leave it running for 8 hours and wake up to ~70 experimental results. This project aims to do the same for algorithm performance.

## How does it work?

### The Git Branch Pattern

This project uses a dedicated branch (`autoalgo/mar14`) for autonomous experimentation. This is key to how it works:

- **Main branch (`main`)**: Stable, production code
- **Experiment branch (`autoalgo/<tag>`)**: Where autonomous experiments run

The GitHub Actions workflow:
1. Checks out the experiment branch
2. Runs experiments by modifying `algorithms.py`
3. Commits improvements back to the branch (using `git commit --amend`)
4. Never touches the `main` branch

**Why branches?** This ensures:
- Every experiment is tracked in git history
- You can see exactly what changed between runs
- Failed experiments are cleanly discarded
- The autonomous loop can run indefinitely without human intervention

### What changes between experiments?

- **Algorithms in `algorithms.py`**: Anything fair game
  - Different algorithm approaches (e.g., Kadane's vs brute force)
  - Data structures (hash maps, heaps, trees)
  - Caching/memoization strategies
  - Loop optimizations, batching, precomputation

### What stays fixed?

- **`evaluate.py`**: The benchmark suite and timing harness
- **Time budget**: ~5 minutes per experiment
- **Benchmark inputs**: Fixed seeds ensure reproducibility

## Setup (for the repo owner only)

If you want to set up your own version:

1. **Create an experiment branch**:
   ```bash
   git checkout -b autoalgo/mar15
   ```

2. **Establish your baseline**:
   ```bash
   uv sync
   uv run evaluate.py > run.log 2>&1
   ```

3. **Record the baseline** in `results.tsv`:
   ```
   commit	total_time_ms	memory_mb	status	description
   <commit_hash>	<time_from_log>	<memory_from_log>	keep	baseline
   ```

4. **Configure GitHub Secrets**:
   - Add `AUTOALGO_PAT` with a Personal Access Token (repo scope)

5. **Enable GitHub Actions** on your repository

6. **Push the branch**:
   ```bash
   git push -u origin autoalgo/mar15
   ```

That's it. The workflow will now run automatically every hour.

## Output format

Once the script finishes it prints a summary like this:

```
---
total_time_ms:    1234.5
memory_mb:        17.0
benchmarks_run:   10
```

## Logging results

Results are logged to `results.tsv` (tab-separated):

```
commit	total_time_ms	memory_mb	status	description
abc1234	1234.5	17.0	keep	Optimized quickselect with median-of-medians
def5678	1245.2	17.0	discard	Simplified LRU cache - slower
```

- `keep`: Improvement over previous best
- `discard`: No improvement or regression
- `crash`: Experiment failed

## Files

| File | Purpose |
|------|---------|
| `algorithms.py` | Algorithm implementations (MODIFY THIS for optimization) |
| `evaluate.py` | Fixed evaluation harness (DO NOT MODIFY) |
| `results.tsv` | Results tracking |
| `.env.example` | Template for credentials (not used by GitHub Actions) |

## Running locally

```bash
uv sync
uv run evaluate.py
```

## License

MIT License - see LICENSE file for details.
