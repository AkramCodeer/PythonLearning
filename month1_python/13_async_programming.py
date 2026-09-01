"""
===============================================================================
 MODULE 13: ASYNC/AWAIT
===============================================================================
 Async Python — your Node.js async skills transfer directly!
 
 Run this file:  python 13_async_programming.py
===============================================================================
"""

import asyncio
import time


# ===========================================================================
# 1. SYNC vs ASYNC — The Coffee Shop Analogy
# ===========================================================================
"""
SYNCHRONOUS (blocking):
  You order coffee → wait → get coffee → order food → wait → get food
  Total time = coffee_time + food_time

ASYNCHRONOUS (non-blocking):
  You order coffee → order food → wait → get coffee → get food
  Total time = max(coffee_time, food_time)

You already know this from Node.js! Python's async works the same way.

JS:   async function fetchData() { await fetch(...) }
Py:   async def fetch_data(): await aiohttp.get(...)
"""


# ===========================================================================
# 2. SYNCHRONOUS EXAMPLE (Blocking)
# ===========================================================================

def sync_task(name, duration):
    """Simulate a blocking task."""
    print(f"  ⏳ Starting {name}...")
    time.sleep(duration)  # BLOCKS the entire program!
    print(f"  ✅ {name} done!")
    return f"{name} result"

print("--- Synchronous ---")
start = time.perf_counter()
sync_task("Task A", 1)
sync_task("Task B", 1)
sync_task("Task C", 1)
end = time.perf_counter()
print(f"  Total: {end - start:.2f}s (all sequential)\n")


# ===========================================================================
# 3. ASYNCHRONOUS EXAMPLE (Non-Blocking)
# ===========================================================================

async def async_task(name, duration):
    """Simulate a non-blocking task."""
    print(f"  ⏳ Starting {name}...")
    await asyncio.sleep(duration)  # Non-blocking sleep!
    print(f"  ✅ {name} done!")
    return f"{name} result"

async def main_concurrent():
    """Run tasks concurrently."""
    start = time.perf_counter()
    
    # JS:  await Promise.all([taskA(), taskB(), taskC()])
    # Py:  await asyncio.gather(taskA(), taskB(), taskC())
    results = await asyncio.gather(
        async_task("Task A", 1),
        async_task("Task B", 1),
        async_task("Task C", 1),
    )
    
    end = time.perf_counter()
    print(f"  Results: {results}")
    print(f"  Total: {end - start:.2f}s (all concurrent!)\n")

print("--- Asynchronous ---")
asyncio.run(main_concurrent())  # Entry point for async code


# ===========================================================================
# 4. ASYNC FUNDAMENTALS
# ===========================================================================

# --- Coroutines ---
async def my_coroutine():
    """An async function creates a coroutine object."""
    return "Hello from coroutine!"

# Calling an async function doesn't execute it — it returns a coroutine!
coro = my_coroutine()
print(f"Coroutine object: {coro}")

# You MUST await it or pass it to asyncio.run()
async def run_it():
    result = await coro
    print(f"Result: {result}")

asyncio.run(run_it())


# ===========================================================================
# 5. asyncio.gather() vs asyncio.create_task()
# ===========================================================================

print(f"\n--- gather vs create_task ---")

async def fetch_user(user_id):
    await asyncio.sleep(0.5)
    return {"id": user_id, "name": f"User {user_id}"}

async def demo_gather():
    """gather() — run multiple coroutines, wait for ALL."""
    # JS: Promise.all([...])
    users = await asyncio.gather(
        fetch_user(1),
        fetch_user(2),
        fetch_user(3),
    )
    print(f"  gather results: {users}")

async def demo_tasks():
    """create_task() — fire and forget, then await later."""
    # Start tasks immediately
    task1 = asyncio.create_task(fetch_user(1))
    task2 = asyncio.create_task(fetch_user(2))
    
    # Do other work while tasks run...
    print(f"  Tasks created, doing other work...")
    
    # Then collect results
    user1 = await task1
    user2 = await task2
    print(f"  task results: {user1}, {user2}")

asyncio.run(demo_gather())
asyncio.run(demo_tasks())


# ===========================================================================
# 6. ERROR HANDLING IN ASYNC
# ===========================================================================

print(f"\n--- Async Error Handling ---")

async def risky_task(name, should_fail=False):
    await asyncio.sleep(0.1)
    if should_fail:
        raise ValueError(f"{name} failed!")
    return f"{name} succeeded"

async def demo_error_handling():
    # Method 1: Try/except on individual awaits
    try:
        result = await risky_task("Task", should_fail=True)
    except ValueError as e:
        print(f"  Caught: {e}")
    
    # Method 2: gather with return_exceptions=True
    # JS: Promise.allSettled([...])
    results = await asyncio.gather(
        risky_task("A"),
        risky_task("B", should_fail=True),
        risky_task("C"),
        return_exceptions=True  # Don't crash, collect errors
    )
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"  Task {i}: ❌ {result}")
        else:
            print(f"  Task {i}: ✅ {result}")

asyncio.run(demo_error_handling())


# ===========================================================================
# 7. TIMEOUTS
# ===========================================================================

print(f"\n--- Timeouts ---")

async def slow_operation():
    await asyncio.sleep(10)
    return "Completed"

async def demo_timeout():
    # JS: Promise.race([promise, timeoutPromise])
    try:
        result = await asyncio.wait_for(slow_operation(), timeout=1.0)
        print(f"  Result: {result}")
    except asyncio.TimeoutError:
        print(f"  ⏰ Operation timed out after 1 second!")

asyncio.run(demo_timeout())


# ===========================================================================
# 8. ASYNC GENERATORS & ITERATORS
# ===========================================================================

print(f"\n--- Async Generators ---")

async def async_range(start, stop, delay=0.1):
    """Async generator — yields values with delays."""
    for i in range(start, stop):
        await asyncio.sleep(delay)
        yield i

async def demo_async_gen():
    # async for — iterate over async generator
    print("  Counting: ", end="")
    async for num in async_range(1, 6, 0.1):
        print(f"{num} ", end="")
    print()

asyncio.run(demo_async_gen())

# Async comprehension
async def demo_async_comprehension():
    results = [num async for num in async_range(1, 6, 0.05)]
    print(f"  Async comprehension: {results}")

asyncio.run(demo_async_comprehension())


# ===========================================================================
# 9. SEMAPHORES (Rate Limiting)
# ===========================================================================

print(f"\n--- Semaphores ---")

async def limited_task(semaphore, task_id):
    async with semaphore:  # Only N tasks run concurrently
        print(f"  Task {task_id} started")
        await asyncio.sleep(0.5)
        print(f"  Task {task_id} done")

async def demo_semaphore():
    sem = asyncio.Semaphore(2)  # Max 2 concurrent tasks
    
    tasks = [limited_task(sem, i) for i in range(5)]
    await asyncio.gather(*tasks)

asyncio.run(demo_semaphore())


# ===========================================================================
# 10. REAL-WORLD PATTERN: Async API Calls
# ===========================================================================

print(f"\n--- Real-World Pattern ---")

# Simulating API calls (in real code, use aiohttp or httpx)
async def fetch_data(url, delay=0.3):
    """Simulate an API call."""
    await asyncio.sleep(delay)
    return {"url": url, "status": 200, "data": f"Response from {url}"}

async def fetch_all_apis():
    """Fetch multiple APIs concurrently."""
    urls = [
        "https://api.example.com/users",
        "https://api.example.com/posts",
        "https://api.example.com/comments",
        "https://api.example.com/todos",
    ]
    
    start = time.perf_counter()
    
    # Create tasks for all URLs
    tasks = [fetch_data(url) for url in urls]
    results = await asyncio.gather(*tasks)
    
    elapsed = time.perf_counter() - start
    
    for result in results:
        print(f"  {result['url']}: {result['status']}")
    
    print(f"  All {len(urls)} APIs fetched in {elapsed:.2f}s (concurrent!)")

asyncio.run(fetch_all_apis())


# ===========================================================================
# 11. COMPARISON: JS vs PYTHON ASYNC
# ===========================================================================

"""
JavaScript                          Python
─────────────────────────────       ──────────────────────────────
async function fn() { }             async def fn():
await promise                       await coroutine
Promise.all([...])                  asyncio.gather(...)
Promise.race([...])                 asyncio.wait(FIRST_COMPLETED)
Promise.allSettled([...])           asyncio.gather(return_exceptions=True)
new Promise((resolve) => ...)       asyncio.Future() (rarely used)
setTimeout(fn, ms)                  asyncio.sleep(seconds)
setInterval(fn, ms)                 while loop with asyncio.sleep()
fetch(url)                          aiohttp.get(url) or httpx.get(url)

Key Differences:
1. Python needs asyncio.run() to start — JS auto-runs
2. Python uses asyncio.gather() — JS uses Promise.all()
3. Python's async is single-threaded (like Node.js!)
4. For CPU-bound work, use multiprocessing, not asyncio
"""


# ===========================================================================
# 🏋️ PRACTICE EXERCISES
# ===========================================================================
"""
1. Write an async function that simulates downloading 5 files concurrently,
   each taking a random amount of time (0.5-2 seconds).

2. Write an async function with a 2-second timeout that handles the 
   timeout gracefully.

3. Create an async generator that yields random numbers with a delay,
   and consume it with async for.

4. Use a semaphore to limit concurrent API calls to 3 at a time,
   while processing 10 requests.

5. ⭐ INTERVIEW: Explain the difference between threading, multiprocessing,
   and asyncio in Python. When would you use each?

6. ⭐ INTERVIEW: What is the GIL? How does it affect async programming?

7. ⭐ INTERVIEW: Compare Python's asyncio with Node.js event loop.
"""

print("\n✅ Module 13 Complete!")
