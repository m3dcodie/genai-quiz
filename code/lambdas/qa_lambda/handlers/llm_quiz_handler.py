
import json
from domain.libraries.logging_utils import get_logger
from domain.models.faq_template.template import faqs_template
from domain.bedrock_client import BedrockClient
from domain.quiz_parser import QuizParser
from domain.prompt_builder import PromptBuilder
from domain.model_config import NovaLiteConfig

logger = get_logger(__name__)

class LLMQuizHandler:
    def handle(self, request_body: dict, context) -> dict:
        """
        Process the incoming request and generate a quiz.

        Args:
            request_body (dict): The request payload.
            context: Lambda context object.

        Returns:
            dict: API Gateway-compatible response.
        """
        content = "Generate the quiz"
        quiz_category, jquiz_data = None, None
        quiz_category = request_body.get('quiz_category')
        if quiz_category and len(quiz_category) > 100:
            raise ValueError('quiz_category must be 100 characters or fewer.')
        template = faqs_template(quiz_category)
        
        prompt = PromptBuilder.build(template, content)
        messages = []
        model_id = "apac.amazon.nova-lite-v1:0"
        model_config = NovaLiteConfig(temperature=0.5)        
        inference_config = model_config.to_inference_config()
        system_prompts = [{"text": prompt}]
        message_1 = {
            "role": "user",
            "content": [{"text": content}]
        }
        messages.append(message_1)
        try:

            bedrock = BedrockClient(model_id)
            logger.info("Generating message with model %s", model_id)
            response = bedrock.generate(system_prompts, messages, inference_config)        
            
            token_usage = response['usage']
            logger.info("Input tokens: %s", token_usage['inputTokens'])
            logger.info("Output tokens: %s", token_usage['outputTokens'])
            logger.info("Total tokens: %s", token_usage['totalTokens'])
            logger.info("Stop reason: %s", response['stopReason'])
            logger.info("metrics latencyMs: %s Ms", response['metrics']['latencyMs'])
            output_message = response['output']['message']
            messages.append(output_message)
            result = output_message["content"][0]['text']
            quiz = QuizParser.parse(result)
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST'
                },
                'body': json.dumps(quiz)
            }
        except Exception as e:
            logger.error("Quiz generation failed: %s", str(e), exc_info=True)
            return {
                'statusCode': 500,
                'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST'
                },
                'body': json.dumps({'error': str(e)})
            }
    # Convert questions to string with each question and options on a new line
    def questions_to_string(self, questions):
        lines = []
        for idx, q in enumerate(questions, 1):
            lines.append(f"Q{idx}: {q['question']}")
            for opt_idx, opt in zip("abcd", q['options']):
                lines.append(f"  {opt_idx}. {opt}")
            lines.append(f"Correct Answer: {q['answer']}\n")
        return "\n".join(lines)

