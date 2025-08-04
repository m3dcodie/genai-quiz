# Project Overview

GenAI Quiz is a serverless application that uses Generative AI to generate FAQs and quizzes for any topic provided by the user. It helps users test and expand their knowledge interactively on their favorite subjects.

## Folder Structure

.
├── code
│   ├── domain
│   │   ├── libraries
│   │   └── models
│   │   └── faq_template
│   ├── lambdas
│   │   └── qa_lambda
│   │   ├── domain -> ../../domain
│   │   ├── handlers
│   │   └── tests
│   ├── lib
│   └── tests
├── html
│   └── multiple-choise
└── modules
└── lambda

- Root folder contains, terraform files for infrastructure, ignore files and code folder.
- `/code`: Contains the source code for the backend, including lambdas, domain, libraries etc.
- `/code/modules`: Contains terraform modules.
- `/code/domain`: Contains business logic specific to this quiz applicaiton.
- `/code/lambdas`: Contains lambda code.
- `/code/lambdas/test`: Contains unit tests
- `/html`: Contains frontend files, uploaded to S3. Cloudfront will use to show to endusers.

## Libraries and Frameworks

- Terraform for infrastrucutre as a code.
- Python3.10 or greater for backend
- AWS boto3 libraries to intreact with AWS service, like Bedrock.
- langchain for prompts

## Coding Standards

- Use PEP 8 style for coding.
- Indentation, use tabs, not spaces.
- Comments, Use JSDoc style comments for functions, interfaces, enums, and classes

## Unit test generation

- Use the AAA pattern for test cases. Arrage, Act, Assert
- Use success cases, failure and edge cases.

## Git

- Git commit messsage: medium detail with the file changes and the reason for the change. Add emojis as much as you can.
