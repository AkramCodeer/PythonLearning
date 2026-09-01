"""
===============================================================================
 PRACTICE PROBLEMS — 50 Problems (Easy to Medium)
===============================================================================
 Solve these to build your Python muscle memory!
 Each problem has hints and expected output.
 Solutions are in practice_solutions.py
 
 Run this file:  python practice_problems.py
===============================================================================
"""


# ===========================================================================
# CATEGORY 1: STRINGS (Problems 1-10)
# ===========================================================================

print("=" * 60)
print("CATEGORY 1: STRINGS")
print("=" * 60)

# Problem 1: Reverse a string
# Input: "Hello World" → Output: "dlroW olleH"
def reverse_string(s):
    # YOUR CODE HERE
    pass

# Problem 2: Check if a string is a palindrome (ignore case and spaces)
# Input: "A man a plan a canal Panama" → Output: True
def is_palindrome(s):
    # YOUR CODE HERE
    pass

# Problem 3: Count vowels and consonants
# Input: "Hello World" → Output: {"vowels": 3, "consonants": 7}
def count_vowels_consonants(s):
    # YOUR CODE HERE
    pass

# Problem 4: Find the most frequent character in a string
# Input: "hello world" → Output: 'l'
def most_frequent_char(s):
    # YOUR CODE HERE
    pass

# Problem 5: Check if two strings are anagrams
# Input: "listen", "silent" → Output: True
def are_anagrams(s1, s2):
    # YOUR CODE HERE
    pass

# Problem 6: Remove duplicate characters (keep first occurrence)
# Input: "programming" → Output: "progamin"
def remove_duplicates(s):
    # YOUR CODE HERE
    pass

# Problem 7: Capitalize first letter of each word
# Input: "hello world python" → Output: "Hello World Python"
def capitalize_words(s):
    # YOUR CODE HERE
    pass

# Problem 8: Compress a string using run-length encoding
# Input: "aaabbbccdddd" → Output: "a3b3c2d4"
def compress_string(s):
    # YOUR CODE HERE
    pass

# Problem 9: Check if string has all unique characters
# Input: "abcdef" → True, "hello" → False
def all_unique(s):
    # YOUR CODE HERE
    pass

# Problem 10: Find longest word in a sentence
# Input: "The quick brown fox" → Output: "quick" (or "brown")
def longest_word(s):
    # YOUR CODE HERE
    pass


# ===========================================================================
# CATEGORY 2: LISTS (Problems 11-20)
# ===========================================================================

print(f"\n{'=' * 60}")
print("CATEGORY 2: LISTS")
print("=" * 60)

# Problem 11: Find the second largest number
# Input: [3, 1, 4, 1, 5, 9, 2, 6] → Output: 6
def second_largest(nums):
    # YOUR CODE HERE
    pass

# Problem 12: Remove all duplicates from a list (preserve order)
# Input: [1, 3, 2, 3, 1, 4, 2] → Output: [1, 3, 2, 4]
def remove_list_duplicates(lst):
    # YOUR CODE HERE
    pass

# Problem 13: Flatten a nested list (any depth)
# Input: [1, [2, 3], [4, [5, 6]], 7] → Output: [1, 2, 3, 4, 5, 6, 7]
def flatten(lst):
    # YOUR CODE HERE
    pass

# Problem 14: Rotate a list by k positions to the right
# Input: [1, 2, 3, 4, 5], k=2 → Output: [4, 5, 1, 2, 3]
def rotate_list(lst, k):
    # YOUR CODE HERE
    pass

# Problem 15: Find all pairs that sum to a target
# Input: [1, 2, 3, 4, 5], target=6 → Output: [(1,5), (2,4)]
def find_pairs(nums, target):
    # YOUR CODE HERE
    pass

# Problem 16: Merge two sorted lists into one sorted list
# Input: [1, 3, 5], [2, 4, 6] → Output: [1, 2, 3, 4, 5, 6]
def merge_sorted(list1, list2):
    # YOUR CODE HERE
    pass

# Problem 17: Find the missing number (1 to n)
# Input: [1, 2, 4, 5, 6] → Output: 3
def find_missing(nums):
    # YOUR CODE HERE
    pass

# Problem 18: Group elements by a key function
# Input: [1, 2, 3, 4, 5, 6], key=lambda x: "even" if x%2==0 else "odd"
# Output: {"odd": [1, 3, 5], "even": [2, 4, 6]}
def group_by(lst, key_func):
    # YOUR CODE HERE
    pass

# Problem 19: Find the intersection of two lists
# Input: [1, 2, 3, 4], [3, 4, 5, 6] → Output: [3, 4]
def list_intersection(lst1, lst2):
    # YOUR CODE HERE
    pass

# Problem 20: Chunk a list into groups of n
# Input: [1, 2, 3, 4, 5, 6, 7], n=3 → Output: [[1,2,3], [4,5,6], [7]]
def chunk_list(lst, n):
    # YOUR CODE HERE
    pass


# ===========================================================================
# CATEGORY 3: DICTIONARIES (Problems 21-28)
# ===========================================================================

print(f"\n{'=' * 60}")
print("CATEGORY 3: DICTIONARIES")
print("=" * 60)

# Problem 21: Merge two dicts, summing values for common keys
# Input: {"a": 1, "b": 2}, {"b": 3, "c": 4} → {"a": 1, "b": 5, "c": 4}
def merge_dicts_sum(d1, d2):
    # YOUR CODE HERE
    pass

# Problem 22: Invert a dictionary (swap keys and values)
# Input: {"a": 1, "b": 2, "c": 3} → {1: "a", 2: "b", 3: "c"}
def invert_dict(d):
    # YOUR CODE HERE
    pass

# Problem 23: Find the key with the maximum value
# Input: {"a": 10, "b": 25, "c": 15} → Output: "b"
def max_value_key(d):
    # YOUR CODE HERE
    pass

# Problem 24: Count word frequency in a sentence
# Input: "the quick brown fox the quick" → {"the": 2, "quick": 2, "brown": 1, "fox": 1}
def word_frequency(sentence):
    # YOUR CODE HERE
    pass

# Problem 25: Flatten a nested dictionary
# Input: {"a": {"b": 1, "c": {"d": 2}}} → {"a.b": 1, "a.c.d": 2}
def flatten_dict(d, parent_key="", sep="."):
    # YOUR CODE HERE
    pass

# Problem 26: Group a list of dicts by a key
# Input: [{"name": "A", "dept": "IT"}, {"name": "B", "dept": "HR"}, 
#         {"name": "C", "dept": "IT"}], key="dept"
# Output: {"IT": [...], "HR": [...]}
def group_dicts_by(lst, key):
    # YOUR CODE HERE
    pass

# Problem 27: Deep merge two nested dicts
# Input: {"a": {"b": 1}}, {"a": {"c": 2}} → {"a": {"b": 1, "c": 2}}
def deep_merge(d1, d2):
    # YOUR CODE HERE
    pass

# Problem 28: Sort a dict by values
# Input: {"banana": 3, "apple": 1, "cherry": 2} → {"apple": 1, "cherry": 2, "banana": 3}
def sort_dict_by_value(d):
    # YOUR CODE HERE
    pass


# ===========================================================================
# CATEGORY 4: FUNCTIONS & COMPREHENSIONS (Problems 29-36)
# ===========================================================================

print(f"\n{'=' * 60}")
print("CATEGORY 4: FUNCTIONS & COMPREHENSIONS")
print("=" * 60)

# Problem 29: Write a function that memoizes any function
# Usage: @memoize def fib(n): ...
def memoize(func):
    # YOUR CODE HERE
    pass

# Problem 30: Write a compose function
# compose(f, g)(x) should return f(g(x))
def compose(f, g):
    # YOUR CODE HERE
    pass

# Problem 31: FizzBuzz using list comprehension (1 to n)
def fizzbuzz(n):
    # YOUR CODE HERE (return a list)
    pass

# Problem 32: Matrix transpose using list comprehension
# Input: [[1,2,3], [4,5,6]] → [[1,4], [2,5], [3,6]]
def transpose(matrix):
    # YOUR CODE HERE
    pass

# Problem 33: Generate Pascal's Triangle (n rows)
# Input: 5 → [[1], [1,1], [1,2,1], [1,3,3,1], [1,4,6,4,1]]
def pascal_triangle(n):
    # YOUR CODE HERE
    pass

# Problem 34: Implement a pipe function
# pipe(fn1, fn2, fn3)(x) = fn3(fn2(fn1(x)))
def pipe(*functions):
    # YOUR CODE HERE
    pass

# Problem 35: Create a range function that works with floats
# float_range(0, 1, 0.2) → [0, 0.2, 0.4, 0.6, 0.8]
def float_range(start, stop, step):
    # YOUR CODE HERE
    pass

# Problem 36: Write a retry decorator with exponential backoff
def retry_with_backoff(max_retries=3, base_delay=0.1):
    # YOUR CODE HERE (return a decorator)
    pass


# ===========================================================================
# CATEGORY 5: OOP (Problems 37-42)
# ===========================================================================

print(f"\n{'=' * 60}")
print("CATEGORY 5: OOP")
print("=" * 60)

# Problem 37: Implement a Stack class
# Methods: push, pop, peek, is_empty, size, __str__
# YOUR CODE HERE

# Problem 38: Implement a Queue class
# Methods: enqueue, dequeue, peek, is_empty, size, __str__
# YOUR CODE HERE

# Problem 39: Implement a LinkedList class
# Methods: append, prepend, delete, find, __str__, __len__
# YOUR CODE HERE

# Problem 40: Implement a BankAccount class with transaction history
# Methods: deposit, withdraw, get_balance, get_history, __str__
# YOUR CODE HERE

# Problem 41: Implement a simple EventEmitter (like Node.js!)
# Methods: on(event, callback), emit(event, *args), off(event, callback)
# YOUR CODE HERE

# Problem 42: Implement a LRU Cache class
# Methods: get(key), put(key, value) — with max capacity
# YOUR CODE HERE


# ===========================================================================
# CATEGORY 6: GENERATORS & ADVANCED (Problems 43-50)
# ===========================================================================

print(f"\n{'=' * 60}")
print("CATEGORY 6: GENERATORS & ADVANCED")
print("=" * 60)

# Problem 43: Write a generator for infinite prime numbers
def prime_generator():
    # YOUR CODE HERE
    pass

# Problem 44: Write a generator that yields Fibonacci numbers
def fib_generator():
    # YOUR CODE HERE
    pass

# Problem 45: Write a generator pipeline
# numbers → filter evens → square → take first 5
# Input: range(1, 100) → Output: [4, 16, 36, 64, 100]
def pipeline_demo():
    # YOUR CODE HERE
    pass

# Problem 46: Implement a simple CSV parser generator
# Yields one row (as dict) at a time from a CSV string
def parse_csv(csv_string):
    # YOUR CODE HERE
    pass

# Problem 47: Write a context manager for timing code
# Usage: with Timer() as t: ... print(t.elapsed)
# YOUR CODE HERE

# Problem 48: Implement a simple decorator that logs execution time
# YOUR CODE HERE

# Problem 49: Write an async function that fetches multiple URLs concurrently
# (simulate with asyncio.sleep)
# YOUR CODE HERE

# Problem 50: Implement binary search (iterative and recursive)
def binary_search_iterative(arr, target):
    # YOUR CODE HERE
    pass

def binary_search_recursive(arr, target, low=0, high=None):
    # YOUR CODE HERE
    pass


# ===========================================================================
# TEST FRAMEWORK
# ===========================================================================

def test(name, actual, expected):
    """Simple test helper."""
    status = "✅" if actual == expected else "❌"
    print(f"  {status} {name}")
    if actual != expected:
        print(f"     Expected: {expected}")
        print(f"     Got:      {actual}")

# Uncomment tests as you solve problems:
# print("\n--- Testing ---")
# test("reverse_string", reverse_string("Hello World"), "dlroW olleH")
# test("is_palindrome", is_palindrome("A man a plan a canal Panama"), True)
# test("second_largest", second_largest([3,1,4,1,5,9,2,6]), 6)
# test("find_missing", find_missing([1,2,4,5,6]), 3)
# test("fizzbuzz[14]", fizzbuzz(15)[-1], "FizzBuzz")


print("\n📝 Open this file and start solving! Uncomment tests as you go.")
print("💡 Solutions are in practice_solutions.py")
print("\n✅ Practice Problems loaded!")
