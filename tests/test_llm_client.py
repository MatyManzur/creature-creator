import unittest
from unittest.mock import Mock, patch, AsyncMock
import asyncio
import aiohttp
from llm_client import OllamaClient, TimeoutExceededError, InvalidResponseError, RetryExceededError, CreatureCreatorError

class TestOllamaClient(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Reset the singleton instance before each test
        OllamaClient._instance = None
        self.test_url = "http://test.url"
        self.test_prompt = "test prompt"
        self.test_model = "test-model"
        
    def test_singleton_pattern(self):
        # Test singleton pattern implementation
        client1 = OllamaClient.get_instance(self.test_url)
        client2 = OllamaClient.get_instance()
        self.assertIs(client1, client2)


    @patch('aiohttp.ClientSession')
    async def test_successful_query(self, mock_session):
        # Test successful query
        expected_response = "test response"
        mock_response = Mock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={"response": expected_response})
        
        mock_context = AsyncMock()
        mock_context.__aenter__.return_value = mock_response
        
        mock_session_instance = Mock()
        mock_session_instance.post = Mock(return_value=mock_context)
        mock_session().__aenter__.return_value = mock_session_instance

        client = OllamaClient.get_instance(self.test_url)
        response = await client.query(self.test_prompt, self.test_model)
        
        self.assertEqual(response, expected_response)
        
        # Verify the correct payload was sent
        expected_payload = {
            "model": self.test_model,
            "prompt": self.test_prompt,
            "stream": False,
            "options": {
                "num_predict": 120,  # Default from config
                "top_k": 20         # Default from config
            }
        }
        mock_session_instance.post.assert_called_once_with(self.test_url, json=expected_payload)

    @patch('aiohttp.ClientSession')
    async def test_timeout_error(self, mock_session):
        # Test timeout error handling
        mock_response = Mock()
        mock_response.json = AsyncMock(side_effect=asyncio.TimeoutError())
        
        mock_context = AsyncMock()
        mock_context.__aenter__.return_value = mock_response
        
        mock_session_instance = Mock()
        mock_session_instance.post = Mock(return_value=mock_context)
        mock_session().__aenter__.return_value = mock_session_instance

        client = OllamaClient.get_instance(self.test_url)
        with self.assertRaises(RetryExceededError):
            await client.query(self.test_prompt, self.test_model)

    @patch('aiohttp.ClientSession')
    async def test_invalid_response(self, mock_session):
        # Test invalid response handling
        mock_response = Mock()
        mock_response.status = 500
        mock_response.json = AsyncMock(return_value={})
        
        mock_context = AsyncMock()
        mock_context.__aenter__.return_value = mock_response
        
        mock_session_instance = Mock()
        mock_session_instance.post = Mock(return_value=mock_context)
        mock_session().__aenter__.return_value = mock_session_instance

        client = OllamaClient.get_instance(self.test_url)
        with self.assertRaises(RetryExceededError):
            await client.query(self.test_prompt, self.test_model)

    @patch('aiohttp.ClientSession')
    async def test_network_error(self, mock_session):
        # Test network error handling
        mock_session_instance = Mock()
        mock_session_instance.post = Mock(side_effect=aiohttp.ClientError())
        mock_session().__aenter__.return_value = mock_session_instance

        client = OllamaClient.get_instance(self.test_url)
        with self.assertRaises(RetryExceededError):
            await client.query(self.test_prompt, self.test_model)

    @patch('aiohttp.ClientSession')
    async def test_creature_creator_error(self, mock_session):
        # Test CreatureCreatorError handling
        mock_session_instance = Mock()
        mock_session_instance.post = Mock(side_effect=CreatureCreatorError("Error!"))
        mock_session().__aenter__.return_value = mock_session_instance

        client = OllamaClient.get_instance(self.test_url)
        with self.assertRaises(RetryExceededError):
            await client.query(self.test_prompt, self.test_model)

    @patch('aiohttp.ClientSession')
    async def test_retry_mechanism(self, mock_session):
        # Test retry mechanism
        mock_response = Mock()
        mock_response.status = 500
        mock_response.json = AsyncMock(return_value={})
        
        mock_context = AsyncMock()
        mock_context.__aenter__.return_value = mock_response
        
        mock_session_instance = Mock()
        mock_session_instance.post = Mock(return_value=mock_context)
        mock_session().__aenter__.return_value = mock_session_instance

        client = OllamaClient.get_instance(self.test_url)
        with self.assertRaises(RetryExceededError):
            await client.query(self.test_prompt, self.test_model)
        
        # Verify that the retry mechanism attempted the correct number of times
        self.assertEqual(mock_session_instance.post.call_count, client.retries)

if __name__ == '__main__':
    unittest.main()