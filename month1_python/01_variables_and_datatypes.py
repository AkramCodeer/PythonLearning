"""
===============================================================================
 MODULE 01: VARIABLES & DATA TYPES
===============================================================================
 Python vs JavaScript — A side-by-side guide for JS developers
 
 Run this file:  python 01_variables_and_datatypes.py
===============================================================================
"""

# ===========================================================================
# 1. VARIABLES — No let, const, or var needed!
# ===========================================================================

# JS:  let name = "Akram";     const age = 25;
# Py:  Just assign directly. No keyword needed.

name = "Akram"
age = 25
is_developer = True  # Note: True/False are capitalized (not true/false like JS)

print(f"Name: {name}, Age: {age}, Developer: {is_developer}")

# Python has NO const keyword. By convention, use UPPER_CASE for constants:
MAX_RETRIES = 3
API_BASE_URL = "https://api.example.com"

# Multiple assignment (not possible in JS this cleanly)
x, y, z = 1, 2, 3
print(f"x={x}, y={y}, z={z}")

# Swap values — super clean in Python!
# JS: [a, b] = [b, a]
# Py:
a, b = 10, 20
a, b = b, a
print(f"After swap: a={a}, b={b}")  # a=20, b=10


# ===========================================================================
# 2. DATA TYPES
# ===========================================================================

# --- Numeric Types ---
integer_num = 42              # int (no separate int/float in JS, all are "number")
float_num = 3.14              # float
complex_num = 2 + 3j          # complex (Python has this built-in!)
big_number = 1_000_000        # Underscores for readability (like JS: 1_000_000)

print(f"\nint: {integer_num}, type: {type(integer_num)}")
print(f"float: {float_num}, type: {type(float_num)}")
print(f"complex: {complex_num}, type: {type(complex_num)}")

# Python integers have UNLIMITED precision (no Number.MAX_SAFE_INTEGER limit!)
huge = 10 ** 100  # 10 to the power of 100
print(f"Huge number: {huge}" , type(huge))

# --- String Type ---
single = 'Hello'
double = "World"
multiline = """This is a
multiline string
in Python"""  # JS equivalent: backtick template literals

# f-strings (like JS template literals)
# JS:  `Hello ${name}, you are ${age}`
# Py:
greeting = f"Hello {name}, you are {age} years old"
print(f"\n{greeting}")

# String methods (many are similar to JS)
text = "Hello, World!"
print(f"Upper: {text.upper()}")           # JS: text.toUpperCase()
print(f"Lower: {text.lower()}")           # JS: text.toLowerCase()
print(f"Replace: {text.replace('World', 'Python')}")  # Same as JS
print(f"Split: {text.split(', ')}")       # Same as JS but returns list, not array
print(f"Strip: {'  hello  '.strip()}")    # JS: '  hello  '.trim()
print(f"Starts with: {text.startswith('Hello')}")  # JS: text.startsWith('Hello')
print(f"Find: {text.find('World')}")      # JS: text.indexOf('World')
print(f"Length: {len(text)}")             # JS: text.length (len is a function!)

# --- Boolean Type ---
# JS: true, false    Py: True, False
is_active = True
is_admin = False

# Falsy values in Python (similar concept to JS):
# False, None, 0, 0.0, "", [], {}, set()
# JS falsy: false, null, undefined, 0, "", NaN

print(f"\nFalsy checks:")
print(f"bool(0) = {bool(0)}")          # False
print(f"bool('') = {bool('')}")        # False
print(f"bool([]) = {bool([])}")        # False
print(f"bool(None) = {bool(None)}")    # False (None ≈ null in JS)
print(f"bool(1) = {bool(1)}")          # True
print(f"bool('hi') = {bool('hi')}")    # True

# --- None Type ---
# JS: null, undefined    Py: None (only one, no undefined!)
result = None
print(f"\nresult is None: {result is None}")  # Use 'is' not '==' for None

# --- Type Checking ---
# JS: typeof variable    Py: type(variable) or isinstance()
print(f"\nType of 42: {type(42)}")            # <class 'int'>
print(f"Type of 'hi': {type('hi')}")          # <class 'str'>
print(f"isinstance check: {isinstance(42, int)}")  # True (preferred way)
print(f"isinstance multiple: {isinstance(42, (int, float))}")  # True


# ===========================================================================
# 3. TYPE CONVERSION (Casting)
# ===========================================================================

# JS: Number("42"), String(42), parseInt("42")
# Py: int("42"),    str(42),    int("42")

str_num = "42"
converted = int(str_num)       # String to int
print(f"\nConverted: {converted}, type: {type(converted)}")

num_to_str = str(42)           # Int to string
float_to_int = int(3.99)      # Truncates (not rounds!): 3
int_to_float = float(42)      # 42.0
str_to_list = list("hello")   # ['h', 'e', 'l', 'l', 'o']

print(f"float_to_int: {float_to_int}")
print(f"str_to_list: {str_to_list}")


# ===========================================================================
# 4. OPERATORS
# ===========================================================================

# Arithmetic (same as JS)
print(f"\n--- Arithmetic ---")
print(f"10 + 3 = {10 + 3}")
print(f"10 - 3 = {10 - 3}")
print(f"10 * 3 = {10 * 3}")
print(f"10 / 3 = {10 / 3}")       # Always returns float: 3.333...
print(f"10 // 3 = {10 // 3}")     # Floor division: 3 (Python special!)
print(f"10 % 3 = {10 % 3}")       # Modulo: 1
print(f"10 ** 3 = {10 ** 3}")     # Power: 1000  (JS: Math.pow(10, 3) or 10**3)

# Comparison
print(f"\n--- Comparison ---")
print(f"10 == 10: {10 == 10}")     # True (value comparison)
print(f"10 != 5: {10 != 5}")       # True
# NO === or !== in Python! == already does strict comparison (no type coercion)
# Python: 10 == "10" is False (unlike JS where 10 == "10" is true)
print(f"10 == '10': {10 == '10'}")  # False! Python doesn't coerce types

# Logical operators
# JS: && || !     Py: and, or, not
print(f"\n--- Logical ---")
print(f"True and False: {True and False}")   # False
print(f"True or False: {True or False}")     # True
print(f"not True: {not True}")               # False

# Identity operators (Python special)
# 'is' checks if two variables point to the SAME OBJECT (like JS ===  for objects)
a = [1, 2, 3]
b = [1, 2, 3]
c = a
print(f"\n--- Identity ---")
print(f"a == b: {a == b}")    # True (same value)
print(f"a is b: {a is b}")    # False (different objects in memory)
print(f"a is c: {a is c}")    # True (same object)

# Membership operators (Python special — no JS equivalent!)
print(f"\n--- Membership ---")
print(f"'h' in 'hello': {'h' in 'hello'}")           # True
print(f"3 in [1, 2, 3]: {3 in [1, 2, 3]}")           # True
print(f"'key' in {{'key': 1}}: {'key' in {'key': 1}}")  # True (checks keys)


# ===========================================================================
# 5. INPUT FROM USER
# ===========================================================================

# JS: prompt() in browser, readline in Node
# Py: input() — always returns a string!

# Uncomment to try:
# user_name = input("Enter your name: ")
# user_age = int(input("Enter your age: "))  # Must convert to int
# print(f"Hello {user_name}, you are {user_age} years old!")


# ===========================================================================
# 🏋️ PRACTICE EXERCISES
# ===========================================================================
"""
1. Create variables for your name, age, height (float), and is_student (bool).
   Print them all using an f-string.


2. Given x = "123.45", convert it to a float, then to an int. What value do you get?

3. What is the result of:
   - 17 // 5
   - 17 % 5
   - 2 ** 10

4. Check if the string "Python" contains the letter "y" using the 'in' operator.

5. Create two lists with the same values. Verify that == returns True but 'is' returns False.

6. What are the falsy values in Python? Write code to verify each one.

7. What's the difference between type() and isinstance()? When would you use each?
"""


name = "Akram khan"
age = 25
height = 5.11
is_student = True
print(f"Name: {name}, Age: {age}, Height: {height}, Is Student: {is_student}")


x = "123.45"
print(float(x))
print(int(x))

print(17//5)
print(17%5)
print(2**10)

word ="python"

print("y" in word)

list1 = [1,2,3]
list2 = [1,2,3]
print(list1 == list2)
print(list1 is list2)

print(bool(0))

print("\n✅ Module 01 Complete! Run the file to see all outputs.")
