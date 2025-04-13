import os
import unittest
from typing import Any
from unittest import mock
from unittest.mock import AsyncMock, patch, MagicMock, Mock

from melodi.utils import openai
from melodi.utils.openai import OpenAI, AzureOpenAI, AsyncOpenAI, AsyncAzureOpenAI


class TestOpenAIModules(unittest.TestCase):
    @patch("melodi.utils.openai.MelodiClient")
    @patch("melodi.utils.openai.AzureOpenAI", autospec=True)
    def test_azure_openai(self, mock_azure_open_ai, mock_melodi):
        # Create a mock instance of AzureOpenAI
        mock_instance = mock_azure_open_ai.return_value
        mock_instance.chat = MagicMock()
        mock_instance.chat.completions = MagicMock()
        mock_instance.chat.completions.create = MagicMock(
            return_value={"choices": [{"message": {"content": "Azure response"}}]}
        )

        # Ensure that any instantiation of AzureOpenAI returns the mock instance
        mock_azure_open_ai.return_value = mock_instance

        # Initialize client with test parameters (mocked)
        client = AzureOpenAI(
            api_key="test",
            api_version="test",
            azure_endpoint="test",
        )

        # Call the method
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello"}]
        )

        # Assertions
        self.assertIn("choices", response)
        self.assertEqual(response["choices"][0]["message"]["content"], "Azure response")

        # Ensure the mocked method was called correctly
        client.chat.completions.create.assert_called_once_with(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello"}]
        )


if __name__ == "__main__":
    unittest.main()
