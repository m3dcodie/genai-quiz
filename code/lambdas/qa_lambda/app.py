# Import necessary libraries
import json
import traceback
from sys import path
import os
from process_request import process_request 

path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), './domain/libraries')))
from logging_utils import get_logger

# Set up logging
logger = get_logger(__name__)

# Define Lambda function
def lambda_handler(event_body, context):
    # Log the incoming event in JSON format
    logger.info('Event: %s', json.dumps(event_body))

    try:
        if isinstance(event_body, str):
            request_body = json.loads(event_body)
        elif isinstance(event_body, dict):
            request_body = event_body
        else:
            raise ValueError(f"Unsupported event_body type: {type(event_body)}")
        response = process_request(request_body, context)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        stack_trace = traceback.format_exc()
        print(f"stack trace: {stack_trace}")
        print(f"error: {str(e)}")
        response = str(e)
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            'body': json.dumps({'error': response})
        }
    
    return response
    

event = json.dumps({
    "resource": "/llm",
    "path": "/llm",    
    "httpMethod": "GET",
    "queryStringParameters": {
        "quiz_category": "World Knowledge & Current Affairs"
    },
    "headers": {
        "Accept": "*/*",
        
    },        
    "isBase64Encoded": False}
)

"""
event = {
    "body": json.dumps({
        "content": "The topic is SageMaker Low-code ML FAQ consisting of 4 questions. Each question should have 4 possible answers.",
        
        "temperature": 0,
        "max_tokens": 200
    })
}
event = {
    "messageVersion": "1.0",
    "parameters": [
        {
            "name": "CustomerName",
            "type": "string",
            "value": "John Doe"
        }
    ],
    "inputText": "John Doe",
    "sessionAttributes": {},
    "promptSessionAttributes": {},
    "sessionId": "235494807105547",
    "agent": {
        "name": "cs-bot-agent",
        "version": "DRAFT",
        "id": "TP5WBYACGS",
        "alias": "TSTALIASID"
    },
    "actionGroup": "cs_bot_action_group",
    "httpMethod": "GET",
    "apiPath": "/customer/{CustomerName}"
}
"""
response = lambda_handler(event, None)
print("Response:")
print(response)
"""
event = json.dumps({
    "path": "/tool_agent/place_order",
    "parameters": [
        {"name": "ShoeID", "value": "123"},
        {"name": "CustomerID", "value": "456"}
    ]
})

"path": "/tool_agent/customer",
    "parameters": [
        {"name": "CustomerName", "value": "John Doe"}
    ],
"""