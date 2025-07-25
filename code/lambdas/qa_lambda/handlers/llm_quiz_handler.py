import os
from sys import path
import json
import boto3
import tempfile

path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../libraries')))
from logging_utils import get_logger
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate

path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../domain/models/faq_template')))
from template import sagemaker_faqs_template, bedrock_faqs_template, bedrock_rag_faqs_template

path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../domain')))
from bedrock_client import BedrockClient
from quiz_parser import QuizParser
from prompt_builder import PromptBuilder
from model_config import NovaLiteConfig, TitanConfig, BaseModelConfig

logger = get_logger(__name__)

class LLMQuizHandler:
    def handle(self, request_body, context):
        content = "Generate the quiz"
        quiz_cat_id, jquiz_data = None, None
        # Get id from queryStringParameters if present
        if 'queryStringParameters' in request_body and request_body['queryStringParameters']:
            quiz_cat_id = request_body['queryStringParameters'].get('id')
       
        s3_client = boto3.client("s3")
        bucket = os.environ.get("ARTIFACT_BUCKET")  # Replace with your bucket name
        key = "quiz/quiz.json"   # Replace with your S3 key
              
        response = s3_client.get_object(Bucket=bucket, Key=key)
        jquiz_data = json.load(response['Body'])

        # Find quiz by id
        quiz_result = next((item for item in jquiz_data if item['id'] == quiz_cat_id), None)
               
        template = f"""
        Below is the {quiz_result['category']} FAQ:

        {LLMQuizHandler.questions_to_string(self, quiz_result['questions'])}
    
        Quiz:

        Q1: <Question 1 text>
        a. <Option 1 for Question 1>
        b. <Option 2 for Question 1>
        c. <Option 3 for Question 1>
        d. <Option 4 for Question 1>

        Correct Answer: <Correct option letter for Question 1>.

        Q2: <Question 2 text>
        a. <Option 1 for Question 2>
        b. <Option 2 for Question 2>
        c. <Option 3 for Question 2>
        d. <Option 4 for Question 2>

        Correct Answer: <Correct option letter for Question 2>.

        ... (Repeat the same format for all questions)
    
        Strickly follow the format above.
        """
        
        prompt = PromptBuilder.build(template, content)
       
        model_id = "apac.amazon.nova-lite-v1:0"
        if model_id.startswith("apac.amazon.nova-lite"):
            model_config = NovaLiteConfig(temperature=0.5)
        elif model_id.startswith("amazon.titan"):
            model_config = TitanConfig(temperature=0.5, top_p=0.95)
        else:
            model_config = BaseModelConfig(temperature=0.5)
        inference_config = model_config.to_inference_config()
        system_prompts = [{"text": prompt}]
        message_1 = {
            "role": "user",
            "content": [{"text": "Generate the quiz."}]
        }
        messages = []
        bedrock = BedrockClient(model_id)
        logger.info("Generating message with model %s", model_id)
        messages.append(message_1)
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
            'body': json.dumps({'quiz': quiz})
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

