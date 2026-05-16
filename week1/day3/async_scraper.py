import asyncio
import aiohttp
from typing import List,Dict

async def fetch_page(session:aiohttp.ClientSession,url:str)->Dict[str, str]:
    async with session.get(url) as response:
        text=await response.text()
        return {"url":url,
                "status":str(response.status),
                "chars":str(len(text))
                }

async def scrape_all(urls:List[str])->List[Dict[str,str]]:
    async with aiohttp.ClientSession() as session:
        coroutines=[fetch_page(session,url) for url in urls]
        return list(await asyncio.gather(*coroutines))

async def main() -> None:
    urls = [
        "https://httpbin.org/get",     # free test endpoint
        "https://httpbin.org/ip",
        "https://httpbin.org/headers",
    ]
    results= await scrape_all(urls)
    for r in results:
        print(f"{r['url']} -> status {r['status']}, {r['chars']} chars")

asyncio.run(main())