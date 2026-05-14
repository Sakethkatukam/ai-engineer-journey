from typing import Optional, Union, List, Dict, Tuple, Callable

# Basic
def greet(name: str, times: int = 1) -> str:
    return f"Hello {name}! " * times

# Optional = can be None
def find_user(user_id: int) -> Optional[str]:
    users = {1: "Alice", 2: "Bob"}
    return users.get(user_id)   # returns str OR None

# Union = one of multiple types
def process(value: Union[str, int]) -> str:
    return str(value).upper()

# Collections
def top_scores(scores: List[float]) -> Dict[str, float]:
    return {"max": max(scores), "min": min(scores), "avg": sum(scores)/len(scores)}

# Callable(a function as an argument)
def apply_twice(fn: Callable[[int], int], x: int) -> int:
    return fn(fn(x))

# Tuple
def split_name(full: str) -> Tuple[str, str]:
    parts = full.split(" ", 1)
    return (parts[0], parts[1])

#Testing the functions
print(greet("Dev", 2))
print(find_user(1))
print(find_user(99))      # None
print(top_scores([8.5, 9.1, 7.3]))
print(apply_twice(lambda x: x * 2, 3))
print(split_name("K Saketh"))