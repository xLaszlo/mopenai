import asyncio
import os

import typer
from dotenv import load_dotenv

from mopenai.openai_service import OpenAIServiceWithInjection


async def main(message):
    load_dotenv()
    openai_service = OpenAIServiceWithInjection.get_service(api_key=os.environ["OPENAI_API_KEY"])
    response = await openai_service.complete(message)
    print(f"AI: {response}")


def typer_main(message: str):
    asyncio.run(main(message))


if __name__ == "__main__":
    typer.run(typer_main)
