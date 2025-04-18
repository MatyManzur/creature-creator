import unittest
from unittest.mock import Mock, patch, AsyncMock
from llm_proxy import LLMProxy, cut_after_last_dot, RetryExceededError

class TestLLMProxy(unittest.TestCase):
    def setUp(self):
        # Reset the singleton instance before each test
        LLMProxy._instance = None

    def test_singleton_pattern(self):
        # Test that LLMProxy follows singleton pattern
        instance1 = LLMProxy.get_instance()
        instance2 = LLMProxy.get_instance()
        self.assertIs(instance1, instance2)

    @patch('llm_proxy.OllamaClient')
    def test_initialization(self, mock_ollama):
        # Test proper initialization of LLMProxy
        mock_instance = Mock()
        mock_ollama.get_instance.return_value = mock_instance
        
        proxy = LLMProxy.get_instance()
        self.assertEqual(proxy.cache, {})
        self.assertEqual(proxy.client, mock_instance)

class TestLLMProxyAsync(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        LLMProxy._instance = None
        self.proxy = LLMProxy.get_instance()
        
    @patch('llm_proxy.OllamaClient')
    async def test_query_cached_response(self, mock_ollama):
        # Test querying with cached response
        test_prompt = "test prompt"
        cached_response = "cached response."
        self.proxy.cache[test_prompt] = cached_response
        
        future, was_cached = self.proxy.query(test_prompt, "test-model")
        result = await future
        
        self.assertTrue(was_cached)
        self.assertEqual(result, cached_response)
        mock_ollama.query.assert_not_called()

    @patch('llm_proxy.OllamaClient')
    async def test_query_new_response(self, mock_ollama):
        # Test querying with new response
        test_prompt = "test prompt"
        expected_response = "new response."
        
        mock_instance = Mock()
        mock_instance.query = AsyncMock(return_value=expected_response)
        mock_ollama.get_instance.return_value = mock_instance
        self.proxy.client = mock_instance
        
        future, was_cached = self.proxy.query(test_prompt, "test-model")
        result = await future
        
        self.assertFalse(was_cached)
        self.assertEqual(result, expected_response)
        self.assertEqual(self.proxy.cache[test_prompt], expected_response)
        mock_instance.query.assert_called_once_with(test_prompt, "test-model")

    @patch('llm_proxy.OllamaClient')
    async def test_query_with_retry_exceeded_error(self, mock_ollama):
        # Test handling of RetryExceededError
        test_prompt = "test prompt"
        
        mock_instance = Mock()
        mock_instance.query = AsyncMock(side_effect=RetryExceededError("Retry exceeded"))
        mock_ollama.get_instance.return_value = mock_instance
        self.proxy.client = mock_instance
        
        future, was_cached = self.proxy.query(test_prompt, "test-model")
        
        with self.assertRaises(RetryExceededError):
            await future

if __name__ == '__main__':
    unittest.main()