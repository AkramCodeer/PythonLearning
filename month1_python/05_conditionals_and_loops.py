"""
===============================================================================
 MODULE 05: CONDITIONALS & LOOPS
===============================================================================
 Control flow in Python — cleaner syntax than JS, more powerful features
 
 Run this file:  python 05_conditionals_and_loops.py
===============================================================================
"""

# ===========================================================================
# 1. IF / ELIF / ELSE
# ===========================================================================

# JS:  if (age >= 18) { ... } else if (age >= 13) { ... } else { ... }
# Py:  No parentheses, no curly braces — uses INDENTATION!

age = 20

if age >= 18:
    print("Adult")
elif age >= 13:
    print("Teenager")
else:
    print("Child")

# ⚠️ Key Differences from JS:
# 1. elif (not "else if")
# 2. Colon : after each condition
# 3. Indentation matters (usually 4 spaces)
# 4. No parentheses needed (but allowed)


# ===========================================================================
# 2. TERNARY OPERATOR
# ===========================================================================

# JS:  const status = age >= 18 ? "Adult" : "Minor"
# Py:  Value if Condition else Other_Value (reads like English!)

status = "Adult" if age >= 18 else "Minor"
print(f"Status: {status}")

# Nested ternary (don't overuse!)
category = "Senior" if age >= 60 else "Adult" if age >= 18 else "Minor"
print(f"Category: {category}")


# ===========================================================================
# 3. MATCH / CASE (Python 3.10+ — like JS switch)
# ===========================================================================

# JS: switch(day) { case "Mon": ...; break; ... }
# Py: match/case — MORE powerful than switch!

command = "start"

match command:
    case "start":
        print("\nStarting...")
    case "stop":
        print("Stopping...")
    case "pause" | "freeze":       # Multiple values (like multiple cases)
        print("Pausing...")
    case _:                        # Default case (underscore = wildcard)
        print("Unknown command")

# Pattern matching (Python's match is way more powerful than JS switch!)
point = (3, 0)

match point:
    case (0, 0):
        print("Origin")
    case (x, 0):
        print(f"On x-axis at {x}")
    case (0, y):
        print(f"On y-axis at {y}")
    case (x, y):
        print(f"Point at ({x}, {y})")


# ===========================================================================
# 4. TRUTHY & FALSY VALUES
# ===========================================================================

print(f"\n--- Truthy/Falsy ---")

# Falsy in Python: False, None, 0, 0.0, "", [], {}, set(), ()
# Everything else is Truthy

# Common pattern: Check if list/dict/string is empty
items = []
if not items:                          # JS: if (!items.length)
    print("List is empty")

name = ""
if not name:                           # JS: if (!name)
    print("Name is empty")

# Truthy check
data = [1, 2, 3]
if data:                               # JS: if (data.length)
    print(f"Data has {len(data)} items")


# ===========================================================================
# 5. LOGICAL OPERATORS
# ===========================================================================

print(f"\n--- Logical Operators ---")

# JS: && || !
# Py: and, or, not

x = 10

# and (JS: &&)
if x > 5 and x < 15:
    print(f"{x} is between 5 and 15")

# Pythonic way — chained comparison!
if 5 < x < 15:                        # This doesn't exist in JS!
    print(f"{x} is between 5 and 15 (chained)")

# or (JS: ||)
name = "" or "Default"                 # Short-circuit like JS
print(f"Name: {name}")

# not (JS: !)
is_active = True
if not is_active:
    print("Inactive")

# Walrus operator := (Python 3.8+) — assign AND use in one line
# Like: if ((n = getNumber()) > 10) in some languages
import random
if (n := random.randint(1, 20)) > 10:
    print(f"Got {n}, which is > 10")
else:
    print(f"Got {n}, which is <= 10")


# ===========================================================================
# 6. FOR LOOPS
# ===========================================================================

print(f"\n--- For Loops ---")

# JS: for (let i = 0; i < 5; i++)
# Py: Python's for is always a "for...of" loop (iterates over items)

# Basic for loop
for i in range(5):                     # 0, 1, 2, 3, 4
    print(f"  i = {i}")

# range() variations
# range(stop)           → 0 to stop-1
# range(start, stop)    → start to stop-1
# range(start, stop, step) → with step

print("\nrange(2, 10, 2):")
for i in range(2, 10, 2):             # 2, 4, 6, 8
    print(f"  {i}")

# Counting down
print("\nCountdown:")
for i in range(5, 0, -1):             # 5, 4, 3, 2, 1
    print(f"  {i}")

# Iterate over list
# JS: for (const fruit of fruits) { ... }
# Py:
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(f"  Fruit: {fruit}")

# With index — enumerate()
# JS: fruits.forEach((fruit, index) => ...)
for index, fruit in enumerate(fruits):
    print(f"  {index}: {fruit}")

# Start enumerate from custom number
for index, fruit in enumerate(fruits, start=1):
    print(f"  {index}. {fruit}")

# Iterate over dictionary
person = {"name": "Akram", "age": 25, "city": "Hyderabad"}

# Keys only
for key in person:
    print(f"  Key: {key}")

# Keys and values
for key, value in person.items():
    print(f"  {key} = {value}")

# Iterate over string
for char in "Hello":
    print(f"  Char: {char}")

# zip — iterate over multiple sequences
names = ["Alice", "Bob", "Charlie"]
scores = [95, 87, 92]
for name, score in zip(names, scores):
    print(f"  {name}: {score}")


# ===========================================================================
# 7. WHILE LOOPS
# ===========================================================================

print(f"\n--- While Loops ---")

# Same concept as JS
count = 0
while count < 5:
    print(f"  Count: {count}")
    count += 1                         # No ++ operator in Python!

# While with else (Python special — no JS equivalent!)
n = 5
while n > 0:
    n -= 1
else:
    print(f"  Loop finished normally, n = {n}")


# ===========================================================================
# 8. BREAK, CONTINUE, PASS
# ===========================================================================

print(f"\n--- Break, Continue, Pass ---")

# break — exit loop (same as JS)
for i in range(10):
    if i == 5:
        break
    print(f"  {i}", end=" ")
print()  # Newline

# continue — skip iteration (same as JS)
for i in range(10):
    if i % 2 == 0:
        continue
    print(f"  {i}", end=" ")
print()

# pass — do nothing placeholder (NO JS equivalent)
# Use when you need a block but have nothing to put in it
for i in range(5):
    if i == 3:
        pass  # TODO: handle this case later
    print(f"  {i}", end=" ")
print()

# for/else — else runs if loop completes WITHOUT break
print("\nFor/Else (searching for 7):")
numbers = [1, 3, 5, 9, 11]
for num in numbers:
    if num == 7:
        print("  Found 7!")
        break
else:
    print("  7 not found in list")  # This runs!


# ===========================================================================
# 9. NESTED LOOPS
# ===========================================================================

print(f"\n--- Nested Loops ---")

# Multiplication table
for i in range(1, 4):
    for j in range(1, 4):
        print(f"  {i} × {j} = {i*j}")
    print()

# Pattern printing
print("Triangle pattern:")
for i in range(1, 6):
    print("  " + "* " * i)


# ===========================================================================
# 10. LOOP TECHNIQUES
# ===========================================================================

print(f"\n--- Loop Techniques ---")

# Reversed iteration
for fruit in reversed(fruits):
    print(f"  {fruit}")

# Sorted iteration
numbers = [3, 1, 4, 1, 5, 9]
for n in sorted(numbers):
    print(f"  {n}", end=" ")
print()

# Unique sorted
for n in sorted(set(numbers)):
    print(f"  {n}", end=" ")
print()

# Using iter() and next() manually
it = iter([10, 20, 30])
print(f"\nnext(): {next(it)}")   # 10
print(f"next(): {next(it)}")     # 20
print(f"next(): {next(it)}")     # 30


# ===========================================================================
# 🏋️ PRACTICE EXERCISES
# ===========================================================================
"""
1. Write a program that prints "Fizz" for multiples of 3, "Buzz" for multiples
   of 5, "FizzBuzz" for both, and the number otherwise (1 to 30).

2. Given a list of numbers, find and print all prime numbers up to 50.

3. Use a while loop to find the first power of 2 that exceeds 1000.

4. Write a program that counts vowels and consonants in a string.

5. Use the for/else construct to check if a number is prime.

6. Print this pattern using nested loops:
   1
   1 2
   1 2 3
   1 2 3 4
   1 2 3 4 5

7. Use enumerate to create a numbered menu from a list of options.

8. Given two lists, use zip to create a dictionary mapping names to ages.

9. Use the walrus operator (:=) to read numbers until the user enters 0,
   and print their sum.

10. Write a program that finds common elements between three lists.
"""

print("\n✅ Module 05 Complete!")
