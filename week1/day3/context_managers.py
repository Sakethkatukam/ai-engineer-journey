#Method-1(class based)
class DBConnection:
    def __init__(self,db_name:str)->None:
        self.db_name=db_name
        self.connection=None
    def __enter__(self)->"DBConnection":
        print(f"connecting to {self.db_name}")
        self.connection=f"connection : {self.db_name}"
        return self
    def __exit__(self,exc_type,exc_val,exc_traceback)->None:
        print(f"Closing {self.db_name} connection" )
        self.connection=None
        return False
with DBConnection("my_database") as db:
    print(f"using {db.connection}")

#Method-2(contextlib)
from contextlib import contextmanager
import time
@contextmanager
def timer(label:str):
    start=time.perf_counter()
    try:
        yield
    finally:
        time_taken=time.perf_counter()-start
        print(f"[Timer] {label}: {time_taken:.4f}s")
with timer("Sum of squares"):
    total=sum(i**2 for i in range(10000))
    print(f"Sum:{total}")