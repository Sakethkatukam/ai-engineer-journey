## Day 1 - OOP

### 1. Instance vs Class Variables
Instance Variables
Unique to each instance of a class.
we use self parameter inside the __init__ method to set them.
Example: employee’s name, email, and salary.

Class Variables
- Shared across all instances of a class.
- Represent data that applies to all instances equally.
Example: Total number of employees,
raise_amount = 1.04 (same for every employee)
- Access via self.raise_amount works, but ClassName.raise_amount is clearer — shows you know it's a class variable

### 2. Regular vs Class vs Static Methods

Regular methods  → first arg is self (the instance, auto-passed)
Class methods    → first arg is cls (the class, auto-passed)
                   declared with @classmethod decorator
                   use: alternative constructors(methods that provide additional ways to instantiate objects), manipulate class variables
Static methods   → no auto-passed arg at all
                   declared with @staticmethod decorator
                   use: utility logic that belongs in the class but doesn't need instance or class data

### 3. Never Use Mutable Default Arguments
We should not use default argument like employees=[] #def __init__(self, employees=[]):
Why it breaks:
- Python creates the default [] ONCE when the function is defined,
  not each time the function is called
- Every instance that uses the default shares the SAME list in memory
- Adding to one instance's list silently corrupts all others

#Correct way
def __init__(self, employees=None):
    if employees is not None :
        self.employees = employees
    else:
        employees=[]

------------------------------------------

## Day 2 - Decorators , Generators

### Decorators
- A decorator is a function that takes a function and returns a new function
- @functools.wraps preserves original function name and docstring
- Decorator stacking order: bottom-up(innermost first). @classmethod/@staticmethod always on TOP
    -   @classmethod
        @my_decorator     ← correct
        def method(cls):

    -   @my_decorator
        @classmethod        ← this breaks — classmethod object is not callable
        def method(cls):
- Real use: @torch.no_grad() in PyTorch is a decorator

### Generators
- yield pauses execution and resumes on next() call
- Generator holds ~200 bytes regardless of dataset size (vs full list in RAM)
- Real use: HuggingFace loads 100GB datasets with generators
- read_in_chunks = foundation of RAG text chunking

### Key difference
- list comprehension: [x*x for x in range(n)]  → all in memory
- generator expression: (x*x for x in range(n)) → lazy, one at a time

--------------------------------------------

# Day 3 — Async/Await, Context Managers, Type Hints

## Why These Matter for LLM Engineering

 async/await       : Streaming LLM responses, calling multiple APIs simultaneously 
 Context Managers  : Managing DB connections, API sessions, file handles safely 
 Type Hints        : Every production LangChain/FastAPI codebase uses them heavily 

---

## 1. Type Hints

Type hints don't change how code runs — they document intent,catch bugs early, and power tools like FastAPI and mypy.

### Key Types to Know

from typing import Optional, Union, List, Dict, Tuple, Callable

def find_user(user_id: int) -> Optional[str]:   # can return str OR None
def process(value: Union[str, int]) -> str:      # accepts str OR int
def scores(data: List[float]) -> Dict[str, float]:
def apply(fn: Callable[[int], int], x: int) -> int:  # function as argument
def split(name: str) -> Tuple[str, str]:         # fixed-length return


### Rules
- `Optional[X]` = `Union[X, None]` — use when return can be None
- `Callable[[ArgType], ReturnType]` — used in decorators constantly
- Always annotate function arguments AND return type
- Empty return = `-> None`

---

## 2. Context Managers

Guarantees setup + teardown even if an exception occurs.
Pattern: open resource → do work → close resource (always).

### How It Works
enter  →  with body runs  →  exit (always runs, even on error)

### Three Ways to Build One

1. Class-based (full control)
2. @contextmanager (most common)
3. Async context manager (LLM streaming pattern)


### Key Rules
- `yield` inside `@contextmanager` = where the `with` body runs
- `try/finally` guarantees cleanup even on exception
- `shutil.rmtree(path)` deletes folders with contents; `os.rmdir` only deletes empty folders

---

## 3. Async / Await

### The Core Problem It Solves

SYNC:   call API_1 → wait 2s → call API_2 → wait 2s → Total: 4s
ASYNC:  call API_1 + call API_2 simultaneously     → Total: ~2s

### Key Keywords

`async def`     : This function is a coroutine — must be awaited to run
 `await`        : Pause here, let other coroutines run, resume when done
 `asyncio.gather(*coroutines)` : Run multiple coroutines concurrently
 `asyncio.run(main())` : Entry point — starts the event loop
 `async for`    : Iterate over async generator (streaming tokens)
 `async with`   : Context manager that can await in setup/teardown 

 ### Patterns

Run one coroutine:
```code
result = await fetch_data("openai.com")
```

Run many concurrently (gather):
```code
coroutines = [fetch_data(url) for url in urls]
results = await asyncio.gather(*coroutines)  # * unpacks the list
```

Async generator (how LLM streaming works):
```code
async def stream_tokens(prompt: str):
    for token in prompt.split():
        await asyncio.sleep(0.1)
        yield token

async for token in stream_tokens("Hello world"):
    print(token, end=" ")
```

-> Why one session? Creating a session opens a connection pool.
One session reused = fast. One session per request = slow + wasteful.

-> Why `async with` not `with`?
Opening/closing an HTTP session involves I/O (network).
`async with` lets the event loop do other work during that I/O.

-> What does `await response.text()` wait for?
The response body to finish downloading over the network.
The status line arrives first — body can still be in transit.

--------------------------------------------

