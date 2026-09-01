"""
===============================================================================
 MODULE 08: DECORATORS
===============================================================================
 ⭐ HIGH INTERVIEW IMPORTANCE — Decorators are Python's way of wrapping functions
 
 Run this file:  python 08_decorators.py
===============================================================================
"""

# ===========================================================================
# 1. WHAT IS A DECORATOR?
# ===========================================================================
"""
A decorator is a function that takes another function, adds some behavior,
and returns a new function — WITHOUT modifying the original function.

Think of it like Express.js middleware that wraps route handlers!

JS Middleware:
  app.get('/api', authMiddleware, (req, res) => { ... })

Python Decorator:
  @auth_required
  def get_users():
      ...
"""


# ===========================================================================
# 2. BUILDING A DECORATOR FROM SCRATCH
# ===========================================================================

# Step 1: Functions are objects in Python (just like JS!)
def say_hello():
    return "Hello!"

# Functions can be assigned to variables
greet = say_hello
print(greet())  # Hello!

# Step 2: Functions can be passed as arguments
def execute(func):
    return func()

print(execute(say_hello))  # Hello!

# Step 3: Functions can return functions (closures)
def create_greeter(greeting):
    def greeter(name):
        return f"{greeting}, {name}!"
    return greeter

hello = create_greeter("Hello")
namaste = create_greeter("Namaste")
print(hello("Akram"))     # Hello, Akram!
print(namaste("Akram"))   # Namaste, Akram!


# ===========================================================================
# 3. YOUR FIRST DECORATOR
# ===========================================================================

print(f"\n--- First Decorator ---")

def my_decorator(func):
    """A simple decorator that adds logging."""
    def wrapper():
        print(f"  ⏳ Before calling {func.__name__}")
        result = func()
        print(f"  ✅ After calling {func.__name__}")
        return result
    return wrapper

# Without @ syntax
def say_hello():
    print("  Hello!")

decorated_hello = my_decorator(say_hello)
decorated_hello()

# With @ syntax (syntactic sugar — same thing!)
@my_decorator
def say_goodbye():
    print("  Goodbye!")

print()
say_goodbye()  # Automatically wrapped!

# @my_decorator is the same as:
# say_goodbye = my_decorator(say_goodbye)


# ===========================================================================
# 4. DECORATOR WITH ARGUMENTS (Using *args, **kwargs)
# ===========================================================================

print(f"\n--- Decorator with Arguments ---")

import functools

def log_function(func):
    """Log function calls with arguments and return value."""
    @functools.wraps(func)  # Preserves original function's metadata!
    def wrapper(*args, **kwargs):
        args_str = ", ".join(repr(a) for a in args)
        kwargs_str = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())
        all_args = ", ".join(filter(None, [args_str, kwargs_str]))
        
        print(f"  📞 Calling {func.__name__}({all_args})")
        result = func(*args, **kwargs)
        print(f"  📤 {func.__name__} returned {result!r}")
        return result
    return wrapper

@log_function
def add(a, b):
    """Add two numbers."""
    return a + b

@log_function
def greet(name, greeting="Hello"):
    """Greet someone."""
    return f"{greeting}, {name}!"

add(3, 5)
print()
greet("Akram", greeting="Namaste")


# ===========================================================================
# 5. WHY functools.wraps IS IMPORTANT
# ===========================================================================

print(f"\n--- functools.wraps ---")

# Without @wraps, the decorated function loses its identity:
def bad_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@bad_decorator
def my_function():
    """My docstring."""
    pass

print(f"Without @wraps:")
print(f"  Name: {my_function.__name__}")  # 'wrapper' — WRONG!
print(f"  Doc: {my_function.__doc__}")    # None — WRONG!

# With @wraps:
print(f"\nWith @wraps:")
print(f"  Name: {add.__name__}")          # 'add' — CORRECT!
print(f"  Doc: {add.__doc__}")            # 'Add two numbers.' — CORRECT!


# ===========================================================================
# 6. PRACTICAL DECORATOR EXAMPLES
# ===========================================================================

print(f"\n--- Practical Decorators ---")

# --- Timer Decorator ---
import time

def timer(func):
    """Measure function execution time."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"  ⏱️ {func.__name__} took {end - start:.4f}s")
        return result
    return wrapper

@timer
def slow_function():
    """Simulate a slow function."""
    time.sleep(0.1)
    return "Done!"

slow_function()

# --- Retry Decorator ---
def retry(max_attempts=3, delay=0.1):
    """Retry a function on failure."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"  ⚠️ Attempt {attempt}/{max_attempts} failed: {e}")
                    if attempt < max_attempts:
                        time.sleep(delay)
                    else:
                        raise
        return wrapper
    return decorator

import random

@retry(max_attempts=3)
def unreliable_api():
    """Simulates an unreliable API call."""
    if random.random() < 0.7:  # 70% chance of failure
        raise ConnectionError("API timeout")
    return {"status": "success"}

print()
try:
    result = unreliable_api()
    print(f"  Result: {result}")
except ConnectionError:
    print("  ❌ All attempts failed")

# --- Cache/Memoize Decorator ---
def memoize(func):
    """Cache function results."""
    cache = {}
    
    @functools.wraps(func)
    def wrapper(*args):
        if args in cache:
            print(f"  💾 Cache hit for {func.__name__}{args}")
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result
    return wrapper

@memoize
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(f"\nfib(10) = {fibonacci(10)}")
print(f"fib(10) again = {fibonacci(10)}")  # Cache hit!

# Note: Python has a built-in version: @functools.lru_cache
@functools.lru_cache(maxsize=128)
def fibonacci_builtin(n):
    if n <= 1:
        return n
    return fibonacci_builtin(n - 1) + fibonacci_builtin(n - 2)

print(f"fib_builtin(50) = {fibonacci_builtin(50)}")

# --- Validate Input Decorator ---
def validate_types(**type_hints):
    """Validate function argument types."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Check positional args
            import inspect
            sig = inspect.signature(func)
            params = list(sig.parameters.keys())
            
            for i, arg in enumerate(args):
                param_name = params[i]
                if param_name in type_hints:
                    expected = type_hints[param_name]
                    if not isinstance(arg, expected):
                        raise TypeError(
                            f"'{param_name}' must be {expected.__name__}, "
                            f"got {type(arg).__name__}"
                        )
            return func(*args, **kwargs)
        return wrapper
    return decorator

@validate_types(name=str, age=int)
def create_profile(name, age):
    return {"name": name, "age": age}

print(f"\n{create_profile('Akram', 25)}")
try:
    create_profile("Akram", "25")  # String instead of int!
except TypeError as e:
    print(f"❌ {e}")


# ===========================================================================
# 7. DECORATOR FACTORIES (Decorators with Arguments)
# ===========================================================================

print(f"\n--- Decorator Factories ---")

# When your decorator needs parameters, you add ANOTHER layer of nesting

def repeat(n=2):
    """Repeat a function call n times."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(n):
                results.append(func(*args, **kwargs))
            return results
        return wrapper
    return decorator

@repeat(n=3)
def say_hi(name):
    print(f"  Hi {name}!")
    return f"Hi {name}!"

results = say_hi("Akram")

# --- Role-based access (like Express middleware!) ---
def require_role(role):
    """Check if user has required role."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(user, *args, **kwargs):
            if user.get("role") != role:
                raise PermissionError(
                    f"Requires '{role}' role, user has '{user.get('role')}'"
                )
            return func(user, *args, **kwargs)
        return wrapper
    return decorator

@require_role("admin")
def delete_user(current_user, user_id):
    return f"User {user_id} deleted by {current_user['name']}"

admin = {"name": "Akram", "role": "admin"}
viewer = {"name": "Guest", "role": "viewer"}

print(f"\n{delete_user(admin, 42)}")
try:
    delete_user(viewer, 42)
except PermissionError as e:
    print(f"❌ {e}")


# ===========================================================================
# 8. STACKING DECORATORS
# ===========================================================================

print(f"\n--- Stacking Decorators ---")

# You can apply multiple decorators — they execute bottom-up!

@timer
@log_function
def process_data(data):
    """Process some data."""
    time.sleep(0.05)
    return [x * 2 for x in data]

# This is equivalent to:
# process_data = timer(log_function(process_data))

result = process_data([1, 2, 3])
print(f"Result: {result}")


# ===========================================================================
# 9. CLASS-BASED DECORATORS
# ===========================================================================

print(f"\n--- Class-Based Decorator ---")

class CountCalls:
    """Count how many times a function is called."""
    
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self.call_count = 0
    
    def __call__(self, *args, **kwargs):
        self.call_count += 1
        print(f"  Call #{self.call_count} to {self.func.__name__}")
        return self.func(*args, **kwargs)

@CountCalls
def say_something(msg):
    print(f"  {msg}")

say_something("First!")
say_something("Second!")
say_something("Third!")
print(f"Total calls: {say_something.call_count}")


# ===========================================================================
# 10. BUILT-IN DECORATORS
# ===========================================================================

print(f"\n--- Built-in Decorators ---")

# @property — covered in OOP module
# @staticmethod — covered in OOP module
# @classmethod — covered in OOP module
# @functools.lru_cache — memoization
# @functools.wraps — preserve function metadata
# @dataclasses.dataclass — covered later

# @functools.lru_cache example
@functools.lru_cache(maxsize=None)
def expensive_computation(n):
    """Simulates an expensive computation."""
    time.sleep(0.01)
    return n ** 2

print(f"Computing 5²: {expensive_computation(5)}")
print(f"Computing 5² (cached): {expensive_computation(5)}")
print(f"Cache info: {expensive_computation.cache_info()}")


# ===========================================================================
# 🏋️ PRACTICE EXERCISES
# ===========================================================================
"""
1. Write a decorator `uppercase` that converts a function's string return 
   value to uppercase.

2. Write a decorator `debug` that prints the function name, arguments, 
   and return value.

3. Write a decorator factory `slow_down(seconds)` that adds a delay 
   before calling the function.

4. Write a decorator `singleton` that ensures a class can only have 
   one instance.

5. Write a decorator `deprecated(message)` that prints a deprecation 
   warning when the function is called.

6. Stack the `timer` and `log_function` decorators on a function.
   What order do they execute in? Why?

7. ⭐ INTERVIEW: Explain how decorators work internally. What does 
   @decorator actually do? Why do we need functools.wraps?

8. ⭐ INTERVIEW: Write a decorator that limits a function to being 
   called at most N times, then raises an error.
"""

print("\n✅ Module 08 Complete!")
