import aiohttp
import asyncio

MAX_TOKENS = 120
CREATIVITY = 20 # 10-100

class OllamaClient():
    def __init__(self, url: str):
        self.url = url

    async def query(self, prompt: str, model: str) -> str:
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": MAX_TOKENS,
                "top_k": CREATIVITY
            }
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, json=payload) as resp:
                data = await resp.json()
                return data["response"]
