"""
===============================================================================
 MODULE 07: FUNCTIONS
===============================================================================
 Functions in Python — your JS function knowledge transfers well!
 
 Run this file:  python 07_functions.py
===============================================================================
"""

# ===========================================================================
# 1. BASIC FUNCTIONS
# ===========================================================================

# JS: function greet(name) { return `Hello ${name}`; }
# Py:
def greet(name):
    """Greet a person by name."""  # This is a docstring — like JSDoc
    return f"Hello {name}!"

print(greet("Akram"))

# Function with no return (returns None automatically)
# JS: function that doesn't return → returns undefined
# Py: function that doesn't return → returns None
def say_hello():
    print("Hello!")

result = say_hello()
print(f"Return value: {result}")  # None


# ===========================================================================
# 2. PARAMETERS & ARGUMENTS
# ===========================================================================

print(f"\n--- Parameters ---")

# --- Default Parameters ---
# JS: function greet(name = "World") { ... }
# Py:
def greet_default(name="World"):
    return f"Hello {name}!"

print(greet_default())           # Hello World!
print(greet_default("Akram"))    # Hello Akram!

# --- Keyword Arguments ---
# Python lets you name your arguments (JS doesn't have this!)
def create_user(name, age, city="Unknown"):
    return {"name": name, "age": age, "city": city}

# All these work:
user1 = create_user("Akram", 25, "Hyderabad")
user2 = create_user("Akram", age=25)               # Named argument
user3 = create_user(age=25, name="Akram")           # Order doesn't matter!
user4 = create_user("Akram", city="Mumbai", age=30) # Mix positional and named

print(f"User1: {user1}")
print(f"User3: {user3}")

# --- *args — Variable positional arguments ---
# JS: function sum(...numbers) { ... }  (rest params)
# Py:
def sum_all(*args):
    """Accept any number of positional arguments."""
    print(f"  args = {args}")  # It's a tuple!
    return sum(args)

print(f"\nsum_all(1,2,3): {sum_all(1, 2, 3)}")
print(f"sum_all(1,2,3,4,5): {sum_all(1, 2, 3, 4, 5)}")

# --- **kwargs — Variable keyword arguments ---
# JS: function config({...options}) (destructured object)
# Py:
def print_info(**kwargs):
    """Accept any number of keyword arguments."""
    print(f"  kwargs = {kwargs}")  # It's a dict!
    for key, value in kwargs.items():
        print(f"    {key}: {value}")

print(f"\nprint_info:")
print_info(name="Akram", age=25, role="Developer")

# --- Combining all parameter types ---
def complex_function(required, *args, default="hi", **kwargs):
    print(f"  required: {required}")
    print(f"  args: {args}")
    print(f"  default: {default}")
    print(f"  kwargs: {kwargs}")

print(f"\nComplex function:")
complex_function("must", 1, 2, 3, default="hello", extra="data")


# ===========================================================================
# 3. RETURN VALUES
# ===========================================================================

print(f"\n--- Return Values ---")

# Return multiple values (Python special — no JS equivalent!)
def get_min_max(numbers):
    return min(numbers), max(numbers)  # Returns a tuple

minimum, maximum = get_min_max([3, 1, 4, 1, 5, 9])
print(f"Min: {minimum}, Max: {maximum}")

# Return a dict (common pattern — like returning an object in JS)
def calculate(a, b):
    return {
        "sum": a + b,
        "diff": a - b,
        "product": a * b,
        "quotient": a / b if b != 0 else None
    }

result = calculate(10, 3)
print(f"Calculate: {result}")


# ===========================================================================
# 4. LAMBDA FUNCTIONS (Arrow Functions)
# ===========================================================================

print(f"\n--- Lambda Functions ---")

# JS: const double = (x) => x * 2
# Py: lambda arguments: expression (ONE expression only!)

double = lambda x: x * 2
print(f"double(5): {double(5)}")

add = lambda x, y: x + y
print(f"add(3, 4): {add(3, 4)}")

# Most useful with map, filter, sorted
numbers = [1, 2, 3, 4, 5]

doubled = list(map(lambda x: x * 2, numbers))
print(f"map doubled: {doubled}")

evens = list(filter(lambda x: x % 2 == 0, numbers))
print(f"filter evens: {evens}")

# Sort by custom key
students = [("Alice", 88), ("Bob", 95), ("Charlie", 72)]
by_score = sorted(students, key=lambda s: s[1], reverse=True)
print(f"By score: {by_score}")

# ⚠️ Lambda limitations:
# - Only ONE expression (no statements, no loops)
# - No type annotations
# - Hard to debug (no name in stack trace)
# Prefer regular functions for anything complex!


# ===========================================================================
# 5. HIGHER-ORDER FUNCTIONS
# ===========================================================================

print(f"\n--- Higher-Order Functions ---")

# Functions that take or return other functions
# JS: const numbers = [1,2,3].map(x => x * 2)
# Py:

# map() — transform each element
# JS: arr.map(fn)
names = ["akram", "sara", "ali"]
upper = list(map(str.upper, names))
print(f"map upper: {upper}")

# filter() — keep elements that pass test
# JS: arr.filter(fn)
numbers = range(1, 21)
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(f"filter evens: {evens}")

# reduce() — accumulate values
# JS: arr.reduce((acc, val) => acc + val, 0)
from functools import reduce
total = reduce(lambda acc, x: acc + x, [1, 2, 3, 4, 5])
print(f"reduce sum: {total}")

product = reduce(lambda acc, x: acc * x, [1, 2, 3, 4, 5])
print(f"reduce product: {product}")

# BUT — Python prefers comprehensions over map/filter!
# Instead of: list(map(lambda x: x*2, numbers))
# Prefer:     [x*2 for x in numbers]

# Function that returns a function (closure)
# JS: const multiplier = (factor) => (n) => n * factor
def multiplier(factor):
    def multiply(n):
        return n * factor
    return multiply

double = multiplier(2)
triple = multiplier(3)
print(f"\ndouble(5): {double(5)}")   # 10
print(f"triple(5): {triple(5)}")      # 15


# ===========================================================================
# 6. SCOPE — LEGB Rule
# ===========================================================================

print(f"\n--- Scope ---")

# Python scope order: Local → Enclosing → Global → Built-in
# JS scope: Block (let/const) → Function → Global

x = "global"  # Global scope

def outer():
    x = "enclosing"  # Enclosing scope
    
    def inner():
        x = "local"  # Local scope
        print(f"  Inner: {x}")
    
    inner()
    print(f"  Outer: {x}")

outer()
print(f"  Global: {x}")

# To modify global variable from inside function
counter = 0

def increment():
    global counter  # Without this, you'd get UnboundLocalError
    counter += 1

increment()
increment()
print(f"\nGlobal counter: {counter}")  # 2

# nonlocal — modify enclosing scope variable
def outer_fn():
    count = 0
    
    def inner_fn():
        nonlocal count  # Refers to outer_fn's count
        count += 1
        return count
    
    return inner_fn

counter_fn = outer_fn()
print(f"Counter: {counter_fn()}")  # 1
print(f"Counter: {counter_fn()}")  # 2
print(f"Counter: {counter_fn()}")  # 3


# ===========================================================================
# 7. TYPE HINTS (Type Annotations)
# ===========================================================================

print(f"\n--- Type Hints ---")

# JS: TypeScript types (function add(a: number, b: number): number)
# Py: Type hints (not enforced at runtime, but great for IDE support!)

def add_typed(a: int, b: int) -> int:
    return a + b

def greet_typed(name: str, times: int = 1) -> str:
    return f"Hello {name}! " * times

# Using typing module for complex types
from typing import Optional, Union

def find_user(user_id: int) -> Optional[dict]:
    """Returns user dict or None if not found."""
    users = {1: {"name": "Akram"}}
    return users.get(user_id)

def process(value: Union[str, int]) -> str:
    """Accepts string or int."""
    return str(value)

# List, Dict, Tuple type hints
def process_data(items: list[str]) -> dict[str, int]:
    return {item: len(item) for item in items}

result = process_data(["hello", "world"])
print(f"Typed result: {result}")


# ===========================================================================
# 8. DOCSTRINGS
# ===========================================================================

def calculate_area(length: float, width: float) -> float:
    """
    Calculate the area of a rectangle.
    
    Args:
        length: The length of the rectangle.
        width: The width of the rectangle.
    
    Returns:
        The area as a float.
    
    Raises:
        ValueError: If length or width is negative.
    
    Example:
        >>> calculate_area(5, 3)
        15.0
    """
    if length < 0 or width < 0:
        raise ValueError("Dimensions must be positive")
    return float(length * width)

# Access the docstring
print(f"\nDocstring: {calculate_area.__doc__[:50]}...")
help(calculate_area)  # Pretty-prints the docstring


# ===========================================================================
# 9. USEFUL PATTERNS
# ===========================================================================

print(f"\n--- Useful Patterns ---")

# Memoization with default mutable argument
def fibonacci(n, cache={}):
    if n in cache:
        return cache[n]
    if n <= 1:
        return n
    cache[n] = fibonacci(n-1, cache) + fibonacci(n-2, cache)
    return cache[n]

print(f"fib(10): {fibonacci(10)}")
print(f"fib(20): {fibonacci(20)}")

# Function as a value (first-class functions — same as JS)
def apply_operation(func, a, b):
    return func(a, b)

print(f"add: {apply_operation(lambda a, b: a + b, 5, 3)}")
print(f"mul: {apply_operation(lambda a, b: a * b, 5, 3)}")

# Default mutable argument gotcha!
# ❌ WRONG:
def append_to(item, lst=[]):
    lst.append(item)
    return lst

# The default list is shared across calls!
print(f"\nGotcha: {append_to(1)}")  # [1]
print(f"Gotcha: {append_to(2)}")    # [1, 2] — NOT [2]!

# ✅ CORRECT:
def append_to_fixed(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst

print(f"Fixed: {append_to_fixed(1)}")  # [1]
print(f"Fixed: {append_to_fixed(2)}")  # [2] — correct!


# ===========================================================================
# 🏋️ PRACTICE EXERCISES
# ===========================================================================
"""
1. Write a function that takes *args of numbers and returns their average.

2. Write a function that accepts **kwargs and returns a formatted string 
   like "name=Akram, age=25, city=Hyderabad".

3. Write a function `compose` that takes two functions and returns their 
   composition: compose(f, g)(x) = f(g(x))

4. Write a recursive function to calculate factorial.

5. Write a function `retry` that takes a function and a number of retries,
   and returns a new function that retries the original on failure.

6. Add proper type hints and docstrings to any 3 functions above.

7. Write a function that returns a closure counter (increment, decrement, get_value).

8. Explain the LEGB scope rule with your own example.
"""

print("\n✅ Module 07 Complete!")
