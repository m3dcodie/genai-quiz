import os
from botocore.exceptions import ClientError
from sys import path

path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), './domain/libraries')))
from logging_utils import get_logger

path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), './handlers')))
from llm_quiz_handler import LLMQuizHandler

# Set up logging
logger = get_logger(__name__)

def process_request(request_body, context):
    """Process the incoming request and dispatch to the appropriate handler."""
    handler = LLMQuizHandler()
       
    try:
        return handler.handle(request_body, context)
    except ClientError as err:
        message = err.response['Error']['Message']
        logger.error("A client error occurred: %s", message)
        print(f"A client error occured: {message}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        print(f"An unexpected error occurred: {str(e)}")
    else:
        print(f"Finished processing request for path {path}.")

