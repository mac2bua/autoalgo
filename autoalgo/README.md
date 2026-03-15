# autoalgo

Autonomous algorithm optimization — an experiment to have the LLM do its own research on algorithm performance.

## ⚠️ Security Warning: Dangerous Permission Mode

This project requires running the LLM agent in a **dangerous permission mode** to function autonomously.

### What This Means

When you run Claude Code with `--dangerously-skip-permissions` (or similar settings), you are **granting the AI agent full access to execute any command** in your project directory without any approval prompts. This means the agent can:

- Read, modify, or delete any file in the project
- Run any shell command
- Install or remove packages
- Make git commits and modify history

### Is It Safe?

**For this specific use case, the risk is relatively low because:**

1. The agent is constrained to only modify `algorithms.py` and `results.tsv`
2. The agent follows a specific loop pattern defined in `program.md`
3. The agent's actions are limited to the project directory
4. Git provides a safety net (changes can be reverted with `git reset`)

**However, you should NOT use this setup if:**
- You're uncomfortable granting full system access to an AI agent
- Your project contains sensitive data or credentials
- You're running this on a shared or production system

**Recommendations:**
- Use a dedicated project directory for autonomous experiments
- Keep backups of important files
- Review changes before merging experiment branches
- Consider running in a container or VM for isolation

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

## Running Unattended (Autonomous Mode)

To run the agent indefinitely without manual intervention, you must **disable all permission prompts** so the agent can execute commands without waiting for approval.

### For Claude Code

If using **Ollama** (like the author's setup):
```bash
ollama launch claude --model qwen3-coder-next:cloud -- --dangerously-skip-permissions
```

If using the **Claude CLI** directly:
```bash
claude --dangerously-skip-permissions
```

If using **VS Code extension**:
Add to your settings (e.g., `~/.claude/settings.json`):
```json
{
  "skipDangerousModePermissionPrompt": true
}
```

**Why this is needed**: The autonomous loop runs continuously, making many small changes and running commands. Without disabling permission prompts, the agent will pause and wait for you to approve each command, causing it to stall.

**Expected behavior**: Once started, the agent will run experiments for ~5 minutes each, keeping improvements and discarding regressions. On an M-series Mac, you can expect ~12 experiments per hour. Leave it running overnight and check the results in the morning!

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
