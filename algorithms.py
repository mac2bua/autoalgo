"""
Algorithm implementations for autoalgo.
MODIFY THIS FILE to optimize for runtime performance.

DO NOT import new packages - only use what's in pyproject.toml.
"""

import random
import bisect
import heapq
import numpy as np
from typing import List, Tuple, Optional


def find_max_subarray_sum(nums: List[int]) -> int:
    """
    Find the maximum sum of a contiguous subarray.
    Baseline: Kadane's algorithm.
    """
    if not nums:
        return 0

    max_sum = current_sum = nums[0]
    for num in nums[1:]:
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)
    return max_sum


def find_duplicates(nums: List[int]) -> List[int]:
    """
    Find all duplicate numbers in the list.
    Baseline: Using a set to track seen numbers.
    """
    seen = set()
    duplicates = set()
    for num in nums:
        if num in seen:
            duplicates.add(num)
        else:
            seen.add(num)
    return list(duplicates)


def merge_sorted_arrays(arr1: List[int], arr2: List[int]) -> List[int]:
    """
    Merge two sorted arrays into one sorted array.
    Optimized: Use heapq.merge for efficient merging.
    """
    return list(heapq.merge(arr1, arr2))


def binary_search(arr: List[int], target: int) -> int:
    """
    Binary search returning index of target or -1 if not found.
    Optimized: Use bisect module for faster binary search.
    """
    idx = bisect.bisect_left(arr, target)
    if idx < len(arr) and arr[idx] == target:
        return idx
    return -1


def quick_select(nums: List[int], k: int) -> int:
    """
    Find the kth smallest element (0-indexed).
    Optimized: Use numpy's partition for O(n) average time.
    """
    arr = np.array(nums)
    return np.partition(arr, k)[k]


def two_sum(nums: List[int], target: int) -> Optional[Tuple[int, int]]:
    """
    Find two numbers that add up to target.
    Returns indices of the two numbers or None if not found.
    Baseline: Hash map approach.
    """
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return (seen[complement], i)
        seen[num] = i
    return None


class LRUCache:
    """
    LRU Cache implementation.
    Baseline: Using OrderedDict.
    """

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.order = []  # Keep track of access order

    def get(self, key: int) -> Optional[int]:
        if key not in self.cache:
            return None
        # Move to end (most recently used)
        self.order.remove(key)
        self.order.append(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.order.remove(key)
        elif len(self.cache) >= self.capacity:
            # Remove least recently used
            lru_key = self.order.pop(0)
            del self.cache[lru_key]
        self.cache[key] = value
        self.order.append(key)


def count_inversions(arr: List[int]) -> int:
    """
    Count inversions in an array (pairs where i < j but arr[i] > arr[j]).
    Optimized: Merge sort with local variable caching.
    """
    def merge_sort_count(arr: List[int]) -> Tuple[List[int], int]:
        n = len(arr)
        if n <= 1:
            return arr, 0

        mid = n // 2
        left, left_count = merge_sort_count(arr[:mid])
        right, right_count = merge_sort_count(arr[mid:])

        merged = []
        i = j = 0
        inversions = left_count + right_count
        left_len = len(left)
        right_len = len(right)

        while i < left_len and j < right_len:
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                inversions += left_len - i
                j += 1

        # Append remaining elements
        while i < left_len:
            merged.append(left[i])
            i += 1
        while j < right_len:
            merged.append(right[j])
            j += 1

        return merged, inversions

    _, count = merge_sort_count(arr[:])
    return count


def longest_common_subsequence_length(s1: str, s2: str) -> int:
    """
    Find the length of the longest common subsequence.
    Optimized: Using zip for s2 character comparison.
    """
    m, n = len(s1), len(s2)

    prev = [0] * (n + 1)
    curr = [0] * (n + 1)

    for i, c1 in enumerate(s1, 1):
        prev_j = prev[0]
        curr[0] = 0
        for j, c2 in zip(range(1, n + 1), s2):
            temp = prev[j]
            if c1 == c2:
                curr[j] = prev_j + 1
            else:
                curr[j] = curr[j - 1] if curr[j - 1] > prev[j] else prev[j]
            prev_j = temp
        prev, curr = curr, prev

    return prev[n]


def matrix_multiply(a, b):
    """
    Multiply two matrices.
    Optimized: Use numpy's optimized matrix multiplication.
    """
    import numpy as np
    # Convert to numpy array, multiply, convert back to list
    result = np.dot(np.array(a), np.array(b))
    return result.tolist()
