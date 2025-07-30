import pytest
from unittest.mock import patch, MagicMock

import os
from sys import path

path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from process_request import process_request

def test_process_request_success():
    mock_handler = MagicMock()
    mock_handler.handle.return_value = {"statusCode": 200, "body": "ok"}
    with patch("process_request.LLMQuizHandler", return_value=mock_handler):
        event = {"quiz_category": "Science"}
        context = None
        response = process_request(event, context)
        assert response["statusCode"] == 200
        assert response["body"] == "ok"


def test_process_request_client_error():
    mock_handler = MagicMock()
    from botocore.exceptions import ClientError
    error_response = {"Error": {"Message": "S3 error"}}
    client_error = ClientError(error_response, "GetObject")
    mock_handler.handle.side_effect = client_error
    with patch("process_request.LLMQuizHandler", return_value=mock_handler):
        event = {"quiz_category": "Science"}
        context = None
        response = process_request(event, context)
        assert response["statusCode"] == 400
        assert "Client error" in response["body"]


def test_process_request_unexpected_exception():
    mock_handler = MagicMock()
    mock_handler.handle.side_effect = Exception("Something went wrong")
    with patch("process_request.LLMQuizHandler", return_value=mock_handler):
        event = {"quiz_category": "Science"}
        context = None
        response = process_request(event, context)
        assert response["statusCode"] == 500
        assert "Internal server error" in response["body"]


def test_process_request_edge_empty_event():
    mock_handler = MagicMock()
    mock_handler.handle.return_value = {"statusCode": 200, "body": "ok"}
    with patch("process_request.LLMQuizHandler", return_value=mock_handler):
        event = {}
        context = None
        response = process_request(event, context)
        assert response["statusCode"] == 200
        assert response["body"] == "ok"
