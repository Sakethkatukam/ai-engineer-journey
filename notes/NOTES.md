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

## Day 3 Plan - Async, Context Managers, Type Hints
- async/await and why it matters for LLM streaming
- context managers (with statement)
- type hints - annotating all my previous functions
- build: async web scraper with aiohttp