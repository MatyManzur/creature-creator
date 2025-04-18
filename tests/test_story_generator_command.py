import unittest
from unittest.mock import Mock, patch
from asyncio import Future
import asyncio
from command import GenerateStoryCommand
from exceptions import RetryExceededError
from creator import Creator, BodyPartType
from llm_proxy import LLMProxy

class TestGenerateStoryCommand(unittest.TestCase):
    def setUp(self):
        # Reset singleton instances
        Creator._instance = None
        LLMProxy._instance = None
        
        # Create mock creator and LLMProxy
        self.mock_creator = Mock()
        self.mock_llm_proxy = Mock()
        
        # Setup test data
        self.test_model = "test-model"
        self.test_head = "dragon head"
        self.test_torso = "lion torso"
        self.test_legs = "eagle legs"
        self.test_wings = "butterfly wings"
        
        # Create command instance
        self.command = GenerateStoryCommand(self.test_model)

        # Setup event loop
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        self.loop.close()

    @patch('command.Creator')
    @patch('command.LLMProxy')
    @patch('command.generate_story')
    def test_successful_story_generation(self, mock_generate_story, mock_llm_proxy, mock_creator):
        # Setup mocks
        mock_creator.get_instance.return_value = self.mock_creator
        mock_llm_proxy.get_instance.return_value = self.mock_llm_proxy
        
        # Setup mock body parts
        self.mock_creator.get_selected_body_part.side_effect = [
            self.test_head,
            self.test_torso,
            self.test_legs,
            self.test_wings
        ]
        
        # Create future with success result
        future = Future(loop=self.loop)
        future.set_result("Generated story")
        mock_generate_story.return_value = (future, False)
        
        # Execute command
        self.command.execute()
        
        # Run the event loop to process callbacks
        self.loop.run_until_complete(asyncio.sleep(0))
        
        # Verify calls
        self.mock_creator.set_story.assert_any_call(story="Loading...")
        self.mock_creator.set_story.assert_called_with(
            story="Generated story",
            was_cached=False
        )

    @patch('command.Creator')
    @patch('command.LLMProxy')
    @patch('command.generate_story')
    def test_cached_story_generation(self, mock_generate_story, mock_llm_proxy, mock_creator):
        # Setup mocks
        mock_creator.get_instance.return_value = self.mock_creator
        mock_llm_proxy.get_instance.return_value = self.mock_llm_proxy
        
        # Create future with cached result
        future = Future(loop=self.loop)
        future.set_result("Cached story")
        mock_generate_story.return_value = (future, True)
        
        # Execute command
        self.command.execute()
        
        # Run the event loop to process callbacks
        self.loop.run_until_complete(asyncio.sleep(0))
        
        # Verify calls
        self.mock_creator.set_story.assert_called_with(
            story="Cached story",
            was_cached=True
        )

    @patch('command.Creator')
    @patch('command.LLMProxy')
    @patch('command.generate_story')
    def test_retry_exceeded_error(self, mock_generate_story, mock_llm_proxy, mock_creator):
        # Setup mocks
        mock_creator.get_instance.return_value = self.mock_creator
        mock_llm_proxy.get_instance.return_value = self.mock_llm_proxy
        
        # Create future with error
        future = Future(loop=self.loop)
        error = RetryExceededError("Connection failed", 3)
        future.set_exception(error)
        mock_generate_story.return_value = (future, False)
        
        # Execute command
        self.command.execute()
        
        # Run the event loop to process callbacks
        self.loop.run_until_complete(asyncio.sleep(0))
        
        # Verify calls
        self.mock_creator.set_story.assert_any_call(story="Loading...")
        self.assertRaises(RetryExceededError)
            

    @patch('command.Creator')
    @patch('command.LLMProxy')
    @patch('command.generate_story')
    def test_general_exception_handling(self, mock_generate_story, mock_llm_proxy, mock_creator):
        # Setup mocks
        mock_creator.get_instance.return_value = self.mock_creator
        mock_llm_proxy.get_instance.return_value = self.mock_llm_proxy
        
        # Create future with general exception
        future = Future(loop=self.loop)
        future.set_exception(Exception("Unexpected error"))
        mock_generate_story.return_value = (future, False)
        
        # Execute command
        self.command.execute()
        
        # Run the event loop to process callbacks
        self.loop.run_until_complete(asyncio.sleep(0))
        
        # Verify calls
        self.mock_creator.set_story.assert_any_call(story="Loading...")

if __name__ == '__main__':
    unittest.main()