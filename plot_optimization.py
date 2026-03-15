#!/usr/bin/env python3
"""Generate a proper visualization of the optimization progress."""

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import csv
from pathlib import Path

# Read results.tsv
results_path = Path(__file__).parent / 'results.tsv'
results = []
with open(results_path, 'r') as f:
    reader = csv.DictReader(f, delimiter='\t')
    for row in reader:
        results.append({
            'commit': row['commit'],
            'total_time_ms': float(row['total_time_ms']),
            'memory_mb': float(row['memory_mb']),
            'description': row['description']
        })

# Project directory path
project_dir = Path(__file__).parent
chart_path = project_dir / 'optimization_chart.png'
md_path = project_dir / 'optimization_chart.md'

# Create figure with subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

# Extract data for plotting
commits = [r['commit'] for r in results]
times = [r['total_time_ms'] for r in results]
memories = [r['memory_mb'] for r in results]
descriptions = [r['description'] for r in results]

# Shorten commit hashes for labels
short_commits = [c[:7] for c in commits]

# Plot 1: Total Time Progress
ax1.plot(range(len(commits)), times, 'o-', linewidth=2, markersize=8, color='#2563eb')
ax1.set_xlabel('Experiment', fontsize=12)
ax1.set_ylabel('Total Time (ms)', fontsize=12)
ax1.set_title('Algorithm Optimization: Total Time Reduction', fontsize=14)
ax1.grid(True, alpha=0.3)

# Add time improvement annotations
for i, (idx, time) in enumerate(zip(range(len(commits)), times)):
    if i == 0:
        ax1.annotate(f'{time:.0f}ms', (idx, time), textcoords="offset points",
                    xytext=(0, 10), ha='center', fontsize=9, fontweight='bold')
    elif i == len(commits) - 1:
        ax1.annotate(f'{time:.2f}ms', (idx, time), textcoords="offset points",
                    xytext=(0, -15), ha='center', fontsize=9, fontweight='bold',
                    color='green')
    elif i == 6:  # First sub-300ms
        ax1.annotate(f'{time:.0f}ms', (idx, time), textcoords="offset points",
                    xytext=(0, 10), ha='center', fontsize=8)

# Calculate improvement percentage
baseline = times[0]
final = times[-1]
improvement = (baseline - final) / baseline * 100
ax1.axhline(y=baseline, linestyle='--', color='red', alpha=0.5, label='Baseline (4187ms)')
ax1.text(len(commits) - 1, baseline * 1.02, f'{improvement:.1f}% improvement', fontsize=10)

# Plot 2: Memory Usage Progress
ax2.plot(range(len(commits)), memories, 's-', linewidth=2, markersize=8, color='#059669')
ax2.set_xlabel('Experiment', fontsize=12)
ax2.set_ylabel('Memory (MB)', fontsize=12)
ax2.set_title('Algorithm Optimization: Memory Usage', fontsize=14)
ax2.grid(True, alpha=0.3)

for i, (idx, mem) in enumerate(zip(range(len(commits)), memories)):
    if i == 0:
        ax2.annotate(f'{mem:.1f}MB', (idx, mem), textcoords="offset points",
                    xytext=(0, 10), ha='center', fontsize=9, fontweight='bold')
    elif i == len(commits) - 1:
        ax2.annotate(f'{mem:.1f}MB', (idx, mem), textcoords="offset points",
                    xytext=(0, -15), ha='center', fontsize=9, fontweight='bold',
                    color='green')

# Add x-axis labels ( shortened commits)
ax1.set_xticks(range(len(commits)))
ax1.set_xticklabels(short_commits, fontsize=8, rotation=45, ha='right')
ax2.set_xticks(range(len(commits)))
ax2.set_xticklabels(short_commits, fontsize=8, rotation=45, ha='right')

plt.tight_layout()
plt.savefig(chart_path, dpi=150, bbox_inches='tight')
print(f"Chart saved to {chart_path}")

# Create markdown report with relative image link
markdown = f"""# Algorithm Optimization Results

## Optimization Timeline

![Optimization Chart](optimization_chart.png)

## Results Summary

| Commit | Total Time (ms) | Memory (MB) | Description |
|--------|-----------------|-------------|-------------|
"""

for r in results:
    markdown += f"| {r['commit']} | {r['total_time_ms']:.2f} | {r['memory_mb']:.1f} | {r['description']} |\n"

markdown += f"""
## Key Findings

- **Baseline**: 4186.96ms
- **Final**: {final:.2f}ms
- **Improvement**: {improvement:.1f}% faster
- **Speedup**: {baseline/final:.1f}x

## Memory Optimization

Memory usage decreased from **17.0MB** to **9.5MB** (~44% reduction), indicating more efficient data structures and reduced temporary allocations.

## Top Optimizations

1. **Module-level imports** - Avoided repeated import overhead on each function call
2. **zip() for LCS character comparison** - Faster than direct indexing
3. **While loops for merge extension** - Faster than list.extend() for remaining elements
4. **Numpy array return** - Avoided .tolist() conversion overhead

## Usage

Run the chart generation script:
```bash
uv run plot_optimization.py
```
"""

with open(md_path, 'w') as f:
    f.write(markdown)
print(f"Markdown report saved to {md_path}")
