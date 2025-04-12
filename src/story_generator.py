from body_part import *
from asyncio import Future
from llm_proxy import LLMProxy

PROMPT = "Write only two sentences about a fictional character with {0} head, {1} torso, {2} legs, and {3} wings. Include the character's name and something special about his story."

def generate_story(llm_proxy: LLMProxy, model: str, head: Head, torso: Torso, legs: Legs, wings: Wings) -> Future[str]:
    prompt = PROMPT.format(head.name, torso.name, legs.name, wings.name)
    print("Prompt:", prompt)
    return llm_proxy.query(prompt, model)