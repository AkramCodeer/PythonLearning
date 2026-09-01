"""
===============================================================================
 MODULE 02: STRINGS & FORMATTING
===============================================================================
 Everything about Python strings — your JS template literal skills transfer here!
 
 Run this file:  python 02_strings_and_formatting.py
===============================================================================
"""

# ===========================================================================
# 1. STRING CREATION
# ===========================================================================

# Single quotes (same as JS)
single = 'Hello World'

# Double quotes (same as JS)
double = "Hello World"

# Triple quotes for multiline (JS: backtick ` template literals)
multiline = """This is line 1
This is line 2
This is line 3"""

# Raw strings — backslashes are NOT escape characters
# Useful for regex patterns and file paths
raw = r"C:\Users\akram\Desktop"  # No escaping needed!
print(f"Raw string: {raw}")

# Strings are IMMUTABLE in Python (just like JS!)
name = "Akram"
# name[0] = "a"  # ❌ TypeError! Can't modify in place


# ===========================================================================
# 2. STRING FORMATTING (3 Ways)
# ===========================================================================

first_name = "Akram"
age = 25
salary = 75000.5678

# --- Method 1: f-strings (PREFERRED — like JS template literals) ---
# JS: `Hello ${name}, age ${age}`

# Py:
print(f"Hello {first_name}, age {age}")
print(f"Salary: ${salary:.2f}")      # Format to 2 decimal places: $75000.57
print(f"{'centered':^20}")            # Center in 20 chars
print(f"{'left':<20}|")              # Left align
print(f"{'right':>20}")              # Right align
print(f"Binary of 10: {10:b}")       # 1010
print(f"Hex of 255: {255:x}")        # ff
print(f"Big number: {1000000:,}")    # 1,000,000

# Expressions inside f-strings
print(f"2 + 3 = {2 + 3}")
print(f"Name uppercased: {first_name.upper()}")
print(f"Is adult: {'Yes' if age >= 18 else 'No'}")  # Ternary in f-string!

# --- Method 2: .format() (older but still used) ---
print("Hello {}, age {}".format(first_name, age))
print("Hello {name}, age {age}".format(name=first_name, age=age))
print("Salary: {:.2f}".format(salary))

# --- Method 3: % formatting (oldest — like C's printf) ---
print("Hello %s, age %d" % (first_name, age))
print("Salary: %.2f" % salary)


# ===========================================================================
# 3. STRING METHODS (with JS equivalents)
# ===========================================================================

text = "  Hello, World! Welcome to Python  "

# --- Case Methods ---
print(f"\n--- Case Methods ---")
print(f"upper(): {'hello'.upper()}")          # HELLO  (JS: toUpperCase())
print(f"lower(): {'HELLO'.lower()}")          # hello  (JS: toLowerCase())
print(f"capitalize(): {'hello world'.capitalize()}")  # Hello world
print(f"title(): {'hello world'.title()}")    # Hello World
print(f"swapcase(): {'Hello'.swapcase()}")    # hELLO

# --- Search Methods ---
print(f"\n--- Search Methods ---")
print(f"find('World'): {text.find('World')}")        # 9 (JS: indexOf())
print(f"rfind('o'): {text.rfind('o')}")               # Returns last occurrence
print(f"index('World'): {text.index('World')}")      # 9 (like find but raises error if not found)
print(f"count('l'): {text.count('l')}")               # 3  (no direct JS equivalent)
print(f"startswith('  He'): {text.startswith('  He')}")  # True  (JS: startsWith())
print(f"endswith('on  '): {text.endswith('on  ')}")     # True  (JS: endsWith())

# --- Trim/Strip Methods ---
print(f"\n--- Strip Methods ---")
print(f"strip(): '{text.strip()}'")           # Removes both sides (JS: trim())
print(f"lstrip(): '{text.lstrip()}'")         # Left only (JS: trimStart())
print(f"rstrip(): '{text.rstrip()}'")         # Right only (JS: trimEnd())

# --- Replace & Transform ---
print(f"\n--- Replace & Transform ---")
print(f"replace(): {'Hello World'.replace('World', 'Python')}")  # Same as JS
print(f"center(20, '-'): {'Hello'.center(20, '-')}")    # -------Hello--------
print(f"ljust(20, '.'): {'Hello'.ljust(20, '.')}")      # Hello...............
print(f"rjust(20, '.'): {'Hello'.rjust(20, '.')}")      # ...............Hello
print(f"zfill(10): {'42'.zfill(10)}")                    # 0000000042

# --- Split & Join ---
print(f"\n--- Split & Join ---")
csv_line = "apple,banana,cherry"
words = csv_line.split(",")                    # JS: split(",")
print(f"split(','): {words}")                  # ['apple', 'banana', 'cherry']

sentence = "Hello   World   Python"
print(f"split() (default): {sentence.split()}")  # Splits on any whitespace!

# Join — Note: it's a STRING method in Python, not a list method!
# JS: ["a", "b", "c"].join(", ")
# Py: ", ".join(["a", "b", "c"])
joined = ", ".join(words)
print(f"join: {joined}")                       # apple, banana, cherry

# Splitlines
multiline_text = "Line 1\nLine 2\nLine 3"
print(f"splitlines(): {multiline_text.splitlines()}")  # ['Line 1', 'Line 2', 'Line 3']

# --- Check Methods (return bool) ---
print(f"\n--- Check Methods ---")
print(f"'hello'.isalpha(): {'hello'.isalpha()}")      # True (only letters)
print(f"'12345'.isdigit(): {'12345'.isdigit()}")      # True (only digits)
print(f"'hello123'.isalnum(): {'hello123'.isalnum()}")  # True (letters or digits)
print(f"'   '.isspace(): {'   '.isspace()}")          # True (only whitespace)
print(f"'Hello'.istitle(): {'Hello'.istitle()}")      # True (title case)
print(f"'HELLO'.isupper(): {'HELLO'.isupper()}")      # True
print(f"'hello'.islower(): {'hello'.islower()}")      # True


# ===========================================================================
# 4. STRING SLICING (Python's superpower!)
# ===========================================================================

# JS has .slice() method, Python uses bracket notation [start:stop:step]
# This is MORE powerful than JS

text = "Hello, Python!"
#       0123456789...

print(f"\n--- String Slicing ---")
print(f"text[0]: {text[0]}")          # H (first character)
print(f"text[-1]: {text[-1]}")        # ! (last character — no JS equivalent!)
print(f"text[0:5]: {text[0:5]}")      # Hello (start:stop, stop not included)
print(f"text[:5]: {text[:5]}")        # Hello (start defaults to 0)
print(f"text[7:]: {text[7:]}")        # Python! (goes to end)
print(f"text[-7:]: {text[-7:]}")      # Python! (negative index from end)
print(f"text[::2]: {text[::2]}")      # Hlo yhn (every 2nd character)
print(f"text[::-1]: {text[::-1]}")    # !nohtyP ,olleH (REVERSED!)

# Reverse a string — one-liner!
original = "Hello"
reversed_str = original[::-1]
print(f"Reversed: {reversed_str}")    # olleH


# ===========================================================================
# 5. STRING ESCAPE CHARACTERS
# ===========================================================================

print(f"\n--- Escape Characters ---")
print("Tab:\tHello")              # Tab
print("Newline:\nHello")          # New line
print("Backslash: \\")            # Backslash
print("Quote: \"Hello\"")        # Double quote
print("Quote: \'Hello\'")        # Single quote

# Or use raw strings to avoid escaping
print(r"Raw: C:\new\test")        # Prints literally: C:\new\test


# ===========================================================================
# 6. STRING MULTIPLICATION & CONCATENATION
# ===========================================================================

print(f"\n--- String Operations ---")
print("Ha" * 3)                   # HaHaHa (string repetition!)
print("Hello" + " " + "World")   # Concatenation (same as JS)

# Python doesn't auto-concatenate strings with numbers like JS does:
# JS: "Age: " + 25  → "Age: 25"
# Py: "Age: " + 25  → ❌ TypeError!
# Py: "Age: " + str(25) → ✅ "Age: 25"
# Py: f"Age: {25}" → ✅ "Age: 25" (better way)


# ===========================================================================
# 7. USEFUL STRING RECIPES
# ===========================================================================

print(f"\n--- Useful Recipes ---")

# Check if string is a palindrome
word = "racecar"
is_palindrome = word == word[::-1]
print(f"'{word}' is palindrome: {is_palindrome}")

# Count vowels 
sentence = "Hello World"
vowel_count = sum(1 for char in sentence.lower() if char in 'aeiou')
print(f"Vowels in '{sentence}': {vowel_count}")

# Remove all spaces
no_spaces = "H e l l o".replace(" ", "")
print(f"No spaces: {no_spaces}")

# Check if all characters are unique
test_str = "abcdef"
all_unique = len(set(test_str)) == len(test_str)
print(f"All unique in '{test_str}': {all_unique}")

# Title case with exceptions
title = "the quick brown fox"
print(f"Title: {title.title()}")  # The Quick Brown Fox


# ===========================================================================
# 🏋️ PRACTICE EXERCISES
# ===========================================================================
"""
1. Given name = "akram", create a greeting "Hello, AKRAM! Welcome." using f-string and upper().

2. Given text = "  Python is awesome!  ", strip whitespace and count how many
   times the letter 'o' appears.

3. Given csv = "name,age,city,country", split it and join with " | ".

4. Reverse the string "JavaScript" using slicing.

5. Given s = "hello world hello python hello", replace only the FIRST "hello" 
   with "Hi" (hint: replace takes a 3rd argument for count).

6. Check if "A man a plan a canal Panama" is a palindrome 
   (ignore spaces and case).

7. Format this: price = 1234567.891 → "$1,234,567.89" using f-string formatting.

8. Given path = r"C:\\Users\\akram\\file.txt", extract just the filename "file.txt"
   using split() or rfind().
"""

print("\n✅ Module 02 Complete!")
