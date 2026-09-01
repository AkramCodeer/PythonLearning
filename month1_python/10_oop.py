"""
===============================================================================
 MODULE 10: OBJECT-ORIENTED PROGRAMMING (OOP)
===============================================================================
 ⭐ HIGH INTERVIEW IMPORTANCE — Python OOP is richer than JS classes
 
 Run this file:  python 10_oop.py
===============================================================================
"""

# ===========================================================================
# 1. CLASSES — Basics
# ===========================================================================

# JS:  class User { constructor(name, age) { this.name = name; } }
# Py:

class User:
    """A simple User class."""
    
    # Class variable (shared by ALL instances — like static in JS)
    user_count = 0
    
    def __init__(self, name, age, email):
        """Constructor — called when creating a new instance.
        
        JS equivalent: constructor(name, age, email) { ... }
        """
        # Instance variables (unique to each instance — self ≈ this in JS)
        self.name = name
        self.age = age
        self.email = email
        self._role = "user"        # Convention: _ prefix = "private"
        self.__password = "123"    # Name mangling: __ prefix = "strongly private"
        
        User.user_count += 1
    
    def greet(self):
        """Instance method — note: 'self' is required (unlike JS 'this')."""
        return f"Hello, I'm {self.name}, age {self.age}"
    
    def __str__(self):
        """Called when you print() the object or str(obj)."""
        return f"User({self.name}, {self.age})"
    
    def __repr__(self):
        """Called in debugger/REPL. Should be unambiguous."""
        return f"User(name='{self.name}', age={self.age}, email='{self.email}')"

# Creating instances
user1 = User("Akram", 25, "akram@email.com")
user2 = User("Sara", 28, "sara@email.com")

print(user1.greet())
print(f"str: {user1}")          # Calls __str__
print(f"repr: {repr(user1)}")   # Calls __repr__
print(f"Total users: {User.user_count}")


# ===========================================================================
# 2. PROPERTIES (Getters/Setters)
# ===========================================================================

print(f"\n--- Properties ---")

class Temperature:
    """Temperature with Celsius/Fahrenheit conversion."""
    
    def __init__(self, celsius=0):
        self._celsius = celsius
    
    @property
    def celsius(self):
        """Getter for celsius."""
        return self._celsius
    
    @celsius.setter
    def celsius(self, value):
        """Setter with validation."""
        if value < -273.15:
            raise ValueError("Temperature below absolute zero!")
        self._celsius = value
    
    @property
    def fahrenheit(self):
        """Computed property (like JS get keyword)."""
        return self._celsius * 9/5 + 32
    
    @fahrenheit.setter
    def fahrenheit(self, value):
        self._celsius = (value - 32) * 5/9

temp = Temperature(100)
print(f"Celsius: {temp.celsius}")        # Uses getter
print(f"Fahrenheit: {temp.fahrenheit}")  # Computed property

temp.fahrenheit = 212                     # Uses setter
print(f"After setting F=212, C={temp.celsius}")

try:
    temp.celsius = -300
except ValueError as e:
    print(f"❌ {e}")


# ===========================================================================
# 3. INHERITANCE
# ===========================================================================

print(f"\n--- Inheritance ---")

# JS: class Admin extends User { ... }
# Py:

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def introduce(self):
        return f"I'm {self.name}, {self.age} years old"

class Employee(Person):
    """Employee inherits from Person."""
    
    def __init__(self, name, age, company, salary):
        super().__init__(name, age)  # JS: super(name, age)
        self.company = company
        self.salary = salary
    
    def introduce(self):
        """Override parent method."""
        return f"{super().introduce()}, working at {self.company}"
    
    def get_annual_salary(self):
        return self.salary * 12

class Manager(Employee):
    """Manager inherits from Employee (multi-level inheritance)."""
    
    def __init__(self, name, age, company, salary, team_size):
        super().__init__(name, age, company, salary)
        self.team_size = team_size
    
    def introduce(self):
        return f"{super().introduce()}, managing {self.team_size} people"

# Usage
mgr = Manager("Akram", 25, "Google", 15000, 10)
print(mgr.introduce())
print(f"Annual salary: ${mgr.get_annual_salary():,}")
print(f"Is Employee? {isinstance(mgr, Employee)}")
print(f"Is Person? {isinstance(mgr, Person)}")


# ===========================================================================
# 4. MULTIPLE INHERITANCE & MRO
# ===========================================================================

print(f"\n--- Multiple Inheritance ---")

# Python supports multiple inheritance (JS does NOT!)

class Flyable:
    def fly(self):
        return "I can fly!"

class Swimmable:
    def swim(self):
        return "I can swim!"

class Duck(Flyable, Swimmable):
    def quack(self):
        return "Quack!"

duck = Duck()
print(f"{duck.fly()}, {duck.swim()}, {duck.quack()}")

# MRO — Method Resolution Order (how Python resolves method calls)
print(f"MRO: {[cls.__name__ for cls in Duck.__mro__]}")
# [Duck, Flyable, Swimmable, object]


# ===========================================================================
# 5. ABSTRACT CLASSES
# ===========================================================================

print(f"\n--- Abstract Classes ---")

from abc import ABC, abstractmethod

class Shape(ABC):
    """Abstract base class — cannot be instantiated."""
    
    @abstractmethod
    def area(self) -> float:
        """Subclasses MUST implement this."""
        pass
    
    @abstractmethod
    def perimeter(self) -> float:
        pass
    
    def describe(self):
        """Concrete method (optional to override)."""
        return f"{self.__class__.__name__}: area={self.area():.2f}"

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        import math
        return math.pi * self.radius ** 2
    
    def perimeter(self):
        import math
        return 2 * math.pi * self.radius

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)

# shape = Shape()  # ❌ TypeError: Can't instantiate abstract class!

circle = Circle(5)
rect = Rectangle(4, 6)

for shape in [circle, rect]:
    print(f"  {shape.describe()}, Perimeter: {shape.perimeter():.2f}")


# ===========================================================================
# 6. DUNDER (MAGIC) METHODS
# ===========================================================================

print(f"\n--- Dunder Methods ---")

class Vector:
    """A 2D vector with rich operator overloading."""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    # String representation
    def __str__(self):
        return f"Vector({self.x}, {self.y})"
    
    def __repr__(self):
        return f"Vector(x={self.x}, y={self.y})"
    
    # Arithmetic operators
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)
    
    # Comparison
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __lt__(self, other):
        return self.magnitude < other.magnitude
    
    # Container behavior
    def __len__(self):
        return 2
    
    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        raise IndexError("Vector has only 2 components")
    
    def __iter__(self):
        yield self.x
        yield self.y
    
    # Boolean
    def __bool__(self):
        return self.x != 0 or self.y != 0
    
    @property
    def magnitude(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

v1 = Vector(3, 4)
v2 = Vector(1, 2)

print(f"v1 = {v1}")
print(f"v2 = {v2}")
print(f"v1 + v2 = {v1 + v2}")
print(f"v1 - v2 = {v1 - v2}")
print(f"v1 * 3 = {v1 * 3}")
print(f"v1 == v2: {v1 == v2}")
print(f"v1[0] = {v1[0]}")
print(f"magnitude = {v1.magnitude}")
print(f"Unpacked: x={v1[0]}, y={v1[1]}")
x, y = v1  # Works because of __iter__!
print(f"Destructured: x={x}, y={y}")


# ===========================================================================
# 7. CLASS METHODS & STATIC METHODS
# ===========================================================================

print(f"\n--- Class & Static Methods ---")

class Employee2:
    raise_percentage = 1.05  # 5% raise
    employee_count = 0
    
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
        Employee2.employee_count += 1
    
    def apply_raise(self):
        """Regular method — works on instance (self)."""
        self.salary = int(self.salary * self.raise_percentage)
    
    @classmethod
    def set_raise_percentage(cls, percentage):
        """Class method — works on the CLASS, not instance.
        
        Can modify class-level state.
        """
        cls.raise_percentage = percentage
    
    @classmethod
    def from_string(cls, emp_string):
        """Alternative constructor (factory method).
        
        JS equivalent: static fromString(str) { return new Employee(...) }
        """
        name, salary = emp_string.split("-")
        return cls(name, int(salary))
    
    @staticmethod
    def is_workday(day):
        """Static method — doesn't access instance OR class.
        
        Just a utility function that belongs to this class.
        """
        return day.weekday() < 5

# Class method usage
Employee2.set_raise_percentage(1.10)  # 10% raise for everyone

# Alternative constructor
emp = Employee2.from_string("Akram-50000")
print(f"From string: {emp.name}, ${emp.salary}")

# Static method
import datetime
today = datetime.date.today()
print(f"Is workday? {Employee2.is_workday(today)}")


# ===========================================================================
# 8. DATACLASSES (Modern Python — Reduces Boilerplate)
# ===========================================================================

print(f"\n--- Dataclasses ---")

from dataclasses import dataclass, field

@dataclass
class Product:
    """Automatically generates __init__, __repr__, __eq__, etc."""
    name: str
    price: float
    quantity: int = 0
    tags: list = field(default_factory=list)  # Mutable default!
    
    @property
    def total_value(self):
        return self.price * self.quantity

# No need to write __init__!
p1 = Product("Laptop", 999.99, 5)
p2 = Product("Phone", 699.99, 10, tags=["mobile", "electronics"])
p3 = Product("Laptop", 999.99, 5)

print(f"p1: {p1}")                     # Auto-generated __repr__
print(f"p1 == p3: {p1 == p3}")         # Auto-generated __eq__
print(f"Total: ${p1.total_value:,.2f}")

# Frozen dataclass (immutable)
@dataclass(frozen=True)
class Point:
    x: float
    y: float

pt = Point(3, 4)
# pt.x = 5  # ❌ FrozenInstanceError!
print(f"Point: {pt}")


# ===========================================================================
# 9. ENCAPSULATION CONVENTIONS
# ===========================================================================

print(f"\n--- Encapsulation ---")

"""
Python's approach to encapsulation (compared to JS):

JS:  #privateField (actual private with #)
Py:  _protected    (convention: "please don't use from outside")
     __private     (name mangling: makes it harder to access)
     __dunder__    (special/magic methods — NOT private!)

Python philosophy: "We're all consenting adults here"
— No strict enforcement, just conventions.
"""

class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner           # Public
        self._balance = balance      # Protected (convention)
        self.__pin = "1234"          # Private (name-mangled)
    
    @property
    def balance(self):
        return self._balance
    
    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
    
    def withdraw(self, amount):
        if 0 < amount <= self._balance:
            self._balance -= amount
            return amount
        raise ValueError("Invalid withdrawal")

acc = BankAccount("Akram", 1000)
print(f"Balance: {acc.balance}")   # Uses property
acc.deposit(500)
print(f"After deposit: {acc.balance}")

# Name mangling: __pin becomes _BankAccount__pin
# Still accessible, but intentionally awkward:
print(f"Mangled: {acc._BankAccount__pin}")  # "1234" (not truly private!)


# ===========================================================================
# 10. SLOTS (Performance Optimization)
# ===========================================================================

print(f"\n--- Slots ---")

class RegularClass:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class SlottedClass:
    __slots__ = ('x', 'y')  # Fixed attributes — saves memory!
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

import sys
regular = RegularClass(1, 2)
slotted = SlottedClass(1, 2)

print(f"Regular size: {sys.getsizeof(regular.__dict__)} bytes (has __dict__)")
print(f"Slotted: no __dict__ (more memory efficient)")

# slotted.z = 3  # ❌ AttributeError! Can't add new attributes


# ===========================================================================
# 🏋️ PRACTICE EXERCISES
# ===========================================================================
"""
1. Create a BankAccount class with deposit, withdraw, and transfer methods.
   Use @property for balance (read-only).

2. Create a Shape hierarchy: Shape (abstract) → Circle, Rectangle, Triangle.
   Each must implement area() and perimeter().

3. Create a Stack class using a list internally, with push, pop, peek,
   is_empty, and __len__ methods.

4. Create a Student dataclass with name, grades (list), and a computed 
   property for average grade.

5. Implement a LinkedList class with append, prepend, __str__, and 
   __len__ methods.

6. ⭐ INTERVIEW: Explain MRO in Python. What happens with diamond 
   inheritance?

7. ⭐ INTERVIEW: What's the difference between @classmethod and 
   @staticmethod? Give real use cases.

8. ⭐ INTERVIEW: Explain Python's __slots__. When and why would you use it?

9. ⭐ INTERVIEW: How does name mangling work with __ prefix? Is it truly private?

10. ⭐ INTERVIEW: What are dunder methods? Name 5 and explain when they're called.
"""

print("\n✅ Module 10 Complete!")
