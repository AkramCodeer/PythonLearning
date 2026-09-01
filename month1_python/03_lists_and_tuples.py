"""
===============================================================================
 MODULE 03: LISTS & TUPLES
===============================================================================
 Lists ≈ JS Arrays (mutable), Tuples ≈ Frozen Arrays (immutable)
 
 Run this file:  python 03_lists_and_tuples.py
===============================================================================
"""

# ===========================================================================
# 1. LISTS — Python's Version of JS Arrays
# ===========================================================================

# Creating lists (JS: const arr = [1, 2, 3])
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", True, 3.14, None]  # Can mix types (like JS)
empty = []
from_range = list(range(1, 11))  # [1, 2, 3, ..., 10]

print(f"numbers: {numbers}")
print(f"mixed: {mixed}")
print(f"from_range: {from_range}")
print(f"Length: {len(numbers)}")  # JS: numbers.length


# ===========================================================================
# 2. ACCESSING ELEMENTS
# ===========================================================================

fruits = ["apple", "banana", "cherry", "date", "elderberry"]

print(f"\n--- Accessing ---")
print(f"First: {fruits[0]}")          # apple
print(f"Last: {fruits[-1]}")          # elderberry (Python special! JS: fruits.at(-1))
print(f"Second to last: {fruits[-2]}")  # date

# Slicing (same as string slicing!)
print(f"First 3: {fruits[:3]}")        # ['apple', 'banana', 'cherry']
print(f"Last 2: {fruits[-2:]}")        # ['date', 'elderberry']
print(f"Middle: {fruits[1:4]}")        # ['banana', 'cherry', 'date']
print(f"Every 2nd: {fruits[::2]}")     # ['apple', 'cherry', 'elderberry']
print(f"Reversed: {fruits[::-1]}")     # Reversed list!


# ===========================================================================
# 3. MODIFYING LISTS
# ===========================================================================

print(f"\n--- Modifying ---")
colors = ["red", "green", "blue"]

# Add elements
colors.append("yellow")               # JS: push() — adds to end
print(f"After append: {colors}")

colors.insert(1, "orange")            # JS: splice(1, 0, "orange")
print(f"After insert at 1: {colors}")

colors.extend(["purple", "pink"])      # JS: push(...otherArray) or concat()
print(f"After extend: {colors}")

# Remove elements
colors.remove("orange")               # Remove by VALUE (first occurrence)
print(f"After remove 'orange': {colors}")

popped = colors.pop()                  # JS: pop() — removes & returns last
print(f"Popped: {popped}, List: {colors}")

popped_at = colors.pop(1)             # JS: splice(1, 1)[0] — remove at index
print(f"Popped at 1: {popped_at}, List: {colors}")

# del keyword — remove by index or slice
del colors[0]                          # Remove first element
print(f"After del [0]: {colors}")

# Clear entire list
# colors.clear()                       # JS: arr.length = 0

# Replace a slice
nums = [1, 2, 3, 4, 5]
nums[1:3] = [20, 30]                  # Replace index 1-2
print(f"After slice replace: {nums}")  # [1, 20, 30, 4, 5]


# ===========================================================================
# 4. LIST METHODS
# ===========================================================================

print(f"\n--- List Methods ---")

nums = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]

# Sorting
nums_sorted = sorted(nums)            # Returns NEW sorted list (like JS [...arr].sort())
print(f"sorted(): {nums_sorted}")

nums.sort()                            # Sorts IN PLACE (like JS arr.sort())
print(f"sort(): {nums}")

nums.sort(reverse=True)               # Sort descending
print(f"sort(reverse): {nums}")

# Reverse
nums.reverse()                         # In place (JS: arr.reverse())
print(f"reverse(): {nums}")

# Count & Index
print(f"count(5): {nums.count(5)}")    # How many times 5 appears
print(f"index(9): {nums.index(9)}")    # First index of 9

# Copy (shallow)
original = [1, 2, 3]
copy1 = original.copy()               # JS: [...arr] or arr.slice()
copy2 = original[:]                    # Another way to copy
copy3 = list(original)                 # Yet another way

original.append(4)
print(f"\nOriginal: {original}, Copy: {copy1}")  # Copy not affected!


# ===========================================================================
# 5. LIST OPERATIONS
# ===========================================================================

print(f"\n--- Operations ---")

# Concatenation
list1 = [1, 2, 3]
list2 = [4, 5, 6]
combined = list1 + list2               # JS: [...list1, ...list2]
print(f"Concatenated: {combined}")

# Repetition
repeated = [0] * 5                     # [0, 0, 0, 0, 0]
print(f"Repeated: {repeated}")

# Membership
print(f"3 in [1,2,3]: {3 in [1, 2, 3]}")        # True (JS: includes())
print(f"4 not in [1,2,3]: {4 not in [1, 2, 3]}")  # True

# Min, Max, Sum
nums = [10, 5, 8, 3, 12]
print(f"min: {min(nums)}, max: {max(nums)}, sum: {sum(nums)}")

# All & Any (like JS .every() and .some())
print(f"all > 0: {all(n > 0 for n in nums)}")    # JS: nums.every(n => n > 0)
print(f"any > 10: {any(n > 10 for n in nums)}")  # JS: nums.some(n => n > 10)


# ===========================================================================
# 6. UNPACKING (Destructuring — like JS!)
# ===========================================================================

print(f"\n--- Unpacking ---")

# JS: const [a, b, c] = [1, 2, 3]
# Py:
a, b, c = [1, 2, 3]
print(f"a={a}, b={b}, c={c}")

# JS: const [first, ...rest] = [1, 2, 3, 4, 5]
# Py: Uses * (star) instead of ... (spread)
first, *rest = [1, 2, 3, 4, 5]
print(f"first={first}, rest={rest}")   # first=1, rest=[2, 3, 4, 5]

first, *middle, last = [1, 2, 3, 4, 5]
print(f"first={first}, middle={middle}, last={last}")  # 1, [2,3,4], 5

# Ignore values with _
_, second, *_ = [1, 2, 3, 4, 5]
print(f"second: {second}")


# ===========================================================================
# 7. NESTED LISTS (2D Arrays)
# ===========================================================================

print(f"\n--- Nested Lists ---")

matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

print(f"matrix[1][2] = {matrix[1][2]}")  # 6 (row 1, col 2)

# Flatten a 2D list
flat = [num for row in matrix for num in row]
print(f"Flattened: {flat}")  # [1, 2, 3, 4, 5, 6, 7, 8, 9]


# ===========================================================================
# 8. TUPLES — Immutable Lists
# ===========================================================================

print(f"\n--- Tuples ---")

# Tuples are like lists but CANNOT be modified after creation
# JS: Object.freeze([1, 2, 3]) — closest equivalent

coords = (10, 20)                      # Parentheses (or without them!)
single = (42,)                         # Single-element tuple NEEDS trailing comma!
not_a_tuple = (42)                     # This is just an int, not a tuple!
empty_tuple = ()
from_list = tuple([1, 2, 3])          # Convert list to tuple

print(f"coords: {coords}, type: {type(coords)}")
print(f"single: {single}, type: {type(single)}")
print(f"not_a_tuple: {not_a_tuple}, type: {type(not_a_tuple)}")

# Accessing (same as lists)
print(f"coords[0]: {coords[0]}")
print(f"coords[-1]: {coords[-1]}")

# Tuples are IMMUTABLE
# coords[0] = 5  # ❌ TypeError!

# Tuple unpacking (very common in Python!)
x, y = coords
print(f"x={x}, y={y}")

# Tuple methods (only 2!)
nums_tuple = (1, 2, 3, 2, 1)
print(f"count(2): {nums_tuple.count(2)}")  # 2
print(f"index(3): {nums_tuple.index(3)}")  # 2

# Named tuples (like a lightweight class)
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])
p = Point(10, 20)
print(f"\nNamedTuple: {p}")
print(f"p.x={p.x}, p.y={p.y}")


# ===========================================================================
# 9. WHEN TO USE LIST vs TUPLE
# ===========================================================================
"""
Use LISTS when:
  - You need to add, remove, or change items
  - The data is homogeneous (all same type)
  - Example: list of users, list of scores

Use TUPLES when:
  - Data shouldn't change (coordinates, RGB colors, database rows)
  - Returning multiple values from a function
  - Dictionary keys (lists can't be dict keys, tuples can!)
  - Performance matters (tuples are slightly faster)
"""

# Tuples as dict keys (lists CAN'T do this!)
locations = {
    (40.7128, -74.0060): "New York",
    (51.5074, -0.1278): "London"
}
print(f"\nLocation lookup: {locations[(40.7128, -74.0060)]}")


# ===========================================================================
# 10. USEFUL FUNCTIONS WITH LISTS/TUPLES
# ===========================================================================

print(f"\n--- Useful Functions ---")

# enumerate — get index AND value (like JS .forEach((item, index) => {}))
fruits = ["apple", "banana", "cherry"]
for index, fruit in enumerate(fruits):
    print(f"  {index}: {fruit}")

# zip — combine two lists (no direct JS equivalent)
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]
for name, age in zip(names, ages):
    print(f"  {name} is {age}")

# map with list (JS: arr.map())
numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, numbers))
print(f"Doubled: {doubled}")

# filter (JS: arr.filter())
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(f"Evens: {evens}")

# sorted with key
words = ["banana", "Apple", "cherry", "Date"]
sorted_words = sorted(words, key=str.lower)  # Case-insensitive sort
print(f"Sorted: {sorted_words}")


# ===========================================================================
# 🏋️ PRACTICE EXERCISES
# ===========================================================================
"""
1. Create a list of 10 numbers. Find the sum, average, min, and max.

2. Given a list [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], use slicing to get:
   - First 5 elements
   - Last 3 elements
   - Every other element
   - The list reversed

3. Write code to remove all duplicates from [1, 2, 2, 3, 3, 3, 4, 4, 4, 4].

4. Given two lists names = ["a", "b", "c"] and scores = [90, 80, 70],
   create a list of tuples: [("a", 90), ("b", 80), ("c", 70)]

5. Unpack this tuple: data = ("Akram", 25, "Developer", "Hyderabad")
   into name, age, role, city variables.

6. Flatten this nested list: [[1, 2], [3, 4], [5, 6]] into [1, 2, 3, 4, 5, 6]

7. Sort a list of tuples [(3, 'c'), (1, 'a'), (2, 'b')] by the first element.

8. Find the second largest number in a list without using sort().
"""

print("\n✅ Module 03 Complete!")
