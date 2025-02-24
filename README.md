# mopenai

How to mock OpenAI's client

## Relevant technologies:

- asyncio
- typer
- openai
- tenacity
- pytest
- unittest
- httpx
- respx
- uv
- ruff
- dotenv

## Usage

Set `OPENAI_API_KEY` in `.env`

Install `uv` with

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Run with

```
uv run mopenai/main.py "How are you?"
```

Test with

```
pytest
```

