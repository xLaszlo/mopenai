import asyncio

import typer
from dotenv import load_dotenv

from mopenai.openai_service import OpenAIService


async def main(message):
    load_dotenv()
    openai_service = OpenAIService()
    response = await openai_service.complete(message)
    print(f"AI: {response}")


def typer_main(message: str):
    asyncio.run(main(message))


if __name__ == "__main__":
    typer.run(typer_main)
