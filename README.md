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

1. **Create an experiment branch** (date format: DD-MM-YYYY):
   ```bash
   git checkout -b autoalgo/15-03-2026
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

3. **Run the baseline**:
   ```bash
   uv run evaluate.py > run.log 2>&1
   ```

4. **Record the baseline** in `results.tsv`:
   - Get the `total_time_ms` and `memory_mb` from `run.log`
   - Add a row with status `baseline`

5. **Kick off the loop**:
   Point Claude Code or another coding agent at `program.md` and let it run the loop.

## Experimentation

- **`algorithms.py`**: Modify this file with experimental optimizations
- **`evaluate.py`**: Fixed benchmark harness (DO NOT MODIFY)
- **`results.tsv`**: Tracks experiment results

Each experiment runs for ~5 minutes, testing different algorithm approaches.

## Files

| File | Purpose |
|------|---------|
| `algorithms.py` | Algorithm implementations (MODIFY THIS for optimization) |
| `evaluate.py` | Fixed evaluation harness (DO NOT MODIFY) |
| `results.tsv` | Results tracking |
| `program.md` | The autonomous experiment protocol |

## License

MIT
