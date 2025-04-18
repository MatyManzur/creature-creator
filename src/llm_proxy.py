from llm_client import OllamaClient
from asyncio import Future
import asyncio
import yaml
from exceptions import RetryExceededError

def cut_after_last_dot(input_string):
    last_dot_index = input_string.rfind('.')
    
    if last_dot_index != -1:
        return input_string[:last_dot_index + 1]
    else:
        return input_string 

CONFIG_FILE = "config.yaml"
with open(CONFIG_FILE, "r") as file:
    config = yaml.safe_load(file)
    OLLAMA_URL = config.get("ollama_server_url", "http://localhost:11434")

class LLMProxy:
    _instance = None

    # Singleton pattern
    @staticmethod
    def get_instance():
        if LLMProxy._instance is None:
            LLMProxy._instance = LLMProxy()
        return LLMProxy._instance

    def __init__(self):
        if hasattr(self, "_initialized"):  
            return
        self.client: OllamaClient = OllamaClient.get_instance(OLLAMA_URL)
        self.cache: dict[str, str] = {}

    def query(self, prompt, model) -> tuple[Future[str], bool]:
        future = asyncio.get_running_loop().create_future()
        was_cached = False
        if prompt in self.cache:
            print("Returning cached answer!")
            future.set_result(self.cache[prompt])
            was_cached = True
        else:
            async def fetch_and_cache():
                print("Fetching answer from LLM...", flush=True)
                try:
                    result = await self.client.query(prompt, model)
                except RetryExceededError as e:
                    future.set_exception(e)
                    return
                result = cut_after_last_dot(result)
                self.cache[prompt] = result
                future.set_result(result)
            asyncio.create_task(fetch_and_cache())
        return future, was_cached