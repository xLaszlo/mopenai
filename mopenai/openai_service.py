import os

from openai import AsyncClient
from tenacity import retry, stop_after_attempt, wait_random

SYSTEM_PROMPT = "If you are greeted, greet them back!"


class OpenAIService:
    def __init__(self):
        self.async_client = AsyncClient(api_key=os.environ["OPENAI_API_KEY"])

    @retry(wait=wait_random(min=5, max=10), stop=stop_after_attempt(3))
    async def complete(self, user_prompt):
        res = await self.async_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
        )
        return res.choices[0].message.content
