# autoalgo

> Autonomous algorithm optimization — an experiment to have the LLM do its own research on algorithm performance.

Inspired by [Andrej Karpathy's autoresearch](https://github.com/karpathy/autoresearch), this project applies the same autonomous research loop to algorithm performance optimization.

## Overview

This system autonomously optimizes algorithm implementations for runtime performance:

1. Runs a fixed set of algorithm benchmarks
2. Tries out different algorithmic approaches
3. Keeps improvements, discards regressions
4. Runs continuously until manually stopped

Each experiment takes ~5 minutes. Leave it running overnight and you can run ~12 experiments per hour.

## How It Works

### The Experiment Loop

1. **Setup**: Create an experiment branch (e.g., `autoalgo/mar15`)
2. **Baseline**: Run the evaluation once to establish your baseline
3. **Loop** (while you're away):
   - Modify `algorithms.py` with a new experimental idea
   - Run `uv run evaluate.py`
   - If the metric improved → keep the change
   - If the metric got worse → discard the change
   - Repeat

### What Changes

- **Algorithms in `algorithms.py`**: Anything fair game
  - Different algorithm approaches
  - Data structures (hash maps, heaps, trees)
  - Caching/memoization strategies
  - Loop optimizations, batching, precomputation

### What Stays Fixed

- **`evaluate.py`**: The benchmark suite and timing harness
- **Time budget**: ~5 minutes per experiment
- **Benchmark inputs**: Fixed seeds ensure reproducibility

## Running Unattended

To run the agent indefinitely without manual intervention, launch Claude Code with the dangerous mode flag:

```bash
# Ollama (author's setup)
ollama launch claude --model qwen3-coder-next:cloud -- --dangerously-skip-permissions

# Claude CLI
claude --dangerously-skip-permissions
```

**Note**: This grants the agent full permission to execute commands without approval. Only use in a dedicated project directory.

## Setup

```bash
# Create experiment branch
git checkout -b autoalgo/mar15

# Install dependencies
uv sync

# Run baseline
uv run evaluate.py > run.log 2>&1
```

Record the baseline in `results.tsv` and kick off the loop.

## Files

| File | Purpose |
|------|---------|
| `algorithms.py` | Algorithm implementations (MODIFY THIS) |
| `evaluate.py` | Fixed evaluation harness (DO NOT MODIFY) |
| `results.tsv` | Results tracking |
| `program.md` | Autonomous experiment protocol |

## License

MIT
