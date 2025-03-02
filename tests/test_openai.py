from types import SimpleNamespace
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

import httpx
import respx
from openai.types.chat import ChatCompletion
from openai.types.chat.chat_completion import Choice
from openai.types.chat.chat_completion_message import ChatCompletionMessage

from mopenai.openai_service import OpenAIService, OpenAIServiceWithInjection

MOCK_ANSWER = "Test answer"


class TestOpenAI(IsolatedAsyncioTestCase):
    def mock_fun(self, request):
        if "https://api.openai.com/v1/chat/completions" in str(request.url):
            response = {
                "choices": [
                    {
                        "message": {
                            "content": MOCK_ANSWER,
                        }
                    }
                ]
            }
            return httpx.Response(200, json=response)
        raise ValueError(f"Unexpected request: {request.url}")

    @patch("tenacity.AsyncRetrying.__call__")
    async def test_openai(self, async_mock_retry):
        async def side_effect(func, obj, *args, **kwargs):
            return await func(obj, *args, **kwargs)

        async_mock_retry.side_effect = side_effect
        async with respx.mock:
            mock_get = respx.get().mock(side_effect=self.mock_fun)
            mock_post = respx.post().mock(side_effect=self.mock_fun)

            openai_service = OpenAIService()
            response = await openai_service.complete("Hello World!")

            self.assertEqual(mock_get.call_count, 0)
            self.assertEqual(mock_post.call_count, 1)
            self.assertEqual(response, MOCK_ANSWER)


from openai.types.chat import ChatCompletion
from openai.types.chat.chat_completion import Choice
from openai.types.chat.chat_completion_message import ChatCompletionMessage


class FakeAsyncOpenAIClient:
    def __init__(self):
        self.call_count = 0

    async def chat_completions_create(self, model, messages):
        self.call_count += 1
        return ChatCompletion(
            id='mock_id',
            created=0,
            model='mock_model',
            object='chat.completion',
            choices=[
                Choice(
                    index=0,
                    finish_reason='stop',
                    message=ChatCompletionMessage(
                        role='assistant',
                        content=MOCK_ANSWER,
                    ),
                ),
            ],
        )


class TestOpenAIWithInjection(IsolatedAsyncioTestCase):
    async def test_openai(self):
        fake_async_openai_client = FakeAsyncOpenAIClient()
        openai_service = OpenAIServiceWithInjection(async_client=fake_async_openai_client)
        response = await openai_service.complete("Hello World!")
        self.assertEqual(fake_async_openai_client.call_count, 1)
        self.assertEqual(response, MOCK_ANSWER)


from types import SimpleNamespace


class FakeAsyncOpenAIClientWithSimpleNameSpace:
    def __init__(self):
        self.call_count = 0

    async def chat_completions_create(self, model, messages):
        self.call_count += 1
        return SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(
                        content=MOCK_ANSWER,
                    )
                )
            ]
        )


class TestOpenAIWithInjectionAndSimpleNamespace(IsolatedAsyncioTestCase):
    async def test_openai(self):
        fake_async_openai_client = FakeAsyncOpenAIClientWithSimpleNameSpace()
        openai_service = OpenAIServiceWithInjection(async_client=fake_async_openai_client)
        response = await openai_service.complete("Hello World!")
        self.assertEqual(fake_async_openai_client.call_count, 1)
        self.assertEqual(response, MOCK_ANSWER)
