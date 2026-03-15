"""
Algorithm implementations for autoalgo.
MODIFY THIS FILE to optimize for runtime performance.

DO NOT import new packages - only use what's in pyproject.toml.
"""

import random
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
    Baseline: Two-pointer merge from merge sort.
    """
    result = []
    i, j = 0, 0
    while i < len(arr1) and j < len(arr2):
        if arr1[i] <= arr2[j]:
            result.append(arr1[i])
            i += 1
        else:
            result.append(arr2[j])
            j += 1
    result.extend(arr1[i:])
    result.extend(arr2[j:])
    return result


def binary_search(arr: List[int], target: int) -> int:
    """
    Binary search returning index of target or -1 if not found.
    Baseline: Iterative binary search.
    """
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1


def quick_select(nums: List[int], k: int) -> int:
    """
    Find the kth smallest element (0-indexed).
    Baseline: Lomuto partition scheme with median-of-three pivot.
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
    Baseline: Modified merge sort.
    """
    def merge_sort_count(arr: List[int]) -> Tuple[List[int], int]:
        if len(arr) <= 1:
            return arr, 0

        mid = len(arr) // 2
        left, left_count = merge_sort_count(arr[:mid])
        right, right_count = merge_sort_count(arr[mid:])

        merged = []
        i = j = 0
        inversions = left_count + right_count

        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                inversions += len(left) - i
                j += 1

        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged, inversions

    _, count = merge_sort_count(arr[:])
    return count


def longest_common_subsequence_length(s1: str, s2: str) -> int:
    """
    Find the length of the longest common subsequence.
    Optimized: Space-efficient DP using two rows.
    """
    m, n = len(s1), len(s2)

    # Use two rows instead of full 2D table
    prev = list(range(n + 1))
    curr = [0] * (n + 1)

    for i in range(1, m + 1):
        curr[0] = 0
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                curr[j] = prev[j-1] + 1
            else:
                curr[j] = max(prev[j], curr[j-1])
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
