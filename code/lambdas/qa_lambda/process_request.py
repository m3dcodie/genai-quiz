
from botocore.exceptions import ClientError
from domain.libraries.logging_utils import get_logger
from handlers.llm_quiz_handler import LLMQuizHandler

# Set up logging
logger = get_logger(__name__)

def process_request(event: dict, context) -> dict:
    """
    Process the incoming request and dispatch to the appropriate handler.

    Args:
        event (dict): The request payload.
        context: Lambda context object.

    Returns:
        dict: The response from the handler or an error response.
    """
    handler = LLMQuizHandler()
    try:
        return handler.handle(event, context)
    except ClientError as err:
        message = err.response['Error']['Message']
        logger.error("A client error occurred: %s", message)
        return {
            'statusCode': 400,
            'body': f'Client error: {message}'
        }
    except Exception as e:
        logger.error("An unexpected error occurred: %s", str(e), exc_info=True)
        return {
            'statusCode': 500,
            'body': f'Internal server error: {str(e)}'
        }

