from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

import httpx
import respx

from mopenai.openai_service import OpenAIService

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
