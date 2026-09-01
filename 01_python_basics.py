# LESSON 1: Python Basics
# Everything you need to know about Python before touching LangChain.
# Run this file: python 01_python_basics.py

# ─────────────────────────────────────────────
# 1. VARIABLES
# A variable is just a named box that holds a value.
# ─────────────────────────────────────────────

name = "Alice"          # text (called a "string")
age = 30                # whole number (called an "int")
temperature = 98.6      # decimal number (called a "float")
is_happy = True         # True or False (called a "bool")

print(name)             # prints: Alice
print(type(name))       # prints: <class 'str'>  ← tells you the type


# ─────────────────────────────────────────────
# 2. F-STRINGS — the easy way to build sentences
# Put an f before the quote, then use {} to insert variables.
# ─────────────────────────────────────────────

greeting = f"Hello, {name}! You are {age} years old."
print(greeting)         # Hello, Alice! You are 30 years old.


# ─────────────────────────────────────────────
# 3. LISTS — an ordered collection of things
# ─────────────────────────────────────────────

fruits = ["apple", "banana", "cherry"]
print(fruits[0])        # apple  ← indexing starts at 0
print(fruits[-1])       # cherry ← -1 means "last item"

fruits.append("date")   # add to the end
print(fruits)           # ['apple', 'banana', 'cherry', 'date']

# Loop through a list:
for fruit in fruits:
    print(f"I like {fruit}")


# ─────────────────────────────────────────────
# 4. DICTIONARIES — key → value pairs (like a real dictionary)
# This is how LangChain often passes data around.
# ─────────────────────────────────────────────

person = {
    "name": "Bob",
    "age": 25,
    "city": "New York"
}

print(person["name"])   # Bob
print(person["city"])   # New York

person["job"] = "developer"   # add a new key
print(person)


# ─────────────────────────────────────────────
# 5. FUNCTIONS — reusable blocks of code
# def = "define a function"
# ─────────────────────────────────────────────

def greet(name):
    """This function takes a name and returns a greeting."""
    return f"Hello, {name}!"

result = greet("Carol")
print(result)           # Hello, Carol!

# Functions can have default values:
def greet_with_title(name, title="Ms."):
    return f"Hello, {title} {name}!"

print(greet_with_title("Smith"))           # Hello, Ms. Smith!
print(greet_with_title("Jones", "Dr."))    # Hello, Dr. Jones!


# ─────────────────────────────────────────────
# 6. CLASSES — a blueprint for creating objects
# LangChain is built on classes. Understanding this is key.
# ─────────────────────────────────────────────

class Dog:
    # __init__ runs automatically when you create a new Dog
    def __init__(self, name, breed):
        self.name = name    # self means "this specific dog"
        self.breed = breed

    def speak(self):
        return f"{self.name} says: Woof!"

# Create instances (actual dogs) from the blueprint:
dog1 = Dog("Rex", "Labrador")
dog2 = Dog("Bella", "Poodle")

print(dog1.speak())     # Rex says: Woof!
print(dog2.name)        # Bella


# ─────────────────────────────────────────────
# 7. IMPORTS — using code someone else wrote
# LangChain is a library you import like this.
# ─────────────────────────────────────────────

import os                           # built-in Python module
from datetime import datetime       # import one specific thing

print(os.getcwd())                  # prints current folder
print(datetime.now())               # prints current date & time


# ─────────────────────────────────────────────
# 8. ENVIRONMENT VARIABLES — secrets and config
# You'll use this to load your API key safely.
# ─────────────────────────────────────────────

# python-dotenv lets you load a .env file into os.environ
# (install it with: pip install python-dotenv)
# from dotenv import load_dotenv
# load_dotenv()
# api_key = os.getenv("OPENAI_API_KEY")
# print(api_key)   # reads from your .env file

print("\n✓ Lesson 1 complete! You know enough Python to start LangChain.")
print("→ Next: run python 02_langchain_intro.py")
