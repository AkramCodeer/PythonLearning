"""
===============================================================================
 MODULE 12: FILE HANDLING & MODULES
===============================================================================
 Reading/writing files + importing code — your Node.js fs skills transfer here
 
 Run this file:  python 12_files_and_modules.py
===============================================================================
"""

import os
import json


# ===========================================================================
# 1. READING FILES
# ===========================================================================

# Create a sample file first
sample_text = """Hello, Python!
This is line 2.
And this is line 3.
File handling is easy!
Last line."""

# Write a sample file to work with
with open("sample.txt", "w") as f:
    f.write(sample_text)

print("--- Reading Files ---")

# Method 1: read() — entire file as one string
# Node.js: fs.readFileSync("file.txt", "utf-8")
with open("sample.txt", "r") as f:
    content = f.read()
    print(f"Full content:\n{content}\n")

# Method 2: readline() — one line at a time
with open("sample.txt", "r") as f:
    first_line = f.readline().strip()
    second_line = f.readline().strip()
    print(f"First: {first_line}")
    print(f"Second: {second_line}")

# Method 3: readlines() — all lines as a list
with open("sample.txt", "r") as f:
    lines = f.readlines()
    print(f"\nAll lines: {[l.strip() for l in lines]}")

# Method 4: Iterate line by line (BEST for large files — memory efficient!)
print("\nLine by line:")
with open("sample.txt", "r") as f:
    for line_num, line in enumerate(f, 1):
        print(f"  {line_num}: {line.strip()}")


# ===========================================================================
# 2. WRITING FILES
# ===========================================================================

print(f"\n--- Writing Files ---")

# Mode 'w' — Write (creates new or OVERWRITES existing)
with open("output.txt", "w") as f:
    f.write("Line 1\n")
    f.write("Line 2\n")

# Mode 'a' — Append (adds to end)
with open("output.txt", "a") as f:
    f.write("Line 3 (appended)\n")

# writelines() — write a list of strings
with open("output.txt", "a") as f:
    f.writelines(["Line 4\n", "Line 5\n"])

# Read back to verify
with open("output.txt") as f:
    print(f"Output file:\n{f.read()}")

# Using print() to write to file
with open("output.txt", "a") as f:
    print("Line 6 (via print)", file=f)


# ===========================================================================
# 3. WORKING WITH JSON
# ===========================================================================

print(f"--- JSON Handling ---")

# JS: JSON.stringify() / JSON.parse()
# Py: json.dumps() / json.loads()

data = {
    "name": "Akram",
    "age": 25,
    "skills": ["Python", "React", "Node.js"],
    "address": {
        "city": "Hyderabad",
        "country": "India"
    }
}

# Write JSON to file
# Node.js: fs.writeFileSync("data.json", JSON.stringify(data, null, 2))
with open("data.json", "w") as f:
    json.dump(data, f, indent=2)
print("JSON written to data.json")

# Read JSON from file
# Node.js: JSON.parse(fs.readFileSync("data.json", "utf-8"))
with open("data.json", "r") as f:
    loaded = json.load(f)
print(f"Loaded: {loaded}")
print(f"Name: {loaded['name']}")

# JSON string operations (not file-based)
json_string = json.dumps(data, indent=2)  # Dict → JSON string
parsed = json.loads(json_string)           # JSON string → Dict
print(f"JSON string type: {type(json_string)}")
print(f"Parsed type: {type(parsed)}")


# ===========================================================================
# 4. WORKING WITH CSV
# ===========================================================================

print(f"\n--- CSV Handling ---")

import csv

# Write CSV
students = [
    ["Name", "Age", "Grade"],
    ["Akram", 25, "A"],
    ["Sara", 28, "A+"],
    ["Ali", 22, "B"],
]

with open("students.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(students)
print("CSV written")

# Read CSV
with open("students.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        print(f"  {row}")

# Read CSV as dictionaries (with headers!)
print("\nAs dictionaries:")
with open("students.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"  {dict(row)}")


# ===========================================================================
# 5. PATH HANDLING
# ===========================================================================

print(f"\n--- Path Handling ---")

from pathlib import Path  # Modern way (preferred over os.path!)

# Current working directory
cwd = Path.cwd()
print(f"CWD: {cwd}")

# Create paths
project = Path("my_project")
config_file = project / "config" / "settings.json"  # / operator for paths!
print(f"Config path: {config_file}")

# Path properties
p = Path("c:/Users/akram/Documents/file.txt")
print(f"Name: {p.name}")          # file.txt
print(f"Stem: {p.stem}")          # file
print(f"Suffix: {p.suffix}")      # .txt
print(f"Parent: {p.parent}")      # c:/Users/akram/Documents
print(f"Parts: {p.parts}")        # ('c:\\', 'Users', 'akram', ...)

# Check existence
print(f"\nsample.txt exists: {Path('sample.txt').exists()}")
print(f"Is file: {Path('sample.txt').is_file()}")
print(f"Is dir: {Path('.').is_dir()}")

# os module basics
print(f"\n--- os module ---")
print(f"Current dir: {os.getcwd()}")
print(f"Files here: {os.listdir('.')[:5]}...")

# List directory with pathlib
print(f"\nPython files:")
for p in Path(".").glob("*.py"):
    print(f"  {p.name}")


# ===========================================================================
# 6. DIRECTORY OPERATIONS
# ===========================================================================

print(f"\n--- Directory Operations ---")

# Create directories
os.makedirs("test_dir/sub_dir", exist_ok=True)  # Like mkdir -p

# Or with pathlib
Path("test_dir/another").mkdir(parents=True, exist_ok=True)

# List directory contents
for item in Path("test_dir").iterdir():
    kind = "DIR" if item.is_dir() else "FILE"
    print(f"  [{kind}] {item.name}")

# Find files recursively (like find command)
print(f"\nAll .py files recursively:")
for py_file in Path(".").rglob("*.py"):
    print(f"  {py_file}")


# ===========================================================================
# 7. MODULES & IMPORTS
# ===========================================================================

print(f"\n--- Modules & Imports ---")

"""
Python modules = JS modules, but different syntax:

JS:                              Python:
import { func } from './mod'  →  from module import func
import * as mod from './mod'  →  import module as mod  
export default func           →  (no equivalent — all top-level is exported)
export { func }               →  (no equivalent — use __all__ = ['func'])
"""

# Import entire module
import math
print(f"math.pi = {math.pi}")
print(f"math.sqrt(16) = {math.sqrt(16)}")

# Import specific items
from datetime import datetime, timedelta
now = datetime.now()
print(f"Now: {now}")
print(f"Tomorrow: {now + timedelta(days=1)}")

# Import with alias
import collections as col
counter = col.Counter("hello world")
print(f"Counter: {counter}")

# Import everything (NOT recommended — pollutes namespace)
# from math import *

# Check what's in a module
print(f"\nmath functions (first 10): {dir(math)[:10]}")


# ===========================================================================
# 8. CREATING YOUR OWN MODULES
# ===========================================================================

"""
Any .py file is a module! To create a package (folder of modules):

my_package/
├── __init__.py      ← Makes it a package (can be empty)
├── utils.py         ← Module
├── models.py        ← Module
└── services/        ← Sub-package
    ├── __init__.py
    └── api.py

Usage:
  from my_package.utils import helper_function
  from my_package.services.api import fetch_data
"""

# __name__ guard — runs code only when script is executed directly
# (not when imported as a module)
# This is like: if (require.main === module) in Node.js

if __name__ == "__main__":
    print(f"\n__name__ = {__name__}")  # __main__ (when run directly)
    print("This runs only when executed directly, not when imported")


# ===========================================================================
# 9. VIRTUAL ENVIRONMENTS & PIP
# ===========================================================================

"""
Virtual environments isolate your project dependencies
(like node_modules + package.json but different mechanism)

Commands:
  # Create virtual environment
  python -m venv venv
  
  # Activate (Windows PowerShell)
  .\\venv\\Scripts\\Activate.ps1
  
  # Activate (Mac/Linux)
  source venv/bin/activate
  
  # Install packages
  pip install requests fastapi
  
  # Save dependencies (like package.json)
  pip freeze > requirements.txt
  
  # Install from requirements (like npm install)
  pip install -r requirements.txt
  
  # Deactivate
  deactivate

Comparison with Node.js:
  npm init           →  python -m venv venv
  npm install pkg    →  pip install pkg
  package.json       →  requirements.txt
  npm install        →  pip install -r requirements.txt
  node_modules/      →  venv/
  npx                →  python -m (somewhat)
"""


# ===========================================================================
# 10. USEFUL STANDARD LIBRARY MODULES
# ===========================================================================

print(f"\n--- Standard Library Highlights ---")

# --- datetime ---
from datetime import datetime, date, timedelta
now = datetime.now()
print(f"Now: {now.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Week from now: {(now + timedelta(weeks=1)).strftime('%Y-%m-%d')}")

# --- random ---
import random
print(f"\nRandom int: {random.randint(1, 100)}")
print(f"Random choice: {random.choice(['apple', 'banana', 'cherry'])}")
print(f"Random sample: {random.sample(range(100), 5)}")

# --- re (regex) ---
import re
text = "Call me at 123-456-7890 or 098-765-4321"
phones = re.findall(r'\d{3}-\d{3}-\d{4}', text)
print(f"\nPhone numbers: {phones}")

# --- collections ---
from collections import Counter, defaultdict, OrderedDict, deque

# Counter
word_count = Counter("hello world hello python".split())
print(f"\nCounter: {word_count}")

# defaultdict
dd = defaultdict(list)
dd["fruits"].append("apple")
dd["fruits"].append("banana")
dd["vegs"].append("carrot")
print(f"defaultdict: {dict(dd)}")

# deque (double-ended queue)
dq = deque([1, 2, 3])
dq.appendleft(0)
dq.append(4)
print(f"deque: {dq}")

# --- itertools ---
import itertools
print(f"\nchain: {list(itertools.chain([1,2], [3,4]))}")

# --- functools ---
from functools import reduce, lru_cache
print(f"reduce sum: {reduce(lambda a, b: a + b, [1,2,3,4,5])}")


# ===========================================================================
# CLEANUP
# ===========================================================================

# Clean up created files
for f in ["sample.txt", "output.txt", "data.json", "students.csv"]:
    if os.path.exists(f):
        os.remove(f)

import shutil
if os.path.exists("test_dir"):
    shutil.rmtree("test_dir")

print("\n🧹 Cleaned up temporary files")


# ===========================================================================
# 🏋️ PRACTICE EXERCISES
# ===========================================================================
"""
1. Write a program that reads a text file, counts word frequency, and 
   writes the results to a JSON file.

2. Create a CSV of 10 students with name, math_score, science_score.
   Read it back and calculate averages.

3. Write a function that recursively finds all files with a given 
   extension in a directory tree.

4. Create a simple "config manager" that reads/writes settings from a 
   JSON file with get/set methods.

5. Write a module called `string_utils.py` with functions: reverse, 
   is_palindrome, count_vowels. Import and use it.

6. Set up a virtual environment, install `requests`, and make a simple
   API call to https://api.github.com/users/octocat

7. Write a context manager that logs the start and end time of a code block 
   to a file.
"""

print("\n✅ Module 12 Complete!")
