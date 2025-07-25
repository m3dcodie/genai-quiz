from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate

class PromptBuilder:
    @staticmethod
    def build(template, context):
        prompt_template = ChatPromptTemplate(
            messages=[HumanMessagePromptTemplate.from_template(template)],
            input_variables=["context"],
        )
        return prompt_template.format(context=context)
