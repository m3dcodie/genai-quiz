import pytest
from unittest.mock import patch, MagicMock

import os
from sys import path

path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from llm_quiz_handler import LLMQuizHandler

def test_handle_success():
    mock_bedrock = MagicMock()
    mock_bedrock.generate.return_value = {
        'usage': {'inputTokens': 10, 'outputTokens': 20, 'totalTokens': 30},
        'stopReason': 'stop',
        'metrics': {'latencyMs': 100},
        'output': {'message': {'content': [{'text': 'Q1: ...\nCorrect Answer: a.'}]}}
    }
    with patch('handlers.llm_quiz_handler.BedrockClient', return_value=mock_bedrock), \
         patch('handlers.llm_quiz_handler.QuizParser.parse', return_value={"quiz": []}):
        handler = LLMQuizHandler()
        request_body = {'quiz_category': 'Science'}
        context = None
        response = handler.handle(request_body, context)
        assert response['statusCode'] == 200
        assert 'body' in response


def test_handle_quiz_category_too_long():
    handler = LLMQuizHandler()
    request_body = {'quiz_category': 'A' * 101}
    context = None
    with pytest.raises(ValueError) as excinfo:
        handler.handle(request_body, context)
    assert '100 characters or fewer' in str(excinfo.value)


def test_handle_bedrock_exception():
    with patch('handlers.llm_quiz_handler.BedrockClient') as mock_bedrock:
        instance = mock_bedrock.return_value
        instance.generate.side_effect = Exception('Bedrock error')
        handler = LLMQuizHandler()
        request_body = {'quiz_category': 'Science'}
        context = None
        response = handler.handle(request_body, context)
        assert response['statusCode'] == 500
        assert 'error' in response['body']
        assert 'Bedrock error' in response['body']


def test_handle_missing_quiz_category():
    mock_bedrock = MagicMock()
    mock_bedrock.generate.return_value = {
        'usage': {'inputTokens': 10, 'outputTokens': 20, 'totalTokens': 30},
        'stopReason': 'stop',
        'metrics': {'latencyMs': 100},
        'output': {'message': {'content': [{'text': 'Q1: ...\nCorrect Answer: a.'}]}}
    }
    with patch('handlers.llm_quiz_handler.BedrockClient', return_value=mock_bedrock), \
         patch('handlers.llm_quiz_handler.QuizParser.parse', return_value={"quiz": []}):
        handler = LLMQuizHandler()
        request_body = {}  # No quiz_category
        context = None
        response = handler.handle(request_body, context)
        assert response['statusCode'] == 200
        assert 'body' in response
