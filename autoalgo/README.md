# autoalgo

Autonomous algorithm optimization — an experiment to have the LLM do its own research on algorithm performance.

## Acknowledgements

This project is inspired by [Andrej Karpathy's autoresearch](https://github.com/karpathy/autoresearch), which pioneered the concept of using LLMs to autonomously optimize machine learning models. This project adapts the same approach to algorithm performance optimization.

## What is this?

This is a weekend project that demonstrates how to use an LLM (via Claude Code or similar) to autonomously optimize algorithm implementations for runtime performance. The system:

1. Runs a fixed set of algorithm benchmarks
2. Tries out different algorithmic approaches
3. Keeps improvements, discards regressions
4. Runs continuously until manually stopped

## How does it work?

### The Experiment Loop

1. **Setup**: Create an experiment branch (e.g., `autoalgo/mar15`)
2. **Baseline**: Run the evaluation once to establish your baseline
3. **Loop forever** (while you're away sleeping or working on other things):
   - Modify `algorithms.py` with a new experimental idea
   - Run `uv run evaluate.py`
   - If the metric improved → keep the change
   - If the metric got worse → discard the change
   - Repeat

Each experiment takes ~5 minutes. If you leave it running for 8 hours, you can get ~80 experimental results by morning.

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

## Who is this for?

**This is NOT a user-facing tool.** You should NOT try to use this if you're looking for:
- A library to install
- A service to run your own experiments
- Support for running on your own repository

**This IS for you if you're:**
- Curious about autonomous LLM-driven development
- Interested in algorithm optimization techniques
- Want to understand how to set up autonomous experimentation loops

## Setup

To set up a new experiment:

1. **Create a branch** (the tag should be based on today's date):
   ```bash
   git checkout -b autoalgo/mar15
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

3. **Run the baseline** (this establishes your starting point):
   ```bash
   uv run evaluate.py > run.log 2>&1
   ```

4. **Record the baseline** in `results.tsv`:
   - Get the `total_time_ms` and `memory_mb` from `run.log`
   - Add a row with status `baseline`

5. **Kick off the loop**:
   Point Claude Code or another coding agent at `program.md` and let it run the loop.

## Files

| File | Purpose |
|------|---------|
| `algorithms.py` | Algorithm implementations (MODIFY THIS for optimization) |
| `evaluate.py` | Fixed evaluation harness (DO NOT MODIFY) |
| `results.tsv` | Results tracking |
| `program.md` | The autonomous experiment protocol |

## Running locally

```bash
uv sync
uv run evaluate.py
```

## License

MIT License - see LICENSE file for details.
