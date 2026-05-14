import asyncio
import time
async def fetch_data(source:str,delay:float)->str:
    print(f"starting to fetch from {source}")
    await asyncio.sleep(delay)
    print(f"Fetch completed from {source}")
    return f"data from {source}"

async def run_concurrent():
    t=time.perf_counter()
    res1,res2=await asyncio.gather(
        fetch_data("Source A",2),
        fetch_data("Source B",3)
    )
    print(f"Time taken in concurrent: {time.perf_counter()-t:.2f}s")

async def run_sequential():
    t=time.perf_counter()
    r1=await fetch_data("Source A",2)
    r2=await fetch_data("Source B",3)
    print(f"Time taken in sequential: {time.perf_counter()-t:.2f}s")

async def main():
    print("=== Sequential ===")
    await run_sequential()

    print("\n=== Concurrent ===")
    await run_concurrent()

asyncio.run(main())