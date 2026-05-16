#Timer
from functools import wraps
import time

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start=time.time()
        result=func(*args, **kwargs)
        end=time.time()
        print(f"TIMER: {func.__name__} ran in {end-start} seconds")
        return result
    return wrapper

@timer
def slow_function(n:int)->str:
    time.sleep(n)
    return "done"

# slow_function(2)

#Logger
def logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"LOG: Calling {func.__name__!r} with args: {args} and kwargs: {kwargs}")
        result=func(*args,**kwargs)
        print(f"LOG: {func.__name__!r} returned {result!r}")
        return result
    return wrapper

@logger
def add(a:int, b:int)->int:
    return a+b

# add(3,6)
# add(10, b=20)

#cache
def cache(func):
    results={}
    @wraps(func)
    def wrapper(*args):
        if args in results:
            print(f"CACHE: Returning cached result for {args}")
            return results[args]
        result=func(*args)
        results[args]=result
        return result
    return wrapper

@cache
def slow_multiply(a:int, b:int)->int:
    time.sleep(1)
    return a*b

# print(slow_multiply(3,4))
# print(slow_multiply(3,4))
# print(slow_multiply(2,10))

@timer
@logger
def batch(batch_size:int)->str:
    time.sleep(1)
    return f"processed {batch_size} items"

batch(32)