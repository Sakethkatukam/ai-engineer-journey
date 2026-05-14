# ──  Async context manager (used in LLM streaming) ──
import asyncio
class AsyncLLMClient:
    async def __aenter__(self) -> "AsyncLLMClient":
        print("[LLM] Client opened")
        return self

    async def __aexit__(self, *args) -> None:
        print("[LLM] Client closed")

    async def stream_tokens(self, prompt: str):
        tokens = prompt.split()
        for token in tokens:
            await asyncio.sleep(0.5)     # simulate token-by-token streaming
            yield token                  # async generator!

# ──  Async generator (this is how real LLM streaming works) ──
async def demo_streaming():
    async with AsyncLLMClient() as client:
        print("Streaming: ", end="", flush=True)
        async for token in client.stream_tokens("Hello world from LLM"):
            print(token, end=" ", flush=True)
        print()  # newline

    print("\n=== Async Streaming ===")

asyncio.run(demo_streaming())