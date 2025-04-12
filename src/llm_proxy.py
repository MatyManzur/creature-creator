from llm_client import OllamaClient
from asyncio import Future
import asyncio

def cut_after_last_dot(input_string):
    last_dot_index = input_string.rfind('.')
    
    if last_dot_index != -1:
        return input_string[:last_dot_index + 1]
    else:
        return input_string 

class LLMProxy:
    def __init__(self, client):
        self.client: OllamaClient = client
        self.cache: dict[str, str] = {}

    def query(self, prompt, model) -> Future[str]:
        future = asyncio.get_running_loop().create_future()
        if prompt in self.cache:
            print("Returning cached answer!")
            future.set_result(self.cache[prompt])
        else:
            async def fetch_and_cache():
                print("Fetching answer from LLM...", flush=True)
                result = await self.client.query(prompt, model)
                result = cut_after_last_dot(result)
                self.cache[prompt] = result
                future.set_result(result)
            asyncio.create_task(fetch_and_cache())
        return future