
import asyncio
from contextlib import contextmanager
from pathlib import Path
import shutil
import time
from typing import Dict, List, Optional


def process_documents(docs: List[str], max_length: Optional[int] = None) -> Dict[str, int]:
    dictionary = {}
    for doc in docs:
        words=doc.split()
        if max_length is not None and len(words) > max_length:
            continue
        dictionary[doc]= len(words)
    return dictionary
print(process_documents(["short", "medium length", "a very long document"], max_length=3))

#context manager 

@contextmanager
def temp_directory(name: str):
    path=Path(name)
    path.mkdir()
    try:
        yield path
    finally:
        shutil.rmtree(path)
    
with temp_directory("My folder") as f:
    test_file= f/"test.txt"
    test_file.write_text("Sample text")
    print("File exists?:",test_file.exists())

print("Does that folder exists after context manager?",Path("My folder").exists())

#async/await
async def fake_fetch(url:str)->str:
    await asyncio.sleep(0.5)
    return "Result from "+url

async def fetch_all_concurrent(urls: List[str]) -> List[str]:
    coroutines=[fake_fetch(url) for url in urls]
    results=await asyncio.gather(*coroutines)
    return results

async def fetch_all_sequential(urls:List[str])->List[str]:
    results=[]
    for url in urls:
        result=await fake_fetch(url)
        results.append(result)
    return results

async def main():
    urls=["URL1", "URL2", "URL3"]
    t1=time.perf_counter()
    seq_results=await fetch_all_sequential(urls)
    seq_time=time.perf_counter()-t1

    t2=time.perf_counter()
    con_results=await fetch_all_concurrent(urls)
    con_time=time.perf_counter()-t2

    print(f"Sequential :{seq_time:.2f}s -> {seq_results}")
    print(f"Concurrent :{con_time:.2f}s -> {con_results}")
    print(f"Speedup    :{seq_time/con_time:.1f}x faster")

asyncio.run(main())