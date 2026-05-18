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

## Day 4

╔══════════════════════════════════════════════════════════════╗
║           DAY 4 NOTES — Git + File I/O + CLI Tracker        ║
║           Week 1 · Phase 1 · Foundation                     ║
╚══════════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GIT CORE WORKFLOW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Three layers:
  Working Directory → Staging Area → Repository
  (your files)         (git add)      (git commit)

Daily commands:
  git status                      always run first
  git add .                       stage all changes
  git commit -m "message"         save snapshot
  git push origin main            upload to GitHub
  git pull origin main            download latest

Branch workflow:
  git checkout -b feature/name    create + switch
  git checkout main               switch back
  git merge feature/name          bring changes in
  git branch -D feature/name      delete branch

History:
  git log --oneline               compact history
  git diff                        what changed

Merge conflict — when it happens:
  Both branches must have NEW commits on the SAME line
  after they diverged. If only one side changed → fast-forward.

Conflict markers:
  <<<<<<< HEAD          ← your current branch version
  your version
  =======
  their version
  >>>>>>> branch-name   ← incoming branch version

  Fix: delete markers, keep what you want, then:
  git add file.py
  git commit -m "fix: resolve conflict"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ARGPARSE — CLI ARGUMENT PARSING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

What it does:
  Converts command-line strings into a Python args object
  "add --amount 250" → args.command="add", args.amount=250.0

Setup pattern:
  parser = argparse.ArgumentParser(prog="tool", description="...")
  subparsers = parser.add_subparsers(dest="command", required=True)

  sub = subparsers.add_parser("add", help="Add something")
  sub.add_argument("--name", "-n", required=True, type=str)
  sub.add_argument("--amount", "-a", required=True, type=float)
  sub.add_argument("--category", "-c", default="general")

  args = parser.parse_args()

Argument options:
  required=True       must be provided
  type=float/int      auto-convert from string
  default="general"   used if argument missing
  help="..."          shown in --help

Accessing values:
  args.command        which subcommand was called
  args.amount         the float value
  args.description    the string value

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FILE I/O — READING AND WRITING FILES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Three modes:
  "r"  read   — file must exist
  "w"  write  — creates or overwrites
  "a"  append — adds to end

Always use with block:
  with open("file.txt", "r") as f:
      content = f.read()
  # file auto-closed even if error occurs

JSON operations:
  import json

  # Write dict to file
  with open("data.json", "w") as f:
      json.dump(data, f, indent=2)

  # Read file to dict
  with open("data.json", "r") as f:
      data = json.load(f)

  # String conversions (no file)
  text = json.dumps(data)        # dict → string
  data = json.loads(text)        # string → dict

  KEY DIFFERENCE:
    json.load(f)   → reads from FILE OBJECT
    json.loads(s)  → reads from STRING
    (the 's' in loads = string)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PATHLIB — MODERN FILE PATH HANDLING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Why pathlib over os.path:
  Path is an OBJECT with methods, not just a string
  / operator joins paths safely on any OS (Windows/Linux/Mac)
  Has direct read/write methods — no need for open()

Creating paths:
  Path("data/file.json")             from string
  Path(__file__).parent / "file.json" relative to current script
  Path("folder") / "sub" / "file"    join multiple parts

Key methods:
  p.exists()                         True/False
  p.parent.mkdir(exist_ok=True)      create folder safely
  p.read_text(encoding="utf-8")      entire file as string
  p.write_text("...", encoding="utf-8") write string to file

Key properties:
  p.name      "expenses.json"    full filename
  p.stem      "expenses"         without extension
  p.suffix    ".json"            just extension
  p.parent    Path("data")       containing folder

Standard project pattern:
  DATA_FILE = Path(__file__).parent / "data.json"

  def load():
      if not DATA_FILE.exists():
          return []
      return json.loads(DATA_FILE.read_text(encoding="utf-8"))

  def save(data):
      DATA_FILE.write_text(
          json.dumps(data, indent=2), encoding="utf-8"
      )

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
F-STRING FORMAT SPECIFIERS — COLUMN ALIGNMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Pattern: f"{value : align width .decimals}"

Alignment:
  <   left-align   (default for strings)
  >   right-align  (default for numbers)
  ^   center

Examples:
  f"{'food':<10}"    →  'food      '   (10 wide, left)
  f"{'food':>10}"    →  '      food'   (10 wide, right)
  f"{'food':^10}"    →  '   food   '   (10 wide, center)

For numbers:
  f"{250.0:>10.2f}"  →  '    250.00'  (10 wide, right, 2 decimals)
  f"{250.0:<10.2f}"  →  '250.00    '  (10 wide, left,  2 decimals)

Why it matters:
  Without it: columns misalign when values have different lengths
  With it:    every row lines up perfectly in a table

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
self.expenses — HOW OOP STATE WORKS IN THE TRACKER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

self = the instance of the class (the specific object created)
self.expenses = the list that belongs to THAT object

Full lifecycle every run:
  1. main() creates: tracker = ExpenseTracker()
  2. __init__ runs:  self.expenses = load_expenses()
                     → reads expenses.json into memory
  3. Command runs:   tracker.add() / remove() / list()
                     → modifies self.expenses in memory
                     → calls save_expenses() to write back to JSON
  4. Script ends:    memory wiped. JSON file persists on disk.

Why load → modify → save every time:
  Python memory is temporary. Disk (JSON) is permanent.
  JSON is your database. self.expenses is the working copy.

How remove() works:
  self.expenses = [e for e in self.expenses if e["id"] != id]
  # builds new list keeping everything EXCEPT the target id
  # then saves the shorter list to JSON

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━