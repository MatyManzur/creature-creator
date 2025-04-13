import aiohttp
import asyncio
import yaml
from exceptions import TimeoutExceededError, InvalidResponseError, RetryExceededError, CreatureCreatorError

CONFIG_FILE = "config.yaml"

with open(CONFIG_FILE, "r") as file:
    config = yaml.safe_load(file)
    MAX_TOKENS = config.get("max_tokens", 100)
    CREATIVITY = config.get("creativity", 20)
    TIMEOUT = config.get("timeout", 10)
    RETRIES = config.get("retries", 3)

class OllamaClient():
    _instance = None

    # Singleton pattern
    @staticmethod
    def get_instance(url: str | None = None):
        if OllamaClient._instance is None:
            if url is None:
                raise ValueError("URL must be provided for the first instance.")
            OllamaClient._instance = OllamaClient(url)
        return OllamaClient._instance
    

    def __init__(self, url: str):
        if hasattr(self, "_initialized"):  
            return
        self.url = url
        self.timeout = TIMEOUT
        self.retries = RETRIES

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

        error = None
        for _ in range(self.retries):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(self.url, json=payload) as resp:
                        try:
                            data = await asyncio.wait_for(resp.json(), timeout=self.timeout)
                        except asyncio.TimeoutError:
                            error = "Timeout of {} seconds exceeded".format(self.timeout)
                            raise TimeoutExceededError()
                        if resp.status != 200:
                            error = "Server returned status code {}".format(resp.status)
                            raise InvalidResponseError()
                        return data["response"]
            except CreatureCreatorError as _:
                pass
            except aiohttp.ClientError as e:
                error = "Network error. Check if server is running, or if the URL is correct."
            except BaseException as e:
                error = str(e)
        raise RetryExceededError(error, self.retries)
