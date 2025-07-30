import json
import traceback
from sys import path
import os
from process_request import process_request 

path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), './domain/libraries')))
from logging_utils import get_logger

# Set up logging
logger = get_logger(__name__)

def lambda_handler(event: dict, context) -> dict:
    """
    AWS Lambda handler for processing quiz requests.
    Args:
        event (dict): The event payload from API Gateway.
        context: Lambda context object.
    Returns:
        dict: API Gateway-compatible response.
    """
    logger.info('Event: %s', json.dumps(event))
    try:
        event = json.loads(event)
        response = process_request(event['body'], context)
        # Ensure CORS headers are present in all responses
        
        if 'headers' not in response:
            response['headers'] = {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            }
        return response
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        logger.error(traceback.format_exc())
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            'body': json.dumps({'error': str(e)})
        }
    

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
    "isBase64Encoded": False}
)

#response = lambda_handler(event, None)
#print("Response:")
#print(response)
