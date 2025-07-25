module "llm_lambda" {
  source             = "./modules/lambda"
  function_name      = "qa_lambda"
  artifact_s3_bucket = var.artifact_s3_bucket
  artifact_s3_key    = "lambdas/qa_lambda_deployment_package.zip"
  handler            = "app.lambda_handler"
  runtime            = "python3.10"
  timeout            = 60
  memory_size        = 128

  environment_variables = {
    TEMPLATE_FUNCTION = "sagemaker_faqs_template"
    ARTIFACT_BUCKET   = "mst-artifact-bucket"
  }

  additional_policies = [
    {
      Effect = "Allow"
      Action = [
        "bedrock:InvokeModel"
      ]
      Resource = [
        "arn:aws:bedrock:ap-southeast-2:235494807105:model*"
      ]
    },
    {
      Effect = "Allow"
      Action = [
        "s3:GetObject",
        "s3:ListBucket"
      ]
      Resource = [
        "arn:aws:s3:::mst-artifact-bucket",
        "arn:aws:s3:::mst-artifact-bucket/*"
      ]
    }
  ]
  log_retention_days = 3
}

resource "aws_lambda_permission" "allow_bedrock_invoke" {
  statement_id  = "AllowExecutionFromBedrock"
  action        = "lambda:InvokeFunction"
  function_name = module.llm_lambda.function_name
  principal     = "bedrock.amazonaws.com"
}


#filename      = "code/llm/llm_deployment_package.zip"
#filename      = "code/prompt/prompt_deployment_package.zip"
#filename      = "code/rag/rag_deployment_package.zip"
