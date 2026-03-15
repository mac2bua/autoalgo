"""
Fixed evaluation harness for autoalgo.
DO NOT MODIFY THIS FILE - it contains the ground truth benchmarks.
"""

import time
import tracemalloc
import sys
import random
from pathlib import Path

# Import the algorithms module that gets modified
from algorithms import (
    find_max_subarray_sum,
    find_duplicates,
    merge_sorted_arrays,
    binary_search,
    quick_select,
    two_sum,
    LRUCache,
    count_inversions,
    longest_common_subsequence_length,
    matrix_multiply,
)


class Benchmark:
    """A single benchmark with fixed inputs."""

    def __init__(self, name, func, inputs, expected_output_checker=None):
        self.name = name
        self.func = func
        self.inputs = inputs
        self.expected_output_checker = expected_output_checker

    def run(self):
        """Run the benchmark and return timing info."""
        start = time.perf_counter()
        result = self.func(*self.inputs)
        elapsed = (time.perf_counter() - start) * 1000  # ms

        if self.expected_output_checker:
            assert self.expected_output_checker(result), f"Benchmark {self.name} failed correctness check"

        return elapsed, result


def create_benchmarks():
    """Create the fixed benchmark suite. DO NOT MODIFY."""

    benchmarks = []

    # Benchmark 1: Maximum subarray sum (Kadane's algorithm)
    random.seed(42)  # Fixed seed for reproducibility
    large_array = [random.randint(-100, 100) for _ in range(10000)]

    def check_max_subarray(result):
        return isinstance(result, (int, float))

    benchmarks.append(Benchmark(
        "max_subarray",
        find_max_subarray_sum,
        (large_array,),
        check_max_subarray
    ))

    # Benchmark 2: Find duplicates in list
    # Create a list with known duplicates for deterministic testing
    dup_list = list(range(2500)) + list(range(2500))  # 5000 elements, 2500 duplicates
    dup_list = dup_list * 3  # 15000 elements

    def check_duplicates(result):
        # Result should be a list with exactly 2500 unique duplicates
        return isinstance(result, list) and len(result) == 2500

    benchmarks.append(Benchmark(
        "find_duplicates",
        find_duplicates,
        (dup_list,),
        check_duplicates
    ))

    # Benchmark 3: Merge sorted arrays
    arr1 = sorted([random.randint(0, 1000) for _ in range(5000)])
    arr2 = sorted([random.randint(0, 1000) for _ in range(5000)])

    def check_merge(result):
        return len(result) == 10000 and result == sorted(result)

    benchmarks.append(Benchmark(
        "merge_sorted",
        merge_sorted_arrays,
        (arr1, arr2),
        check_merge
    ))

    # Benchmark 4: Binary search (multiple searches)
    sorted_array = sorted(range(100000))
    search_targets = [random.randint(0, 99999) for _ in range(1000)]

    def check_binary_search(result):
        return len(result) == 1000

    benchmarks.append(Benchmark(
        "binary_search",
        lambda arr, targets: [binary_search(arr, t) for t in targets],
        (sorted_array, search_targets),
        check_binary_search
    ))

    # Benchmark 5: Quick select (find kth smallest)
    unsorted = [random.randint(0, 10000) for _ in range(50000)]
    k_values = [100, 500, 1000, 5000, 10000]

    def check_quick_select(results):
        return len(results) == 5

    benchmarks.append(Benchmark(
        "quick_select",
        lambda arr, ks: [quick_select(arr.copy(), k) for k in ks],
        (unsorted, k_values),
        check_quick_select
    ))

    # Benchmark 6: Two sum problem
    nums = [random.randint(-1000, 1000) for _ in range(10000)]
    target = 500

    def check_two_sum(result):
        return result is None or (isinstance(result, tuple) and len(result) == 2)

    benchmarks.append(Benchmark(
        "two_sum",
        two_sum,
        (nums, target),
        check_two_sum
    ))

    # Benchmark 7: LRU cache operations
    def run_lru_benchmark():
        cache = LRUCache(1000)
        for i in range(5000):
            cache.put(i % 500, i)
        for i in range(1000):
            cache.get(i % 500)
        return True

    def check_lru(result):
        return result == True

    benchmarks.append(Benchmark(
        "lru_cache",
        lambda: run_lru_benchmark(),
        (),
        check_lru
    ))

    # Benchmark 8: Count inversions
    perm = list(range(10000))
    random.shuffle(perm)

    def check_inversions(result):
        return isinstance(result, int) and result >= 0

    benchmarks.append(Benchmark(
        "count_inversions",
        count_inversions,
        (perm,),
        check_inversions
    ))

    # Benchmark 9: Longest common subsequence
    str1 = ''.join(random.choices('ACGT', k=500))
    str2 = ''.join(random.choices('ACGT', k=500))

    def check_lcs(result):
        return isinstance(result, int)

    benchmarks.append(Benchmark(
        "lcs",
        longest_common_subsequence_length,
        (str1, str2),
        check_lcs
    ))

    # Benchmark 10: Matrix multiplication (small)
    import numpy as np
    np.random.seed(42)
    mat1 = np.random.rand(100, 100)
    mat2 = np.random.rand(100, 100)

    def check_matmul(result):
        # Result can be a numpy array or a list of lists
        if hasattr(result, 'shape'):
            return result.shape == (100, 100)
        else:
            return len(result) == 100 and len(result[0]) == 100

    benchmarks.append(Benchmark(
        "matrix_multiply",
        matrix_multiply,
        (mat1, mat2),
        check_matmul
    ))

    return benchmarks


def evaluate():
    """Run all benchmarks and report results."""
    print("Starting autoalgo evaluation...")
    print("-" * 40)

    tracemalloc.start()

    benchmarks = create_benchmarks()
    results = []

    for benchmark in benchmarks:
        try:
            elapsed_ms, _ = benchmark.run()
            results.append((benchmark.name, elapsed_ms, None))
            print(f"  {benchmark.name}: {elapsed_ms:.2f} ms")
        except Exception as e:
            print(f"  {benchmark.name}: CRASHED - {e}")
            results.append((benchmark.name, float('inf'), str(e)))

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    total_time = sum(r[1] for r in results if r[1] != float('inf'))
    successful = sum(1 for r in results if r[1] != float('inf'))
    crashed = len(results) - successful

    print("-" * 40)
    print(f"Benchmarks successful: {successful}/{len(results)}")
    if crashed > 0:
        print(f"CRASHED: {crashed}")
        sys.exit(1)

    print(f"total_time_ms:      {total_time:.6f}")
    print(f"memory_mb:          {peak / 1024 / 1024:.1f}")
    print(f"benchmarks_run:     {len(results)}")


if __name__ == "__main__":
    evaluate()
