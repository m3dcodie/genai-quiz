# Get current AWS region
data "aws_region" "current" {}

# API Gateway REST API
resource "aws_api_gateway_rest_api" "quiz_api" {
  name        = "quiz-api"
  description = "API Gateway for Quiz Lambda function"
}

# API Gateway Resource
resource "aws_api_gateway_resource" "llm_resource" {
  rest_api_id = aws_api_gateway_rest_api.quiz_api.id
  parent_id   = aws_api_gateway_rest_api.quiz_api.root_resource_id
  path_part   = "quiz"
}

# API Gateway POST Method
resource "aws_api_gateway_method" "quiz_post" {
  rest_api_id      = aws_api_gateway_rest_api.quiz_api.id
  resource_id      = aws_api_gateway_resource.llm_resource.id
  http_method      = "POST"
  authorization    = "NONE"
  api_key_required = false # Add this line
}

# API Gateway Integration with Lambda
resource "aws_api_gateway_integration" "lambda_integration" {
  rest_api_id = aws_api_gateway_rest_api.quiz_api.id
  resource_id = aws_api_gateway_resource.llm_resource.id
  http_method = aws_api_gateway_method.quiz_post.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "arn:aws:apigateway:${data.aws_region.current.name}:lambda:path/2015-03-31/functions/${module.llm_lambda.function_arn}/invocations"
}

# Lambda permission to allow API Gateway to invoke the function
resource "aws_lambda_permission" "api_gateway_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = module.llm_lambda.function_name
  principal     = "apigateway.amazonaws.com"

  # Allow invocation from any stage/method in this API Gateway
  source_arn = "${aws_api_gateway_rest_api.quiz_api.execution_arn}/*/*"
}

# API Gateway Deployment
resource "aws_api_gateway_deployment" "llm_deployment" {
  rest_api_id = aws_api_gateway_rest_api.quiz_api.id

  depends_on = [
    aws_api_gateway_integration.lambda_integration
  ]
}

# API Gateway Stage
resource "aws_api_gateway_stage" "llm_stage" {
  deployment_id = aws_api_gateway_deployment.llm_deployment.id
  rest_api_id   = aws_api_gateway_rest_api.quiz_api.id
  stage_name    = "prod"
}

# Enable CORS
resource "aws_api_gateway_method" "options_method" {
  rest_api_id   = aws_api_gateway_rest_api.quiz_api.id
  resource_id   = aws_api_gateway_resource.llm_resource.id
  http_method   = "OPTIONS"
  authorization = "NONE"
}

resource "aws_api_gateway_method_response" "options_200" {
  rest_api_id = aws_api_gateway_rest_api.quiz_api.id
  resource_id = aws_api_gateway_resource.llm_resource.id
  http_method = aws_api_gateway_method.options_method.http_method
  status_code = "200"

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true,
    "method.response.header.Access-Control-Allow-Methods" = true,
    "method.response.header.Access-Control-Allow-Origin"  = true
  }
}

resource "aws_api_gateway_integration" "options_integration" {
  rest_api_id = aws_api_gateway_rest_api.quiz_api.id
  resource_id = aws_api_gateway_resource.llm_resource.id
  http_method = aws_api_gateway_method.options_method.http_method
  type        = "MOCK"

  request_templates = {
    "application/json" = "{\"statusCode\": 200}"
  }
}

resource "aws_api_gateway_integration_response" "options_integration_response" {
  rest_api_id = aws_api_gateway_rest_api.quiz_api.id
  resource_id = aws_api_gateway_resource.llm_resource.id
  http_method = aws_api_gateway_method.options_method.http_method
  status_code = aws_api_gateway_method_response.options_200.status_code

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
    "method.response.header.Access-Control-Allow-Methods" = "'OPTIONS,POST'",
    "method.response.header.Access-Control-Allow-Origin"  = "'*'"
  }
}

resource "aws_api_gateway_usage_plan" "llm_usage_plan" {
  name = "llm-usage-plan"

  api_stages {
    api_id = aws_api_gateway_rest_api.quiz_api.id
    stage  = aws_api_gateway_stage.llm_stage.stage_name
  }

  quota_settings {
    limit  = 200
    period = "MONTH"
  }

  throttle_settings {
    burst_limit = 10
    rate_limit  = 10
  }
}

# POST Method Response
resource "aws_api_gateway_method_response" "post_200" {
  rest_api_id = aws_api_gateway_rest_api.quiz_api.id
  resource_id = aws_api_gateway_resource.llm_resource.id
  http_method = aws_api_gateway_method.quiz_post.http_method
  status_code = "200"

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true,
    "method.response.header.Access-Control-Allow-Methods" = true,
    "method.response.header.Access-Control-Allow-Origin"  = true
  }
}

# POST Integration Response
resource "aws_api_gateway_integration_response" "post_integration_response" {
  rest_api_id = aws_api_gateway_rest_api.quiz_api.id
  resource_id = aws_api_gateway_resource.llm_resource.id
  http_method = aws_api_gateway_method.quiz_post.http_method
  status_code = aws_api_gateway_method_response.post_200.status_code

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
    "method.response.header.Access-Control-Allow-Methods" = "'OPTIONS,POST'",
    "method.response.header.Access-Control-Allow-Origin"  = "'*'"
  }
}

# Output the API Gateway URL
output "api_gateway_url" {
  value = "${aws_api_gateway_stage.llm_stage.invoke_url}/${aws_api_gateway_resource.llm_resource.path_part}"
}
