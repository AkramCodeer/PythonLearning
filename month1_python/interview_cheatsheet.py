"""
===============================================================================
 PYTHON INTERVIEW CHEAT SHEET
===============================================================================
 Quick reference for the most common Python interview questions
 Keep this handy during your interview prep!
 
 Run this file:  python interview_cheatsheet.py
===============================================================================
"""


# ===========================================================================
# 1. MUTABILITY
# ===========================================================================
"""
MUTABLE (can change):     list, dict, set, bytearray
IMMUTABLE (can't change): int, float, str, tuple, frozenset, bytes

Why it matters:
- Mutable objects can't be dict keys or set elements
- Default mutable arguments are shared across calls (gotcha!)
- Immutable objects are hashable → can use in sets and dict keys
"""

# Gotcha: Mutable default argument
def bad(lst=[]):
    lst.append(1)
    return lst

# print(bad())  # [1]
# print(bad())  # [1, 1] — NOT [1]!

def good(lst=None):
    lst = lst or []
    lst.append(1)
    return lst


# ===========================================================================
# 2. DEEP COPY vs SHALLOW COPY
# ===========================================================================

import copy

original = [[1, 2], [3, 4]]

shallow = original.copy()  # or list(original) or original[:]
deep = copy.deepcopy(original)

original[0][0] = 99

print(f"Original: {original}")   # [[99, 2], [3, 4]]
print(f"Shallow: {shallow}")     # [[99, 2], [3, 4]] — inner list shared!
print(f"Deep: {deep}")           # [[1, 2], [3, 4]]  — fully independent!


# ===========================================================================
# 3. *args and **kwargs
# ===========================================================================

def example(*args, **kwargs):
    print(f"args: {args}")      # Tuple of positional args
    print(f"kwargs: {kwargs}")  # Dict of keyword args

example(1, 2, 3, name="Akram", age=25)

# Unpacking
def add(a, b, c):
    return a + b + c

nums = [1, 2, 3]
print(f"Unpacked: {add(*nums)}")  # 6

config = {"a": 1, "b": 2, "c": 3}
print(f"Unpacked: {add(**config)}")  # 6


# ===========================================================================
# 4. DECORATORS — Concise Review
# ===========================================================================

import functools

def decorator(func):
    @functools.wraps(func)  # Preserves metadata
    def wrapper(*args, **kwargs):
        # Before
        result = func(*args, **kwargs)
        # After
        return result
    return wrapper

# @decorator is syntactic sugar for: func = decorator(func)

# Decorator with arguments needs extra layer:
def repeat(n):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return [func(*args, **kwargs) for _ in range(n)]
        return wrapper
    return decorator

@repeat(3)
def greet(name):
    return f"Hi {name}"

print(f"\n{greet('Akram')}")


# ===========================================================================
# 5. GENERATORS — Concise Review
# ===========================================================================

# yield makes a function a generator
def counter(n):
    i = 0
    while i < n:
        yield i  # Pauses here, returns value
        i += 1

# Benefits: Memory efficient (lazy), can represent infinite sequences
# Key: Can only iterate ONCE

gen = counter(5)
print(f"\nGenerator: {list(gen)}")
print(f"Exhausted: {list(gen)}")  # [] — empty!

# Generator expression
squares = (x**2 for x in range(10))


# ===========================================================================
# 6. GIL (Global Interpreter Lock)
# ===========================================================================
"""
What: A mutex that allows only ONE thread to execute Python bytecode at a time.

Impact:
  - CPU-bound: Threads don't help → use multiprocessing
  - I/O-bound: Threads still help (GIL released during I/O) → use threading/asyncio

Solutions for CPU-bound:
  1. multiprocessing (separate processes, each has own GIL)
  2. C extensions (NumPy releases GIL during computation)
  3. Sub-interpreters (Python 3.12+)
"""


# ===========================================================================
# 7. ASYNC/AWAIT — Key Points
# ===========================================================================
"""
- asyncio is for I/O-bound concurrency (NOT CPU-bound)
- Single-threaded, event-loop based (like Node.js)
- await suspends coroutine, lets other tasks run
- asyncio.gather() = Promise.all()
- asyncio.create_task() = fire and forget

When to use what:
  I/O-bound → asyncio (or threading)
  CPU-bound → multiprocessing
  Simple concurrency → threading
"""


# ===========================================================================
# 8. OOP QUICK REFERENCE
# ===========================================================================

# MRO (Method Resolution Order) — C3 linearization
# class D(B, C): → D → B → C → A → object

# @classmethod: Works on class, not instance. Used for alt constructors
# @staticmethod: Utility function. No access to cls or self
# @property: Getter/setter with attribute syntax

# __init__: Constructor
# __str__: User-friendly string (print)
# __repr__: Developer string (debugger)
# __eq__: Equality comparison
# __hash__: Make hashable (needed for sets/dict keys)
# __len__: len(obj)
# __iter__: Make iterable
# __getitem__: obj[key]
# __contains__: 'in' operator

class Example:
    count = 0  # Class variable
    
    def __init__(self, value):
        self.value = value  # Instance variable
        Example.count += 1
    
    @classmethod
    def from_string(cls, s):
        return cls(int(s))
    
    @staticmethod
    def validate(value):
        return isinstance(value, int) and value > 0
    
    @property
    def double(self):
        return self.value * 2

    def __str__(self):
        return f"Example({self.value})"

    def __eq__(self, other):
        return self.value == other.value
    
    def __lt__(self, other):
        return self.value < other.value


# ===========================================================================
# 9. COMMON PATTERNS & TRICKS
# ===========================================================================

print(f"\n--- Common Patterns ---")

# Swap variables
a, b = 1, 2
a, b = b, a

# Ternary
x = "yes" if True else "no"

# Chained comparison
assert 1 < 2 < 3  # Works in Python!

# Walrus operator (:=)
import random
if (n := random.randint(1, 10)) > 5:
    print(f"  Got {n} (> 5)")

# Dictionary dispatch (replace if/elif chains)
def handle_add(a, b): return a + b
def handle_sub(a, b): return a - b
def handle_mul(a, b): return a * b

operations = {
    "add": handle_add,
    "sub": handle_sub,
    "mul": handle_mul,
}
result = operations["add"](5, 3)
print(f"  Dispatch: {result}")

# Defaultdict for grouping
from collections import defaultdict
groups = defaultdict(list)
for item in [("a", 1), ("b", 2), ("a", 3)]:
    groups[item[0]].append(item[1])
print(f"  Groups: {dict(groups)}")

# Counter for frequency
from collections import Counter
freq = Counter("abracadabra")
print(f"  Freq: {freq.most_common(3)}")

# zip for parallel iteration
names = ["a", "b", "c"]
scores = [1, 2, 3]
combined = dict(zip(names, scores))
print(f"  Zipped: {combined}")

# enumerate for index + value
for i, v in enumerate(["x", "y", "z"], start=1):
    print(f"  {i}: {v}")


# ===========================================================================
# 10. COMPLEXITY CHEAT SHEET
# ===========================================================================
"""
Operation                  | List      | Dict/Set  | Notes
========================== | ========= | ========= | ========
Access by index            | O(1)      | N/A       |
Search (in)                | O(n)      | O(1) avg  | Dicts use hash tables
Append/Add                 | O(1)      | O(1) avg  |
Insert at beginning        | O(n)      | N/A       | Use deque for O(1)
Delete by value            | O(n)      | O(1) avg  |
Sort                       | O(n log n)| N/A       | Timsort
Min/Max                    | O(n)      | O(n)      |
List comprehension         | O(n)      | O(n)      |

Data structures to know:
  list        → Dynamic array
  dict        → Hash table
  set         → Hash table (keys only)
  deque       → Double-ended queue
  heapq       → Min-heap (priority queue)
  OrderedDict → Insertion-ordered dict (now default in 3.7+)
  defaultdict → Dict with default factory
  Counter     → Frequency counter
"""


# ===========================================================================
# 11. TOP 10 INTERVIEW QUESTIONS (Quick Answers)
# ===========================================================================
"""
Q1: Difference between list and tuple?
A:  List is mutable, tuple is immutable. Tuples are hashable (can be dict keys).

Q2: What is the GIL?
A:  Global Interpreter Lock — prevents true parallelism in threads for CPU-bound.
    Use multiprocessing for CPU, asyncio/threading for I/O.

Q3: How do decorators work?
A:  A decorator wraps a function: @dec is sugar for func = dec(func).
    Use @functools.wraps to preserve metadata.

Q4: What's the difference between == and is?
A:  == compares values, 'is' compares identity (same object in memory).

Q5: Explain generators.
A:  Functions that yield values lazily using 'yield'. Memory efficient.
    Can only iterate once. Created with yield or generator expressions.

Q6: What are *args and **kwargs?
A:  *args collects positional args as tuple, **kwargs as dict.
    * unpacks iterables, ** unpacks dicts.

Q7: How does Python handle memory?
A:  Reference counting + garbage collector (cycle detection).
    Small ints (-5 to 256) and short strings are cached.

Q8: Explain Python's MRO.
A:  Method Resolution Order — C3 linearization for multiple inheritance.
    Use ClassName.__mro__ to see the order.

Q9: What is EAFP?
A:  "Easier to Ask Forgiveness than Permission" — use try/except instead 
    of checking conditions first. Pythonic approach.

Q10: How does async/await work?
A:   Single-threaded event loop (like Node.js). await suspends coroutine,
     allowing other tasks to run. For I/O-bound, not CPU-bound.
"""


print("\n✅ Interview Cheatsheet Complete!")
print("📖 Review this before every interview!")
