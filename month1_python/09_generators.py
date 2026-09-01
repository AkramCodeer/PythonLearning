"""
===============================================================================
 MODULE 09: GENERATORS
===============================================================================
 ⭐ HIGH INTERVIEW IMPORTANCE — Lazy evaluation for memory-efficient code
 
 Run this file:  python 09_generators.py
===============================================================================
"""

# ===========================================================================
# 1. WHAT IS A GENERATOR?
# ===========================================================================
"""
A generator is a function that produces a SEQUENCE of values lazily
(one at a time) instead of creating them all at once.

Think of it like:
- Regular function: Makes a full meal, serves it all at once
- Generator function: Makes each dish only when you ask for the next one

JS equivalent: function* (generator functions) — same concept!
"""


# ===========================================================================
# 2. REGULAR FUNCTION vs GENERATOR
# ===========================================================================

# Regular function — creates ENTIRE list in memory
def get_squares_list(n):
    result = []
    for i in range(n):
        result.append(i ** 2)
    return result

# Generator function — creates values ONE AT A TIME
def get_squares_gen(n):
    for i in range(n):
        yield i ** 2  # 'yield' instead of 'return'

# Using the regular function
squares_list = get_squares_list(5)
print(f"List: {squares_list}")          # [0, 1, 4, 9, 16]
print(f"Type: {type(squares_list)}")    # <class 'list'>

# Using the generator
squares_gen = get_squares_gen(5)
print(f"\nGenerator: {squares_gen}")        # <generator object ...>
print(f"Type: {type(squares_gen)}")         # <class 'generator'>

# Get values one at a time with next()
print(f"next(): {next(squares_gen)}")   # 0
print(f"next(): {next(squares_gen)}")   # 1
print(f"next(): {next(squares_gen)}")   # 4

# Or iterate with for loop (most common)
squares_gen2 = get_squares_gen(5)
print("\nFor loop:")
for sq in squares_gen2:
    print(f"  {sq}")


# ===========================================================================
# 3. HOW GENERATORS WORK INTERNALLY
# ===========================================================================

print(f"\n--- How Generators Work ---")

def counting_gen():
    print("  Starting...")
    yield 1                    # Pauses here, returns 1
    print("  Resuming after 1...")
    yield 2                    # Pauses here, returns 2
    print("  Resuming after 2...")
    yield 3                    # Pauses here, returns 3
    print("  Done!")           # No more yields → StopIteration

gen = counting_gen()
print(f"First: {next(gen)}")   # "Starting..." then returns 1
print(f"Second: {next(gen)}")  # "Resuming after 1..." then returns 2
print(f"Third: {next(gen)}")   # "Resuming after 2..." then returns 3

# next(gen) would raise StopIteration
# for loop handles this automatically!


# ===========================================================================
# 4. WHY USE GENERATORS? — Memory Efficiency!
# ===========================================================================

print(f"\n--- Memory Efficiency ---")

import sys

# List: ALL values in memory at once
big_list = [x for x in range(1000000)]
print(f"List size: {sys.getsizeof(big_list):,} bytes")  # ~8 MB!

# Generator: ONE value at a time
big_gen = (x for x in range(1000000))
print(f"Generator size: {sys.getsizeof(big_gen)} bytes")  # ~200 bytes!

# Same result, fraction of memory!
list_sum = sum([x for x in range(1000000)])
gen_sum = sum(x for x in range(1000000))
print(f"Sums match: {list_sum == gen_sum}")


# ===========================================================================
# 5. GENERATOR EXPRESSIONS (Like List Comprehensions)
# ===========================================================================

print(f"\n--- Generator Expressions ---")

# List comprehension: [expr for item in iterable]   → creates list
# Generator expression: (expr for item in iterable)  → creates generator

# Just replace [] with ()!
squares_list = [x**2 for x in range(10)]   # List (stored in memory)
squares_gen = (x**2 for x in range(10))    # Generator (lazy)

print(f"List: {squares_list}")
print(f"Generator: {squares_gen}")  # <generator object>

# Common use: pass directly to functions
total = sum(x**2 for x in range(100))    # No need for extra parentheses!
print(f"Sum of squares: {total}")

# Find maximum
max_val = max(len(word) for word in ["hello", "world", "python"])
print(f"Max word length: {max_val}")

# Check conditions
all_positive = all(x > 0 for x in [1, 2, 3, 4])
any_negative = any(x < 0 for x in [1, -2, 3])
print(f"All positive: {all_positive}")
print(f"Any negative: {any_negative}")


# ===========================================================================
# 6. PRACTICAL GENERATOR EXAMPLES
# ===========================================================================

print(f"\n--- Practical Examples ---")

# --- Infinite Counter ---
def infinite_counter(start=0):
    """Count forever — only possible with generators!"""
    n = start
    while True:
        yield n
        n += 1

counter = infinite_counter(1)
print(f"Counter: {next(counter)}, {next(counter)}, {next(counter)}")

# --- Fibonacci Generator ---
def fibonacci():
    """Generate infinite Fibonacci sequence."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

fib = fibonacci()
first_10 = [next(fib) for _ in range(10)]
print(f"Fibonacci: {first_10}")

# --- File Reader (line by line) ---
def read_lines(filename):
    """Read a file line by line without loading entire file."""
    try:
        with open(filename) as f:
            for line in f:
                yield line.strip()
    except FileNotFoundError:
        print(f"  File {filename} not found")

# --- Chunked Data Processing ---
def chunked(data, chunk_size):
    """Process data in chunks — great for API pagination!"""
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]

data = list(range(1, 21))
for chunk in chunked(data, 5):
    print(f"  Chunk: {chunk}")

# --- Flattening Nested Data ---
def flatten(nested):
    """Flatten any nested structure."""
    for item in nested:
        if isinstance(item, (list, tuple)):
            yield from flatten(item)  # yield from — delegate to sub-generator!
        else:
            yield item

nested = [1, [2, 3], [4, [5, 6]], [7, [8, [9]]]]
print(f"Flattened: {list(flatten(nested))}")


# ===========================================================================
# 7. GENERATOR METHODS: send(), throw(), close()
# ===========================================================================

print(f"\n--- Generator Methods ---")

# --- send() — Send values INTO the generator ---
def accumulator():
    """A generator that accumulates values sent to it."""
    total = 0
    while True:
        value = yield total    # yield returns sent value
        if value is not None:
            total += value

acc = accumulator()
next(acc)              # Initialize (must call next() first!)
print(f"Send 10: {acc.send(10)}")   # 10
print(f"Send 20: {acc.send(20)}")   # 30
print(f"Send 5: {acc.send(5)}")     # 35

# --- close() — Stop the generator ---
def counter_gen():
    i = 0
    while True:
        yield i
        i += 1

c = counter_gen()
print(f"\nCounter: {next(c)}, {next(c)}, {next(c)}")
c.close()  # Stop the generator
# next(c) would raise StopIteration


# ===========================================================================
# 8. yield from — Delegating to Sub-Generators
# ===========================================================================

print(f"\n--- yield from ---")

# Without yield from:
def chain_old(*iterables):
    for it in iterables:
        for item in it:
            yield item

# With yield from (cleaner!):
def chain(*iterables):
    for it in iterables:
        yield from it  # Delegates to the sub-iterable

result = list(chain([1, 2], [3, 4], [5, 6]))
print(f"Chained: {result}")

# yield from also works with generators
def sub_gen():
    yield "a"
    yield "b"

def main_gen():
    yield 1
    yield from sub_gen()  # Inserts a, b here
    yield 2

print(f"yield from: {list(main_gen())}")  # [1, 'a', 'b', 2]


# ===========================================================================
# 9. GENERATOR PIPELINE (Real-World Pattern!)
# ===========================================================================

print(f"\n--- Generator Pipeline ---")

# Chain generators together like Unix pipes: cmd1 | cmd2 | cmd3
# Each stage processes one item at a time — very memory efficient!

def generate_numbers(n):
    """Stage 1: Generate numbers"""
    for i in range(1, n + 1):
        yield i

def filter_evens(numbers):
    """Stage 2: Keep only even numbers"""
    for n in numbers:
        if n % 2 == 0:
            yield n

def square(numbers):
    """Stage 3: Square each number"""
    for n in numbers:
        yield n ** 2

def add_label(numbers):
    """Stage 4: Add labels"""
    for n in numbers:
        yield f"Value: {n}"

# Build the pipeline
pipeline = add_label(square(filter_evens(generate_numbers(20))))

# Process — each value flows through ALL stages one at a time
for item in pipeline:
    print(f"  {item}")


# ===========================================================================
# 10. COMPARING: LIST vs GENERATOR vs ITERATOR
# ===========================================================================
"""
List:
  - All values in memory at once
  - Can access by index, iterate multiple times
  - Created with [] or list()

Generator:
  - Values computed on-the-fly (lazy)
  - Can only iterate ONCE
  - Created with yield or () expression

Iterator:
  - Any object with __iter__ and __next__ methods
  - Generators are a type of iterator
  - Created with iter() or by implementing the protocol

When to use:
  ✅ Generator: Large datasets, infinite sequences, pipelines
  ✅ List: Need random access, multiple iterations, small data
"""


# ===========================================================================
# 11. itertools — Generator Power Tools!
# ===========================================================================

print(f"\n--- itertools ---")

import itertools

# count — infinite counter
counter = itertools.count(start=1, step=2)  # 1, 3, 5, 7, ...
print(f"count: {[next(counter) for _ in range(5)]}")

# cycle — infinite cycle through iterable
colors = itertools.cycle(["red", "green", "blue"])
print(f"cycle: {[next(colors) for _ in range(7)]}")

# islice — slice a generator (can't use [:] on generators!)
fib = fibonacci()
first_15 = list(itertools.islice(fib, 15))
print(f"First 15 fib: {first_15}")

# chain — concatenate iterables
chained = list(itertools.chain([1, 2], [3, 4], [5, 6]))
print(f"chain: {chained}")

# product — cartesian product
pairs = list(itertools.product("AB", "12"))
print(f"product: {pairs}")

# combinations & permutations
combos = list(itertools.combinations("ABC", 2))
perms = list(itertools.permutations("AB", 2))
print(f"combinations: {combos}")
print(f"permutations: {perms}")

# groupby — group consecutive elements
data = [("A", 1), ("A", 2), ("B", 3), ("B", 4), ("A", 5)]
for key, group in itertools.groupby(data, key=lambda x: x[0]):
    print(f"  {key}: {list(group)}")


# ===========================================================================
# 🏋️ PRACTICE EXERCISES
# ===========================================================================
"""
1. Write a generator that yields powers of 2 (2, 4, 8, 16, 32, ...) infinitely.

2. Write a generator `take(n, iterable)` that yields the first n items.

3. Write a generator pipeline that:
   - Generates numbers 1-100
   - Filters multiples of 3
   - Squares them
   - Takes only the first 5

4. Write a generator that reads a large CSV file line by line and yields 
   dictionaries (simulate with a string if no file available).

5. Compare memory usage of a list vs generator for 10 million numbers.

6. ⭐ INTERVIEW: Explain the difference between a generator and an iterator.

7. ⭐ INTERVIEW: What happens when you call next() on an exhausted generator?

8. ⭐ INTERVIEW: Explain yield from and when you'd use it.
"""

print("\n✅ Module 09 Complete!")
