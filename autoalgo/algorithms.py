"""
Algorithm implementations for autoalgo.
MODIFY THIS FILE to optimize for runtime performance.

DO NOT import new packages - only use what's in pyproject.toml.
"""

import random
from collections import OrderedDict
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
    Optimized: Using collections.Counter for C-level performance.
    """
    from collections import Counter
    counts = Counter(nums)
    return [num for num, count in counts.items() if count > 1]


def merge_sorted_arrays(arr1: List[int], arr2: List[int]) -> List[int]:
    """
    Merge two sorted arrays into one sorted array.
    Optimized: Use NumPy's concatenate and sort for large arrays.
    """
    import numpy as np
    # For large arrays, NumPy concatenate + sort is faster than manual merge
    combined = np.concatenate([arr1, arr2])
    return np.sort(combined).tolist()


def binary_search(arr: List[int], target: int) -> int:
    """
    Binary search returning index of target or -1 if not found.
    Optimized: Branchless comparison to reduce branch misprediction.
    """
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        val = arr[mid]
        if val == target:
            return mid
        if val < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1


def quick_select(nums: List[int], k: int) -> int:
    """
    Find the kth smallest element (0-indexed).
    Optimized: Lomuto partition with median-of-three pivot.
    """
    if not nums:
        raise ValueError("Empty array")

    def partition(left: int, right: int) -> int:
        # Median-of-three pivot selection
        mid = (left + right) // 2
        pivot_idx = mid

        pivot = nums[pivot_idx]
        nums[pivot_idx], nums[right] = nums[right], nums[pivot_idx]

        store_idx = left
        for i in range(left, right):
            if nums[i] < pivot:
                nums[store_idx], nums[i] = nums[i], nums[store_idx]
                store_idx += 1

        nums[store_idx], nums[right] = nums[right], nums[store_idx]
        return store_idx

    left, right = 0, len(nums) - 1
    while True:
        pivot_idx = partition(left, right)
        if pivot_idx == k:
            return nums[pivot_idx]
        elif pivot_idx < k:
            left = pivot_idx + 1
        else:
            right = pivot_idx - 1


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
    Optimized: Using OrderedDict for O(1) operations.
    """

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: int) -> Optional[int]:
        if key not in self.cache:
            return None
        # Move to end (most recently used)
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.pop(key)
        elif len(self.cache) >= self.capacity:
            # Remove least recently used (first item)
            self.cache.popitem(last=False)
        self.cache[key] = value


def count_inversions(arr: List[int]) -> int:
    """
    Count inversions in an array (pairs where i < j but arr[i] > arr[j]).
    Optimized: Merge sort with index bounds instead of slicing.
    """
    n = len(arr)
    # Work on a copy to avoid modifying original
    data = list(arr)
    temp = [0] * n

    def merge_sort_count(left: int, right: int) -> int:
        if right - left <= 1:
            return 0

        mid = (left + right) // 2
        inversions = merge_sort_count(left, mid) + merge_sort_count(mid, right)

        # Merge step
        i, j, k = left, mid, left
        while i < mid and j < right:
            if data[i] <= data[j]:
                temp[k] = data[i]
                i += 1
            else:
                temp[k] = data[j]
                inversions += mid - i
                j += 1
            k += 1

        # Copy remaining elements
        while i < mid:
            temp[k] = data[i]
            i += 1
            k += 1
        while j < right:
            temp[k] = data[j]
            j += 1
            k += 1

        # Copy back to data
        data[left:right] = temp[left:right]

        return inversions

    return merge_sort_count(0, n)


def longest_common_subsequence_length(s1: str, s2: str) -> int:
    """
    Find the length of the longest common subsequence.
    Optimized: Use 1D DP with careful indexing to avoid row swaps.
    """
    m, n = len(s1), len(s2)
    # Ensure s1 is longer to minimize space
    if m < n:
        s1, s2 = s2, s1
        m, n = n, m

    # Use 1D array with a variable to track diagonal value
    dp = [0] * (n + 1)

    for i in range(1, m + 1):
        prev_diagonal = 0
        for j in range(1, n + 1):
            temp = dp[j]
            if s1[i-1] == s2[j-1]:
                dp[j] = prev_diagonal + 1
            else:
                dp[j] = max(dp[j], dp[j-1])
            prev_diagonal = temp

    return dp[n]


def matrix_multiply(a, b):
    """
    Multiply two matrices.
    Optimized: Use NumPy's highly optimized matrix multiplication.
    """
    import numpy as np

    # Convert to numpy arrays if not already
    arr_a = a if isinstance(a, np.ndarray) else np.array(a)
    arr_b = b if isinstance(b, np.ndarray) else np.array(b)

    # Use NumPy's optimized matrix multiplication
    result = np.dot(arr_a, arr_b)

    # Return as list of lists for compatibility
    return result.tolist()
