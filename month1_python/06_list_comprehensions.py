"""
===============================================================================
 MODULE 06: LIST COMPREHENSIONS
===============================================================================
 Python's most Pythonic feature — replaces map/filter in one clean line
 
 Run this file:  python 06_list_comprehensions.py
===============================================================================
"""

# ===========================================================================
# 1. BASIC LIST COMPREHENSION
# ===========================================================================

# JS:  [1,2,3,4,5].map(x => x * 2)
# Py:  [expression for item in iterable]

numbers = [1, 2, 3, 4, 5]

# Traditional loop way
doubled_loop = []
for n in numbers:
    doubled_loop.append(n * 2)

# List comprehension way (PREFERRED in Python!)
doubled = [n * 2 for n in numbers]
print(f"Doubled: {doubled}")  # [2, 4, 6, 8, 10]

# More examples
squares = [x**2 for x in range(1, 11)]
print(f"Squares: {squares}")  # [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

names = ["akram", "sarah", "john"]
upper_names = [name.upper() for name in names]
print(f"Upper: {upper_names}")

lengths = [len(name) for name in names]
print(f"Lengths: {lengths}")


# ===========================================================================
# 2. WITH CONDITION (Filter)
# ===========================================================================

# JS:  numbers.filter(x => x % 2 === 0)
# Py:  [expression for item in iterable if condition]

numbers = list(range(1, 21))

# Get even numbers
evens = [n for n in numbers if n % 2 == 0]
print(f"\nEvens: {evens}")

# Get numbers greater than 10
big = [n for n in numbers if n > 10]
print(f"Greater than 10: {big}")

# Combined: filter AND transform
# JS: numbers.filter(x => x % 2 === 0).map(x => x ** 2)
even_squares = [n**2 for n in numbers if n % 2 == 0]
print(f"Even squares: {even_squares}")

# Multiple conditions
divisible_by_3_and_5 = [n for n in range(1, 101) if n % 3 == 0 and n % 5 == 0]
print(f"Divisible by 3 AND 5: {divisible_by_3_and_5}")


# ===========================================================================
# 3. IF/ELSE IN COMPREHENSION
# ===========================================================================

# Note: if/else goes BEFORE for (when you want else)
# JS: numbers.map(x => x % 2 === 0 ? "even" : "odd")

labels = ["even" if n % 2 == 0 else "odd" for n in range(1, 11)]
print(f"\nLabels: {labels}")

# FizzBuzz in one line!
fizzbuzz = [
    "FizzBuzz" if n % 15 == 0 
    else "Fizz" if n % 3 == 0 
    else "Buzz" if n % 5 == 0 
    else str(n) 
    for n in range(1, 16)
]
print(f"FizzBuzz: {fizzbuzz}")


# ===========================================================================
# 4. NESTED COMPREHENSIONS
# ===========================================================================

print(f"\n--- Nested Comprehensions ---")

# Flatten a 2D list
# JS: matrix.flat() or [].concat(...matrix)
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [num for row in matrix for num in row]
print(f"Flattened: {flat}")

# Create a 2D matrix
grid = [[i * j for j in range(1, 4)] for i in range(1, 4)]
print(f"Grid: {grid}")  # [[1,2,3], [2,4,6], [3,6,9]]

# All pairs
pairs = [(x, y) for x in range(3) for y in range(3)]
print(f"Pairs: {pairs}")

# Cartesian product with condition
combos = [(x, y) for x in range(5) for y in range(5) if x != y]
print(f"Combos (x≠y): {combos[:8]}...")


# ===========================================================================
# 5. DICTIONARY COMPREHENSION
# ===========================================================================

print(f"\n--- Dict Comprehension ---")

# {key_expr: value_expr for item in iterable}

# Create a mapping
squares_dict = {x: x**2 for x in range(1, 6)}
print(f"Squares dict: {squares_dict}")

# Filter a dictionary
scores = {"Alice": 85, "Bob": 62, "Charlie": 91, "Diana": 78, "Eve": 55}
passed = {name: score for name, score in scores.items() if score >= 70}
print(f"Passed: {passed}")

# Swap keys and values
swapped = {v: k for k, v in scores.items()}
print(f"Swapped: {swapped}")

# From two lists
keys = ["name", "age", "city"]
values = ["Akram", 25, "Hyderabad"]
combined = {k: v for k, v in zip(keys, values)}
print(f"Combined: {combined}")

# Word lengths
words = ["hello", "world", "python", "ai"]
word_lengths = {word: len(word) for word in words}
print(f"Word lengths: {word_lengths}")


# ===========================================================================
# 6. SET COMPREHENSION
# ===========================================================================

print(f"\n--- Set Comprehension ---")

# {expr for item in iterable} — same as list but with {}

# Unique squares
squares_set = {x**2 for x in range(-5, 6)}
print(f"Unique squares: {squares_set}")

# Unique first letters
names = ["Alice", "Anna", "Bob", "Bella", "Charlie"]
first_letters = {name[0] for name in names}
print(f"First letters: {first_letters}")  # {'A', 'B', 'C'}


# ===========================================================================
# 7. GENERATOR EXPRESSIONS (Preview — more in Module 10)
# ===========================================================================

print(f"\n--- Generator Expression ---")

# Same as list comprehension but with () — LAZY evaluation!
# Doesn't create the whole list in memory

# List comprehension: creates list in memory
sum_of_squares_list = sum([x**2 for x in range(1000000)])

# Generator expression: generates values on-the-fly (much less memory!)
sum_of_squares_gen = sum(x**2 for x in range(1000000))

print(f"Sum (gen): {sum_of_squares_gen}")

# Check if any/all (using generator)
numbers = [2, 4, 6, 8, 10]
all_even = all(n % 2 == 0 for n in numbers)
any_gt_5 = any(n > 5 for n in numbers)
print(f"All even: {all_even}")
print(f"Any > 5: {any_gt_5}")


# ===========================================================================
# 8. WHEN TO USE / NOT USE COMPREHENSIONS
# ===========================================================================
"""
✅ USE comprehensions when:
  - Simple transformations or filters
  - Creating new lists/dicts/sets from existing data
  - Replacing simple map/filter operations

❌ DON'T use comprehensions when:
  - Logic is complex (more than 2-3 conditions)
  - You need error handling (try/except)
  - You need side effects (printing, API calls)
  - Readability suffers — ALWAYS prefer readable code!

Rule of thumb: If the comprehension doesn't fit on one line,
consider using a regular loop instead.
"""


# ===========================================================================
# 9. PRACTICAL EXAMPLES
# ===========================================================================

print(f"\n--- Practical Examples ---")

# 1. Extract emails from data
users = [
    {"name": "Akram", "email": "akram@gmail.com"},
    {"name": "Sara", "email": "sara@yahoo.com"},
    {"name": "Ali", "email": "ali@gmail.com"},
]
gmail_users = [u["name"] for u in users if u["email"].endswith("@gmail.com")]
print(f"Gmail users: {gmail_users}")

# 2. Parse CSV-like data
csv_data = "Akram,25,Hyderabad\nSara,28,Mumbai\nAli,30,Delhi"
parsed = [line.split(",") for line in csv_data.split("\n")]
print(f"Parsed CSV: {parsed}")

# 3. Clean and normalize data
raw = ["  Hello  ", "WORLD", "  python  ", "  AI "]
cleaned = [s.strip().lower() for s in raw]
print(f"Cleaned: {cleaned}")

# 4. Create lookup table
products = [("laptop", 999), ("phone", 699), ("tablet", 499)]
price_lookup = {name: price for name, price in products}
print(f"Price lookup: {price_lookup}")

# 5. Matrix transpose
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
transposed = [[row[i] for row in matrix] for i in range(3)]
print(f"Transposed: {transposed}")


# ===========================================================================
# 🏋️ PRACTICE EXERCISES
# ===========================================================================
"""
1. Create a list of squares of even numbers from 1 to 20.

2. Given words = ["hello", "world", "Python", "is", "great"],
   create a list of words longer than 3 characters, in uppercase.

3. Given a string "Hello World 123", extract only the digits as integers.

4. Create a dict comprehension that maps each letter in "hello" to its 
   ASCII value (use ord()).

5. Flatten and sort: [[3,1], [5,2], [4,6]] → [1, 2, 3, 4, 5, 6]

6. Given a list of temperatures in Celsius [0, 10, 20, 30, 40],
   convert to Fahrenheit using: F = C * 9/5 + 32

7. Create a list of (number, square, cube) tuples for numbers 1-10.

8. Given a sentence, create a dict of {word: length} but only for 
   words with length > 3.

9. Remove all vowels from a string using a list comprehension + join.

10. FizzBuzz from 1-30 using a list comprehension.
"""

print("\n✅ Module 06 Complete!")
