"""
===============================================================================
 MODULE 11: EXCEPTIONS & ERROR HANDLING
===============================================================================
 Python's try/except — similar to JS try/catch but with more features
 
 Run this file:  python 11_exceptions.py
===============================================================================
"""

# ===========================================================================
# 1. BASIC TRY/EXCEPT
# ===========================================================================

# JS: try { ... } catch (error) { ... } finally { ... }
# Py: try: ... except Exception as e: ... finally: ...

try:
    result = 10 / 0
except ZeroDivisionError:
    print("❌ Cannot divide by zero!")

# Catch the exception object
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"❌ Error: {e}")            # division by zero
    print(f"   Type: {type(e).__name__}")  # ZeroDivisionError


# ===========================================================================
# 2. MULTIPLE EXCEPT BLOCKS
# ===========================================================================

print(f"\n--- Multiple Except ---")

def risky_operation(value):
    try:
        number = int(value)
        result = 100 / number
        my_list = [1, 2, 3]
        return my_list[result]
    except ValueError:
        print(f"  ❌ '{value}' is not a valid number")
    except ZeroDivisionError:
        print(f"  ❌ Cannot divide by zero")
    except IndexError:
        print(f"  ❌ Index out of range")
    except Exception as e:
        # Catch-all — catches everything else
        print(f"  ❌ Unexpected error: {type(e).__name__}: {e}")

risky_operation("abc")    # ValueError
risky_operation("0")      # ZeroDivisionError
risky_operation("5")      # IndexError

# Catch multiple exception types in one block
try:
    result = int("abc")
except (ValueError, TypeError) as e:
    print(f"\nCaught: {e}")


# ===========================================================================
# 3. ELSE & FINALLY
# ===========================================================================

print(f"\n--- Else & Finally ---")

# else: runs ONLY if no exception occurred
# finally: ALWAYS runs (cleanup code)

def divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("  ❌ Division by zero!")
        return None
    else:
        # This runs ONLY if try succeeded (no JS equivalent!)
        print(f"  ✅ Division successful: {result}")
        return result
    finally:
        # This ALWAYS runs (same as JS finally)
        print("  🔄 Cleanup complete")

divide(10, 3)
print()
divide(10, 0)


# ===========================================================================
# 4. RAISING EXCEPTIONS
# ===========================================================================

print(f"\n--- Raising Exceptions ---")

# JS: throw new Error("message")
# Py: raise Exception("message")

def set_age(age):
    if not isinstance(age, int):
        raise TypeError(f"Age must be int, got {type(age).__name__}")
    if age < 0:
        raise ValueError(f"Age must be positive, got {age}")
    if age > 150:
        raise ValueError(f"Age unrealistic: {age}")
    return age

try:
    set_age(-5)
except ValueError as e:
    print(f"❌ {e}")

try:
    set_age("twenty")
except TypeError as e:
    print(f"❌ {e}")

# Re-raising an exception
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Logging the error...")
    raise  # Re-raise the same exception (like JS: throw without argument)


# ===========================================================================
# 5. CUSTOM EXCEPTIONS
# ===========================================================================

print(f"\n--- Custom Exceptions ---")

class AppError(Exception):
    """Base exception for our application."""
    pass

class ValidationError(AppError):
    """Raised when input validation fails."""
    def __init__(self, field, message):
        self.field = field
        self.message = message
        super().__init__(f"Validation error on '{field}': {message}")

class NotFoundError(AppError):
    """Raised when a resource is not found."""
    def __init__(self, resource, identifier):
        self.resource = resource
        self.identifier = identifier
        super().__init__(f"{resource} with id '{identifier}' not found")

class AuthenticationError(AppError):
    """Raised when authentication fails."""
    pass

# Using custom exceptions
def create_user(name, age):
    if not name or len(name) < 2:
        raise ValidationError("name", "Must be at least 2 characters")
    if not isinstance(age, int) or age < 0:
        raise ValidationError("age", "Must be a positive integer")
    return {"name": name, "age": age}

def find_user(user_id):
    users = {1: "Akram", 2: "Sara"}
    if user_id not in users:
        raise NotFoundError("User", user_id)
    return users[user_id]

# Handle custom exceptions
try:
    create_user("A", 25)
except ValidationError as e:
    print(f"❌ {e}")
    print(f"   Field: {e.field}")

try:
    find_user(99)
except NotFoundError as e:
    print(f"❌ {e}")
    print(f"   Resource: {e.resource}, ID: {e.identifier}")


# ===========================================================================
# 6. EXCEPTION HIERARCHY
# ===========================================================================

"""
BaseException
├── SystemExit
├── KeyboardInterrupt
├── GeneratorExit
└── Exception            ← Catch this or its subclasses
    ├── StopIteration
    ├── ArithmeticError
    │   ├── ZeroDivisionError
    │   └── OverflowError
    ├── LookupError
    │   ├── IndexError
    │   └── KeyError
    ├── OSError
    │   ├── FileNotFoundError
    │   ├── PermissionError
    │   └── ConnectionError
    ├── TypeError
    ├── ValueError
    ├── AttributeError
    ├── ImportError
    │   └── ModuleNotFoundError
    └── RuntimeError
        └── RecursionError
"""


# ===========================================================================
# 7. EXCEPTION CHAINING
# ===========================================================================

print(f"\n--- Exception Chaining ---")

def process_config(filename):
    try:
        with open(filename) as f:
            data = f.read()
    except FileNotFoundError as e:
        # 'from e' preserves the original exception chain
        raise RuntimeError(f"Failed to load config") from e

try:
    process_config("nonexistent.yaml")
except RuntimeError as e:
    print(f"❌ {e}")
    print(f"   Caused by: {e.__cause__}")


# ===========================================================================
# 8. CONTEXT MANAGERS (try/finally Alternative)
# ===========================================================================

print(f"\n--- Context Managers ---")

# Instead of try/finally for cleanup, use 'with' statement
# This is like try-with-resources in Java

# File handling with 'with'
try:
    with open("test_file.txt", "w") as f:
        f.write("Hello, World!")
    # File automatically closed when exiting 'with' block
    
    with open("test_file.txt", "r") as f:
        content = f.read()
        print(f"File content: {content}")
except Exception as e:
    print(f"File error: {e}")

# Custom context manager
class Timer:
    """Context manager to time code blocks."""
    
    def __enter__(self):
        import time
        self.start = time.perf_counter()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        import time
        self.elapsed = time.perf_counter() - self.start
        print(f"  ⏱️ Took {self.elapsed:.4f}s")
        return False  # Don't suppress exceptions

with Timer():
    total = sum(range(1000000))
    print(f"  Sum: {total}")

# Using contextlib
from contextlib import contextmanager

@contextmanager
def managed_resource(name):
    print(f"  📂 Opening {name}")
    try:
        yield name  # Code inside 'with' block runs here
    finally:
        print(f"  📂 Closing {name}")

with managed_resource("database") as resource:
    print(f"  Using {resource}")


# ===========================================================================
# 9. BEST PRACTICES
# ===========================================================================

"""
✅ DO:
  - Catch specific exceptions, not bare 'except:'
  - Use 'else' for code that should only run if try succeeded
  - Use 'finally' for cleanup (or better: context managers)
  - Create custom exceptions for your application
  - Include helpful error messages
  - Log exceptions before re-raising

❌ DON'T:
  - Use bare except: (catches EVERYTHING including KeyboardInterrupt)
  - Catch Exception silently (swallowing errors)
  - Use exceptions for flow control (use if/else instead)
  - Catch too broadly when you can be specific
"""

# ❌ BAD: Bare except
# try:
#     do_something()
# except:  # Catches EVERYTHING — even Ctrl+C!
#     pass

# ❌ BAD: Silently swallowing
# try:
#     do_something()
# except Exception:
#     pass  # Error is lost!

# ✅ GOOD: Specific, logged, with context
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def good_error_handling(data):
    try:
        result = process_data_safe(data)
    except ValueError as e:
        logger.error(f"Invalid data: {e}")
        raise
    except ConnectionError as e:
        logger.warning(f"Connection failed, retrying: {e}")
        # retry logic
    else:
        logger.info(f"Successfully processed: {result}")
        return result

def process_data_safe(data):
    if not data:
        raise ValueError("Data cannot be empty")
    return data.upper()


# ===========================================================================
# 10. EAFP vs LBYL
# ===========================================================================

print(f"\n--- EAFP vs LBYL ---")

"""
LBYL = "Look Before You Leap" (JS style — check before acting)
EAFP = "Easier to Ask Forgiveness than Permission" (Python style — try and handle)
"""

user_data = {"name": "Akram", "age": 25}

# LBYL (JS style) — Check first, then act
if "email" in user_data:
    email = user_data["email"]
else:
    email = "N/A"
print(f"LBYL: {email}")

# EAFP (Pythonic style) — Try it, handle error
try:
    email = user_data["email"]
except KeyError:
    email = "N/A"
print(f"EAFP: {email}")

# Even better — use .get()
email = user_data.get("email", "N/A")
print(f"Best: {email}")


# ===========================================================================
# 🏋️ PRACTICE EXERCISES
# ===========================================================================
"""
1. Write a function safe_divide(a, b) that handles ZeroDivisionError 
   and TypeError gracefully.

2. Create a custom exception hierarchy for an e-commerce app:
   - AppError (base)
   - PaymentError (with amount and reason)
   - InventoryError (with product and requested quantity)
   - AuthError (with username)

3. Write a context manager `suppress_errors(*exceptions)` that silently 
   catches specified exceptions.

4. Write a function that reads a JSON file safely, handling 
   FileNotFoundError and json.JSONDecodeError.

5. ⭐ INTERVIEW: Explain EAFP vs LBYL. Which does Python prefer and why?

6. ⭐ INTERVIEW: What's the difference between 'except Exception' and 
   bare 'except:'?

7. ⭐ INTERVIEW: When would you use 'raise ... from ...' (exception chaining)?
"""

# Cleanup
import os
if os.path.exists("test_file.txt"):
    os.remove("test_file.txt")

print("\n✅ Module 11 Complete!")
