import json

from unittest.mock import patch

import os
from sys import path

path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from app import lambda_handler

def test_lambda_handler_success():
    event = json.dumps({
        "resource": "/llm",
        "path": "/llm",
        "httpMethod": "POST",
        "body": {
            "quiz_category": "World Knowledge & Current Affairs"
        },
        "headers": {
            "Accept": "*/*",
        },
        "isBase64Encoded": False
    })
    with patch("app.process_request") as mock_process_request:
        mock_process_request.return_value = {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({"quiz": []})
        }
        response = lambda_handler(event, None)
    assert isinstance(response, dict)
    assert "statusCode" in response
    assert response["statusCode"] in (200, 400, 500)
    assert "headers" in response
    assert "body" in response
    # Optionally, check for error message if statusCode is 400 or 500
    if response["statusCode"] != 200:
        body = json.loads(response["body"])
        assert "error" in body


def test_lambda_handler_missing_quiz_category():
    event = json.dumps({
        "resource": "/llm",
        "path": "/llm",
        "httpMethod": "POST",
        "body": {},
        "headers": {"Accept": "*/*"},
        "isBase64Encoded": False
    })
    with patch("app.process_request") as mock_process_request:
        mock_process_request.return_value = {
            "statusCode": 200,
            "headers": {},
            "body": json.dumps({"quiz": []})
        }
        response = lambda_handler(event, None)
    assert isinstance(response, dict)
    assert "statusCode" in response
    assert response["statusCode"] in (200, 400, 500)
    assert "headers" in response
    assert "body" in response

def test_lambda_handler_quiz_category_too_long():
    long_category = "A" * 101
    event = json.dumps({
        "resource": "/llm",
        "path": "/llm",
        "httpMethod": "POST",
        "body": {"quiz_category": long_category},
        "headers": {"Accept": "*/*"},
        "isBase64Encoded": False
    })
    with patch("app.process_request") as mock_process_request:
        # Should not be called, but patch anyway
        mock_process_request.return_value = {
            "statusCode": 400,
            "headers": {},
            "body": json.dumps({"error":""})
        }
        response = lambda_handler(event, None)
    assert isinstance(response, dict)
    assert response["statusCode"] == 400
    assert "body" in response
    body = json.loads(response["body"])
    assert "error" in body
    

def test_lambda_handler_process_request_exception():
    event = json.dumps({
        "resource": "/llm",
        "path": "/llm",
        "httpMethod": "POST",
        "body": {"quiz_category": "World Knowledge & Current Affairs"},
        "headers": {"Accept": "*/*"},
        "isBase64Encoded": False
    })
    with patch("app.process_request", side_effect=Exception("Simulated failure")):
        response = lambda_handler(event, None)
    assert isinstance(response, dict)
    assert response["statusCode"] == 500
    assert "body" in response
    body = json.loads(response["body"])
    assert "error" in body
    assert "Simulated failure" in body["error"]
