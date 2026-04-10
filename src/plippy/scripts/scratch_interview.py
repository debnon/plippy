"""
Interview practice problems.
Fill in each function body, then run the file to check your answers.

    /Users/debnon/plippy/.venv/bin/python src/plippy/scripts/scratch_interview.py
"""

from __future__ import annotations

import asyncio
import json


# ---------------------------------------------------------------------------
# 1. Strings
# ---------------------------------------------------------------------------

def is_palindrome(s: str) -> bool:
    """Return True if s reads the same forwards and backwards (ignore case)."""
    # Hint: lowercase + two-pointer or slice comparison
    s = s.lower()
    sr = s[::-1]
    for n in range(0, len(s)):
        if s[n] != sr[n]:
            return False
    return True

    ...


def count_vowels(s: str) -> int:
    """Return the number of vowels (a e i o u) in s (case-insensitive)."""
    vowels = {"a", "e", "i", "o", "u"}
    count = 0
    for char in s.lower():
        if char in vowels:
            count += 1
    return count
    ...


def first_non_repeating_char(s: str) -> str | None:
    """Return the first character that appears exactly once, or None."""
    # Hint: collections.Counter then scan original string
    ...


# ---------------------------------------------------------------------------
# 2. Lists / Arrays
# ---------------------------------------------------------------------------

def two_sum(nums: list[int], target: int) -> tuple[int, int] | None:
    """Return indices (i, j) where nums[i] + nums[j] == target, or None."""
    # Hint: dict mapping value -> index; one pass
    ...


def max_subarray_sum(nums: list[int]) -> int:
    """Return the largest contiguous subarray sum (Kadane's algorithm)."""
    # Hint: track current_sum and best_sum; reset current_sum when it goes negative
    ...


def rotate_list(nums: list[int], k: int) -> list[int]:
    """Return nums rotated right by k positions (non-destructive)."""
    # Hint: slicing with modulo; handle empty list
    ...


# ---------------------------------------------------------------------------
# 3. Dicts / Hashing
# ---------------------------------------------------------------------------

def group_anagrams(words: list[str]) -> list[list[str]]:
    """Group words that are anagrams of each other."""
    # Hint: use sorted(word) as dict key
    ...


def most_frequent(items: list) -> object:
    """Return the item that appears most often (any type)."""
    # Hint: collections.Counter.most_common(1)
    ...


# ---------------------------------------------------------------------------
# 4. Recursion
# ---------------------------------------------------------------------------

def fibonacci(n: int) -> int:
    """Return the nth Fibonacci number (0-indexed: fib(0)=0, fib(1)=1)."""
    # Hint: base cases n==0 and n==1; then recurse
    # Stretch: try a memoized version with @functools.lru_cache
    ...


def flatten(nested: list) -> list:
    """Flatten an arbitrarily nested list into a flat list."""
    # Hint: recurse when element is a list, otherwise append
    ...


# ---------------------------------------------------------------------------
# 5. Sorting / Searching
# ---------------------------------------------------------------------------

def binary_search(nums: list[int], target: int) -> int:
    """Return index of target in sorted nums, or -1 if not found."""
    # Hint: lo/hi pointers; mid = (lo + hi) // 2
    ...


def merge_sorted(a: list[int], b: list[int]) -> list[int]:
    """Merge two sorted lists into one sorted list."""
    # Hint: two-pointer walk; append remainders
    ...


# ---------------------------------------------------------------------------
# 6. JSON parsing
# ---------------------------------------------------------------------------

def parse_user(raw: str) -> dict | None:
    """
    Parse a JSON string representing a user.
    Return a dict with keys 'id' (int), 'name' (str), 'email' (str).
    Return None if the string is invalid JSON or missing any of those keys.
    """
    # Hint: json.loads inside a try/except; then check for required keys
    try:
        data = json.loads(raw)
        if not all(k in data for k in ("id", "name", "email")):
            return None
        return {"id": data["id"], "name": data["name"], "email": data["email"]}
    except json.JSONDecodeError:
        return None
    ...


def extract_emails(raw: str) -> list[str]:
    """
    Given a JSON string containing a list of user objects under key 'users',
    return a sorted list of all email strings (lowercased, stripped).
    Return [] on any parse error or missing key.
    """
    # Hint: json.loads, then [u['email'].strip().lower() for u in payload['users']]
    ...


def merge_json_objects(a: str, b: str) -> str:
    """
    Parse two JSON objects and merge them into one.
    Keys from b override keys from a on conflict.
    Return the result as a compact JSON string (no extra spaces).
    Return '{}' if either input is invalid JSON or not a JSON object.
    """
    # Hint: json.loads both, {**dict_a, **dict_b}, then json.dumps
    ...


# ---------------------------------------------------------------------------
# 7. asyncio
# ---------------------------------------------------------------------------

async def async_double(n: int) -> int:
    """Wait 0 ms then return n * 2. Practice: make it actually async."""
    # Hint: await asyncio.sleep(0) yields control even with zero delay
    await asyncio.sleep(0)
    return n * 2
    ...


async def gather_results(values: list[int]) -> list[int]:
    """
    Double every value in the list concurrently using asyncio.gather.
    Return results in the same order as inputs.
    """
    # Hint: asyncio.gather(*(async_double(v) for v in values))
    return await asyncio.gather(*(async_double(v) for v in values))
    ...



async def first_above_threshold(values: list[int], threshold: int) -> int | None:
    """
    Simulate fetching each value asynchronously (asyncio.sleep(0)).
    Return the FIRST value that exceeds threshold (completion order, not input order).
    Return None if none exceed it.
    """
    # Hint: asyncio.create_task per value, then asyncio.as_completed
    # Inner coroutine should sleep then return the value.
    ...


# ---------------------------------------------------------------------------
# Tests — add more as you go
# ---------------------------------------------------------------------------

def run_tests() -> None:
    results = []

    def check(label: str, got, expected) -> None:
        ok = got == expected
        results.append(ok)
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {label}")
        if not ok:
            print(f"         expected: {expected!r}")
            print(f"              got: {got!r}")

    print("\n--- Strings ---")
    check("is_palindrome('racecar')", is_palindrome("racecar"), True)
    check("is_palindrome('Racecar')", is_palindrome("Racecar"), True)
    check("is_palindrome('hello')",   is_palindrome("hello"),   False)
    check("count_vowels('hello')",    count_vowels("hello"),     2)
    check("count_vowels('AEIOU')",    count_vowels("AEIOU"),     5)
    check("first_non_repeating_char('aabbc')",  first_non_repeating_char("aabbc"),  "c")
    check("first_non_repeating_char('aabb')",   first_non_repeating_char("aabb"),   None)

    print("\n--- Lists ---")
    check("two_sum([2,7,11,15], 9)",   two_sum([2, 7, 11, 15], 9),   (0, 1))
    check("two_sum([3,2,4], 6)",       two_sum([3, 2, 4], 6),         (1, 2))
    check("two_sum([1,2,3], 99)",      two_sum([1, 2, 3], 99),        None)
    check("max_subarray_sum([-2,1,-3,4,-1,2,1,-5,4])",
          max_subarray_sum([-2, 1, -3, 4, -1, 2, 1, -5, 4]), 6)
    check("rotate_list([1,2,3,4,5], 2)", rotate_list([1, 2, 3, 4, 5], 2), [4, 5, 1, 2, 3])
    check("rotate_list([1,2,3], 0)",     rotate_list([1, 2, 3], 0),         [1, 2, 3])

    print("\n--- Dicts ---")
    raw = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
    check("group_anagrams(['eat','tea','tan','ate','nat','bat'])",
          sorted([sorted(g) for g in raw]) if raw is not None else None,
          sorted([["ate", "eat", "tea"], ["bat"], ["nat", "tan"]]))
    check("most_frequent([1,3,3,2,1,3])", most_frequent([1, 3, 3, 2, 1, 3]), 3)

    print("\n--- Recursion ---")
    check("fibonacci(0)",  fibonacci(0),  0)
    check("fibonacci(1)",  fibonacci(1),  1)
    check("fibonacci(7)",  fibonacci(7),  13)
    check("flatten([1,[2,[3,[4]]],5])", flatten([1, [2, [3, [4]]], 5]), [1, 2, 3, 4, 5])

    print("\n--- Sorting / Searching ---")
    check("binary_search([1,3,5,7,9], 5)",  binary_search([1, 3, 5, 7, 9], 5),  2)
    check("binary_search([1,3,5,7,9], 4)",  binary_search([1, 3, 5, 7, 9], 4),  -1)
    check("merge_sorted([1,3,5],[2,4,6])",
          merge_sorted([1, 3, 5], [2, 4, 6]), [1, 2, 3, 4, 5, 6])

    print("\n--- JSON ---")
    check(
        "parse_user valid",
        parse_user('{"id": 1, "name": "Alice", "email": "alice@example.com"}'),
        {"id": 1, "name": "Alice", "email": "alice@example.com"},
    )
    check("parse_user missing key", parse_user('{"id": 1, "name": "Alice"}'), None)
    check("parse_user invalid json", parse_user("not json"), None)
    check(
        "extract_emails",
        extract_emails('{"users": [{"email": " Bob@X.com "}, {"email": "alice@y.com"}]}'),
        ["alice@y.com", "bob@x.com"],
    )
    check("extract_emails bad json", extract_emails("bad"), [])
    check(
        "merge_json_objects",
        merge_json_objects('{"a": 1, "b": 2}', '{"b": 99, "c": 3}'),
        '{"a": 1, "b": 99, "c": 3}',
    )
    check("merge_json_objects invalid", merge_json_objects("bad", '{"a": 1}'), "{}")

    print("\n--- asyncio ---")

    async def run_async_checks() -> None:
        check("async_double(5)",      await async_double(5),         10)
        check("async_double(0)",      await async_double(0),          0)
        check("gather_results",       await gather_results([1,2,3]), [2, 4, 6])
        check("gather_results empty", await gather_results([]),       [])
        check(
            "first_above_threshold found",
            await first_above_threshold([1, 5, 3, 8, 2], 4),
            5,
        )
        check(
            "first_above_threshold none",
            await first_above_threshold([1, 2, 3], 99),
            None,
        )

    asyncio.run(run_async_checks())

    passed = sum(results)
    total  = len(results)
    print(f"\n{passed}/{total} tests passed.")


if __name__ == "__main__":
    run_tests()
