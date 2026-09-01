"""
===============================================================================
 MODULE 04: DICTIONARIES & SETS
===============================================================================
 Dicts ≈ JS Objects/Maps, Sets ≈ JS Sets
 
 Run this file:  python 04_dictionaries_and_sets.py
===============================================================================
"""

# ===========================================================================
# 1. DICTIONARIES — Python's Key-Value Store
# ===========================================================================

# JS: const user = { name: "Akram", age: 25 }
# Py: Keys must be quoted (unlike JS objects)
user = {
    "name": "Akram",
    "age": 25,
    "is_developer": True,
    "skills": ["Python", "JavaScript", "React"]
}

print(f"User: {user}")
print(f"Type: {type(user)}")


# ===========================================================================
# 2. ACCESSING VALUES
# ===========================================================================

print(f"\n--- Accessing ---")

# Method 1: Bracket notation (like JS)
print(f"Name: {user['name']}")

# ⚠️ KeyError if key doesn't exist (unlike JS which returns undefined)
# print(user["email"])  # ❌ KeyError!

# Method 2: .get() — Safe access (returns None or default if missing)
print(f"Email: {user.get('email')}")              # None
print(f"Email: {user.get('email', 'N/A')}")       # N/A (with default)

# JS equivalent of .get() with default:
# const email = user.email ?? "N/A"  (nullish coalescing)


# ===========================================================================
# 3. MODIFYING DICTIONARIES
# ===========================================================================

print(f"\n--- Modifying ---")

# Add / Update
user["email"] = "akram@example.com"    # Add new key
user["age"] = 26                       # Update existing
print(f"After update: {user}")

# Update multiple keys at once
user.update({
    "city": "Hyderabad",
    "role": "GenAI Engineer"
})
print(f"After update(): {user}")

# Remove
removed_value = user.pop("role")       # Remove & return value
print(f"Popped: {removed_value}")

del user["city"]                       # Remove without return
print(f"After del: {user}")

# Remove last inserted item
last = user.popitem()
print(f"Last item: {last}")            # Returns (key, value) tuple

# Set default — add only if key doesn't exist
user.setdefault("country", "India")    # Adds "country": "India"
user.setdefault("name", "Unknown")     # "name" exists, so no change
print(f"After setdefault: {user}")


# ===========================================================================
# 4. DICTIONARY METHODS
# ===========================================================================

print(f"\n--- Methods ---")

person = {"name": "Akram", "age": 25, "city": "Hyderabad"}

# Get all keys, values, items
print(f"Keys: {list(person.keys())}")      # ['name', 'age', 'city']
print(f"Values: {list(person.values())}")  # ['Akram', 25, 'Hyderabad']
print(f"Items: {list(person.items())}")    # [('name', 'Akram'), ...]

# Check if key exists
# JS: "name" in user  or  user.hasOwnProperty("name")
# Py:
print(f"'name' in person: {'name' in person}")      # True
print(f"'email' in person: {'email' in person}")     # False

# Length
print(f"Length: {len(person)}")

# Copy
copy = person.copy()                   # Shallow copy

# Create from keys
keys = ["a", "b", "c"]
from_keys = dict.fromkeys(keys, 0)     # {"a": 0, "b": 0, "c": 0}
print(f"fromkeys: {from_keys}")


# ===========================================================================
# 5. ITERATING OVER DICTIONARIES
# ===========================================================================

print(f"\n--- Iterating ---")

student = {"name": "Akram", "grade": "A", "score": 95}

# JS: for (const key in obj) { ... }
# Py: Several ways

# Just keys
for key in student:
    print(f"  Key: {key}")

# Keys and values together (most common)
# JS: Object.entries(obj).forEach(([key, value]) => ...)
for key, value in student.items():
    print(f"  {key}: {value}")

# Just values
for value in student.values():
    print(f"  Value: {value}")


# ===========================================================================
# 6. DICTIONARY COMPREHENSIONS
# ===========================================================================

print(f"\n--- Dict Comprehensions ---")

# JS: Object.fromEntries([1,2,3].map(x => [x, x**2]))
# Py:
squares = {x: x**2 for x in range(1, 6)}
print(f"Squares: {squares}")  # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# With condition
even_squares = {x: x**2 for x in range(1, 11) if x % 2 == 0}
print(f"Even squares: {even_squares}")

# Transform dict values
prices = {"apple": 1.0, "banana": 0.5, "cherry": 2.0}
doubled_prices = {k: v * 2 for k, v in prices.items()}
print(f"Doubled prices: {doubled_prices}")

# Swap keys and values
swapped = {v: k for k, v in prices.items()}
print(f"Swapped: {swapped}")


# ===========================================================================
# 7. NESTED DICTIONARIES
# ===========================================================================

print(f"\n--- Nested Dicts ---")

# JS: const users = { user1: { name: "...", ... } }
users = {
    "user1": {
        "name": "Akram",
        "age": 25,
        "skills": ["Python", "React"]
    },
    "user2": {
        "name": "Sarah",
        "age": 28,
        "skills": ["Java", "Angular"]
    }
}

print(f"User1 name: {users['user1']['name']}")
print(f"User1 first skill: {users['user1']['skills'][0]}")

# Safe nested access (no optional chaining ?. like JS)
# Use .get() chains:
email = users.get("user1", {}).get("email", "N/A")
print(f"User1 email: {email}")  # N/A


# ===========================================================================
# 8. MERGE DICTIONARIES
# ===========================================================================

print(f"\n--- Merging ---")

defaults = {"color": "blue", "size": "medium", "font": "Arial"}
custom = {"color": "red", "weight": "bold"}

# Method 1: ** unpacking (Python 3.5+)  — like JS spread: {...defaults, ...custom}
merged = {**defaults, **custom}
print(f"Merged: {merged}")

# Method 2: | operator (Python 3.9+)
merged2 = defaults | custom
print(f"Merged (|): {merged2}")


# ===========================================================================
# 9. SETS — Unique Collections
# ===========================================================================

print(f"\n--- Sets ---")

# Sets contain UNIQUE values only (like JS Set)
# JS: new Set([1, 2, 3])
# Py:
numbers = {1, 2, 3, 4, 5}             # Curly braces (but no key:value!)
from_list = set([1, 2, 2, 3, 3, 3])   # {1, 2, 3} — duplicates removed!
empty_set = set()                       # NOT {} — that's an empty dict!

print(f"Set: {numbers}")
print(f"From list (deduped): {from_list}")

# Add & Remove
numbers.add(6)                         # JS: set.add(6)
numbers.discard(3)                     # Remove (no error if missing)
numbers.remove(4)                      # Remove (KeyError if missing!)
print(f"After add/remove: {numbers}")


# ===========================================================================
# 10. SET OPERATIONS (Python's superpower!)
# ===========================================================================

print(f"\n--- Set Operations ---")

set_a = {1, 2, 3, 4, 5}
set_b = {4, 5, 6, 7, 8}

# Union (all elements from both)
print(f"Union: {set_a | set_b}")           # {1, 2, 3, 4, 5, 6, 7, 8}
print(f"Union: {set_a.union(set_b)}")

# Intersection (common elements)
print(f"Intersection: {set_a & set_b}")    # {4, 5}
print(f"Intersection: {set_a.intersection(set_b)}")

# Difference (in A but not in B)
print(f"Difference: {set_a - set_b}")      # {1, 2, 3}
print(f"Difference: {set_a.difference(set_b)}")

# Symmetric Difference (in A or B but not both)
print(f"Sym Diff: {set_a ^ set_b}")        # {1, 2, 3, 6, 7, 8}

# Subset & Superset
small = {1, 2}
big = {1, 2, 3, 4, 5}
print(f"\n{small} subset of {big}: {small.issubset(big)}")      # True
print(f"{big} superset of {small}: {big.issuperset(small)}")    # True
print(f"Disjoint: {small.isdisjoint({6, 7})}")                  # True (no common)


# ===========================================================================
# 11. PRACTICAL EXAMPLES
# ===========================================================================

print(f"\n--- Practical Examples ---")

# Remove duplicates from a list (preserving order)
items = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
unique_ordered = list(dict.fromkeys(items))
print(f"Unique (ordered): {unique_ordered}")

# Count word frequency
sentence = "the quick brown fox jumps over the lazy fox"
word_count = {}
for word in sentence.split():
    word_count[word] = word_count.get(word, 0) + 1
print(f"Word count: {word_count}")

# Using collections.Counter (even easier!)
from collections import Counter
word_count2 = Counter(sentence.split())
print(f"Counter: {word_count2}")
print(f"Most common 2: {word_count2.most_common(2)}")

# Group items by property
students = [
    {"name": "Ali", "grade": "A"},
    {"name": "Sara", "grade": "B"},
    {"name": "Ahmed", "grade": "A"},
    {"name": "Fatima", "grade": "B"},
    {"name": "Omar", "grade": "A"},
]
by_grade = {}
for s in students:
    by_grade.setdefault(s["grade"], []).append(s["name"])
print(f"By grade: {by_grade}")

# Find common skills between two users
user1_skills = {"Python", "React", "Node", "SQL"}
user2_skills = {"Python", "Angular", "Java", "SQL"}
common = user1_skills & user2_skills
unique_to_user1 = user1_skills - user2_skills
print(f"Common skills: {common}")
print(f"Unique to user1: {unique_to_user1}")


# ===========================================================================
# 🏋️ PRACTICE EXERCISES
# ===========================================================================
"""
1. Create a dict with 5 Indian cities and their populations. Find the city 
   with the highest population using max().

2. Given two dicts representing users, merge them with custom dict taking 
   priority over defaults.

3. Count character frequency in "hello world" using a dictionary.

4. Given a list [1,1,2,2,3,3,4,5,5], find elements that appear more than once.

5. Given two lists, find elements common to both using sets.

6. Create a nested dict representing a student with name, grades (as a dict 
   with subjects), and hobbies (as a list). Access the math grade.

7. Invert a dictionary: {"a": 1, "b": 2, "c": 3} → {1: "a", 2: "b", 3: "c"}

8. Use set operations to find:
   - Letters in "hello" but not in "world"
   - Letters in both "hello" and "world"  
   - All unique letters in both words combined
"""

print("\n✅ Module 04 Complete!")
