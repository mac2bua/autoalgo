# Memory for Karpathy AutoResearch Experiment

## Auto-optimization Strategy

### DO NOT STOP until one of these conditions is met:
1. User explicitly stops the experiment
2. 3 consecutive experiments fail to improve the score
3. Time budget exceeded (15 minutes total)

### Required number of experiments:
- Minimum 100 experiments per optimization target
- At least 3 different approaches per optimization category

### Optimization Categories to explore:
1. **Data structures**: array, deque, defaultdict, Counter
2. **Loop optimizations**: enumerate vs range, zip vs direct indexing
3. **Memory access patterns**: caching, precomputation, local variables
4. **Algorithmic improvements**: different algorithm for same problem
5. **Library-specific optimizations**: numpy vs built-in, special functions

### After 5 consecutive failures:
- Enter "brainstorm mode" - generate 10 new ideas without testing
- Prioritize ideas that are most different from current approach
- Try one completely new approach per category

### Current best score tracking:
- Track all scores in results.tsv
- Always compare against best known score, not previous score
