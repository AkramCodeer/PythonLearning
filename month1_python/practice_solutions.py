"""
===============================================================================
 PRACTICE SOLUTIONS — Solutions to all 50 problems
===============================================================================
 ⚠️ TRY SOLVING ON YOUR OWN FIRST before looking here!
 
 Run this file:  python practice_solutions.py
===============================================================================
"""

from collections import Counter, defaultdict
from functools import reduce, wraps
import asyncio
import time


# ===========================================================================
# CATEGORY 1: STRINGS (Problems 1-10)
# ===========================================================================

# Problem 1: Reverse a string
def reverse_string(s):
    return s[::-1]

# Problem 2: Check palindrome (ignore case and spaces)
def is_palindrome(s):
    cleaned = ''.join(c.lower() for c in s if c.isalnum())
    return cleaned == cleaned[::-1]

# Problem 3: Count vowels and consonants
def count_vowels_consonants(s):
    s = s.lower()
    vowels = sum(1 for c in s if c in 'aeiou')
    consonants = sum(1 for c in s if c.isalpha() and c not in 'aeiou')
    return {"vowels": vowels, "consonants": consonants}

# Problem 4: Most frequent character
def most_frequent_char(s):
    s = s.replace(" ", "")
    return Counter(s).most_common(1)[0][0]

# Problem 5: Check anagrams
def are_anagrams(s1, s2):
    return sorted(s1.lower()) == sorted(s2.lower())

# Problem 6: Remove duplicate characters
def remove_duplicates(s):
    seen = set()
    result = []
    for c in s:
        if c not in seen:
            seen.add(c)
            result.append(c)
    return ''.join(result)

# Problem 7: Capitalize first letter of each word
def capitalize_words(s):
    return ' '.join(word.capitalize() for word in s.split())

# Problem 8: Run-length encoding
def compress_string(s):
    if not s:
        return ""
    result = []
    count = 1
    for i in range(1, len(s)):
        if s[i] == s[i-1]:
            count += 1
        else:
            result.append(f"{s[i-1]}{count}")
            count = 1
    result.append(f"{s[-1]}{count}")
    return ''.join(result)

# Problem 9: All unique characters
def all_unique(s):
    return len(set(s)) == len(s)

# Problem 10: Longest word
def longest_word(s):
    return max(s.split(), key=len)


# ===========================================================================
# CATEGORY 2: LISTS (Problems 11-20)
# ===========================================================================

# Problem 11: Second largest
def second_largest(nums):
    unique = list(set(nums))
    unique.sort()
    return unique[-2]

# Problem 12: Remove duplicates (preserve order)
def remove_list_duplicates(lst):
    return list(dict.fromkeys(lst))

# Problem 13: Flatten nested list
def flatten(lst):
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result

# Problem 14: Rotate list
def rotate_list(lst, k):
    k = k % len(lst)
    return lst[-k:] + lst[:-k]

# Problem 15: Find pairs summing to target
def find_pairs(nums, target):
    seen = set()
    pairs = []
    for num in nums:
        complement = target - num
        if complement in seen and (complement, num) not in pairs:
            pairs.append((min(num, complement), max(num, complement)))
        seen.add(num)
    return sorted(pairs)

# Problem 16: Merge sorted lists
def merge_sorted(list1, list2):
    result = []
    i = j = 0
    while i < len(list1) and j < len(list2):
        if list1[i] <= list2[j]:
            result.append(list1[i])
            i += 1
        else:
            result.append(list2[j])
            j += 1
    result.extend(list1[i:])
    result.extend(list2[j:])
    return result

# Problem 17: Find missing number
def find_missing(nums):
    n = max(nums)
    expected = n * (n + 1) // 2
    return expected - sum(nums)

# Problem 18: Group by key function
def group_by(lst, key_func):
    result = defaultdict(list)
    for item in lst:
        result[key_func(item)].append(item)
    return dict(result)

# Problem 19: List intersection
def list_intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))

# Problem 20: Chunk list
def chunk_list(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]


# ===========================================================================
# CATEGORY 3: DICTIONARIES (Problems 21-28)
# ===========================================================================

# Problem 21: Merge dicts summing common keys
def merge_dicts_sum(d1, d2):
    result = d1.copy()
    for k, v in d2.items():
        result[k] = result.get(k, 0) + v
    return result

# Problem 22: Invert dict
def invert_dict(d):
    return {v: k for k, v in d.items()}

# Problem 23: Key with max value
def max_value_key(d):
    return max(d, key=d.get)

# Problem 24: Word frequency
def word_frequency(sentence):
    return dict(Counter(sentence.split()))

# Problem 25: Flatten nested dict
def flatten_dict(d, parent_key="", sep="."):
    items = {}
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(flatten_dict(v, new_key, sep))
        else:
            items[new_key] = v
    return items

# Problem 26: Group list of dicts by key
def group_dicts_by(lst, key):
    result = defaultdict(list)
    for item in lst:
        result[item[key]].append(item)
    return dict(result)

# Problem 27: Deep merge
def deep_merge(d1, d2):
    result = d1.copy()
    for k, v in d2.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = deep_merge(result[k], v)
        else:
            result[k] = v
    return result

# Problem 28: Sort dict by value
def sort_dict_by_value(d):
    return dict(sorted(d.items(), key=lambda x: x[1]))


# ===========================================================================
# CATEGORY 4: FUNCTIONS & COMPREHENSIONS (Problems 29-36)
# ===========================================================================

# Problem 29: Memoize decorator
def memoize(func):
    cache = {}
    @wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper

# Problem 30: Compose
def compose(f, g):
    return lambda x: f(g(x))

# Problem 31: FizzBuzz
def fizzbuzz(n):
    return [
        "FizzBuzz" if i % 15 == 0
        else "Fizz" if i % 3 == 0
        else "Buzz" if i % 5 == 0
        else str(i)
        for i in range(1, n + 1)
    ]

# Problem 32: Transpose
def transpose(matrix):
    return [[row[i] for row in matrix] for i in range(len(matrix[0]))]

# Problem 33: Pascal's Triangle
def pascal_triangle(n):
    if n == 0:
        return []
    triangle = [[1]]
    for i in range(1, n):
        prev = triangle[-1]
        row = [1]
        for j in range(1, len(prev)):
            row.append(prev[j-1] + prev[j])
        row.append(1)
        triangle.append(row)
    return triangle

# Problem 34: Pipe
def pipe(*functions):
    def piped(x):
        result = x
        for func in functions:
            result = func(result)
        return result
    return piped

# Problem 35: Float range
def float_range(start, stop, step):
    result = []
    current = start
    while current < stop:
        result.append(round(current, 10))
        current += step
    return result

# Problem 36: Retry with backoff
def retry_with_backoff(max_retries=3, base_delay=0.1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    delay = base_delay * (2 ** attempt)
                    time.sleep(delay)
        return wrapper
    return decorator


# ===========================================================================
# CATEGORY 5: OOP (Problems 37-42)
# ===========================================================================

# Problem 37: Stack
class Stack:
    def __init__(self):
        self._items = []
    
    def push(self, item):
        self._items.append(item)
    
    def pop(self):
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self._items.pop()
    
    def peek(self):
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self._items[-1]
    
    def is_empty(self):
        return len(self._items) == 0
    
    def size(self):
        return len(self._items)
    
    def __str__(self):
        return f"Stack({self._items})"

# Problem 38: Queue
class Queue:
    def __init__(self):
        self._items = []
    
    def enqueue(self, item):
        self._items.append(item)
    
    def dequeue(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self._items.pop(0)
    
    def peek(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self._items[0]
    
    def is_empty(self):
        return len(self._items) == 0
    
    def size(self):
        return len(self._items)
    
    def __str__(self):
        return f"Queue({self._items})"

# Problem 39: LinkedList
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self._length = 0
    
    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self._length += 1
    
    def prepend(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self._length += 1
    
    def delete(self, data):
        if not self.head:
            return
        if self.head.data == data:
            self.head = self.head.next
            self._length -= 1
            return
        current = self.head
        while current.next:
            if current.next.data == data:
                current.next = current.next.next
                self._length -= 1
                return
            current = current.next
    
    def find(self, data):
        current = self.head
        while current:
            if current.data == data:
                return True
            current = current.next
        return False
    
    def __str__(self):
        items = []
        current = self.head
        while current:
            items.append(str(current.data))
            current = current.next
        return " → ".join(items) + " → None"
    
    def __len__(self):
        return self._length

# Problem 40: BankAccount
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self._balance = balance
        self._history = []
    
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self._balance += amount
        self._history.append(f"+${amount:.2f}")
        return self._balance
    
    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal must be positive")
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount
        self._history.append(f"-${amount:.2f}")
        return self._balance
    
    def get_balance(self):
        return self._balance
    
    def get_history(self):
        return self._history.copy()
    
    def __str__(self):
        return f"BankAccount({self.owner}, ${self._balance:.2f})"

# Problem 41: EventEmitter
class EventEmitter:
    def __init__(self):
        self._events = defaultdict(list)
    
    def on(self, event, callback):
        self._events[event].append(callback)
    
    def emit(self, event, *args):
        for callback in self._events.get(event, []):
            callback(*args)
    
    def off(self, event, callback):
        if event in self._events:
            self._events[event] = [
                cb for cb in self._events[event] if cb != callback
            ]

# Problem 42: LRU Cache
class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.order = []
    
    def get(self, key):
        if key in self.cache:
            self.order.remove(key)
            self.order.append(key)
            return self.cache[key]
        return -1
    
    def put(self, key, value):
        if key in self.cache:
            self.order.remove(key)
        elif len(self.cache) >= self.capacity:
            oldest = self.order.pop(0)
            del self.cache[oldest]
        self.cache[key] = value
        self.order.append(key)


# ===========================================================================
# CATEGORY 6: GENERATORS & ADVANCED (Problems 43-50)
# ===========================================================================

# Problem 43: Prime generator
def prime_generator():
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True
    
    n = 2
    while True:
        if is_prime(n):
            yield n
        n += 1

# Problem 44: Fibonacci generator
def fib_generator():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# Problem 45: Generator pipeline
def pipeline_demo():
    numbers = range(1, 100)
    evens = (x for x in numbers if x % 2 == 0)
    squared = (x**2 for x in evens)
    import itertools
    return list(itertools.islice(squared, 5))

# Problem 46: CSV parser generator
def parse_csv(csv_string):
    lines = csv_string.strip().split("\n")
    headers = lines[0].split(",")
    for line in lines[1:]:
        values = line.split(",")
        yield dict(zip(headers, values))

# Problem 47: Timer context manager
class Timer:
    def __enter__(self):
        self.start = time.perf_counter()
        return self
    
    def __exit__(self, *args):
        self.elapsed = time.perf_counter() - self.start
        return False

# Problem 48: Timing decorator
def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"  {func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

# Problem 50: Binary search
def binary_search_iterative(arr, target):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

def binary_search_recursive(arr, target, low=0, high=None):
    if high is None:
        high = len(arr) - 1
    if low > high:
        return -1
    mid = (low + high) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, high)
    else:
        return binary_search_recursive(arr, target, low, mid - 1)


# ===========================================================================
# RUN ALL TESTS
# ===========================================================================

def test(name, actual, expected):
    status = "✅" if actual == expected else "❌"
    print(f"  {status} {name}")
    if actual != expected:
        print(f"     Expected: {expected}")
        print(f"     Got:      {actual}")

if __name__ == "__main__":
    print("=" * 60)
    print("RUNNING ALL TESTS")
    print("=" * 60)
    
    # Strings
    print("\n📝 Strings:")
    test("reverse_string", reverse_string("Hello World"), "dlroW olleH")
    test("is_palindrome", is_palindrome("A man a plan a canal Panama"), True)
    test("count_vowels", count_vowels_consonants("Hello World"), {"vowels": 3, "consonants": 7})
    test("most_frequent", most_frequent_char("hello world"), "l")
    test("anagrams", are_anagrams("listen", "silent"), True)
    test("remove_dups", remove_duplicates("programming"), "progamin")
    test("capitalize", capitalize_words("hello world python"), "Hello World Python")
    test("compress", compress_string("aaabbbccdddd"), "a3b3c2d4")
    test("all_unique", all_unique("abcdef"), True)
    test("longest_word", longest_word("The quick brown fox"), "quick")
    
    # Lists
    print("\n📝 Lists:")
    test("second_largest", second_largest([3,1,4,1,5,9,2,6]), 6)
    test("remove_dups", remove_list_duplicates([1,3,2,3,1,4,2]), [1,3,2,4])
    test("flatten", flatten([1,[2,3],[4,[5,6]],7]), [1,2,3,4,5,6,7])
    test("rotate", rotate_list([1,2,3,4,5], 2), [4,5,1,2,3])
    test("find_pairs", find_pairs([1,2,3,4,5], 6), [(1,5),(2,4)])
    test("merge_sorted", merge_sorted([1,3,5],[2,4,6]), [1,2,3,4,5,6])
    test("find_missing", find_missing([1,2,4,5,6]), 3)
    test("chunk", chunk_list([1,2,3,4,5,6,7], 3), [[1,2,3],[4,5,6],[7]])
    
    # Dicts
    print("\n📝 Dictionaries:")
    test("merge_sum", merge_dicts_sum({"a":1,"b":2}, {"b":3,"c":4}), {"a":1,"b":5,"c":4})
    test("invert", invert_dict({"a":1,"b":2}), {1:"a",2:"b"})
    test("max_key", max_value_key({"a":10,"b":25,"c":15}), "b")
    test("flatten_dict", flatten_dict({"a":{"b":1,"c":{"d":2}}}), {"a.b":1,"a.c.d":2})
    test("sort_by_val", sort_dict_by_value({"b":3,"a":1,"c":2}), {"a":1,"c":2,"b":3})
    
    # Functions
    print("\n📝 Functions:")
    test("fizzbuzz[0]", fizzbuzz(15)[0], "1")
    test("fizzbuzz[2]", fizzbuzz(15)[2], "Fizz")
    test("fizzbuzz[4]", fizzbuzz(15)[4], "Buzz")
    test("fizzbuzz[14]", fizzbuzz(15)[14], "FizzBuzz")
    test("transpose", transpose([[1,2,3],[4,5,6]]), [[1,4],[2,5],[3,6]])
    test("pascal", pascal_triangle(5), [[1],[1,1],[1,2,1],[1,3,3,1],[1,4,6,4,1]])
    test("pipeline", pipeline_demo(), [4, 16, 36, 64, 100])
    
    # OOP
    print("\n📝 OOP:")
    s = Stack()
    s.push(1); s.push(2); s.push(3)
    test("stack_peek", s.peek(), 3)
    test("stack_pop", s.pop(), 3)
    test("stack_size", s.size(), 2)
    
    ll = LinkedList()
    ll.append(1); ll.append(2); ll.append(3)
    test("ll_find", ll.find(2), True)
    test("ll_len", len(ll), 3)
    
    ba = BankAccount("Akram", 1000)
    ba.deposit(500)
    ba.withdraw(200)
    test("bank_balance", ba.get_balance(), 1300)
    test("bank_history", len(ba.get_history()), 2)
    
    ee = EventEmitter()
    results = []
    ee.on("test", lambda x: results.append(x))
    ee.emit("test", 42)
    test("event_emitter", results, [42])
    
    lru = LRUCache(2)
    lru.put("a", 1); lru.put("b", 2)
    test("lru_get", lru.get("a"), 1)
    lru.put("c", 3)  # Evicts "b"
    test("lru_evict", lru.get("b"), -1)
    
    # Generators
    print("\n📝 Generators:")
    pg = prime_generator()
    first_5_primes = [next(pg) for _ in range(5)]
    test("primes", first_5_primes, [2, 3, 5, 7, 11])
    
    fg = fib_generator()
    first_8_fib = [next(fg) for _ in range(8)]
    test("fibonacci", first_8_fib, [0, 1, 1, 2, 3, 5, 8, 13])
    
    # Binary search
    test("binary_iter", binary_search_iterative([1,3,5,7,9], 5), 2)
    test("binary_recur", binary_search_recursive([1,3,5,7,9], 5), 2)
    test("binary_miss", binary_search_iterative([1,3,5,7,9], 4), -1)
    
    print(f"\n{'=' * 60}")
    print("🎉 All tests complete!")
    print("=" * 60)
