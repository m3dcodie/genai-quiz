import boto3
from domain.models.coverse_api import generate_conversation

class BedrockClient:
    def __init__(self, model_id):
        self.model_id = model_id
        self.client = boto3.client(service_name='bedrock-runtime')

    def generate(self, system_prompts, messages, inference_config):
        return generate_conversation(
            self.client, self.model_id, system_prompts, messages, inference_config
        )
