from typing import Optional
from openai import Completion

MODEL = "gpt-3.5-turbo"

def complete(prompt: str, max_tokens: Optional[int] = None) -> str:
    completion = Completion.create(model=MODEL, prompt=prompt, max_tokens=max_tokens)

    return completion.choices[0].text