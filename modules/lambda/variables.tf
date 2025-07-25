variable "function_name" {
  description = "Name of the Lambda function"
  type        = string
}

variable "artifact_s3_bucket" {
  description = "S3 bucket containing the Lambda deployment package"
  type        = string
}

variable "artifact_s3_key" {
  description = "S3 key of the Lambda deployment package"
  type        = string
}

variable "handler" {
  description = "Lambda function handler"
  type        = string
}

variable "runtime" {
  description = "Lambda function runtime"
  type        = string
  default     = "python3.10"
}

variable "timeout" {
  description = "Lambda function timeout in seconds"
  type        = number
  default     = 60
}

variable "memory_size" {
  description = "Lambda function memory size in MB"
  type        = number
  default     = 128
}

variable "environment_variables" {
  description = "Environment variables for the Lambda function"
  type        = map(string)
  default     = {}
}

variable "additional_policies" {
  description = "Additional IAM policies for the Lambda role"
  type        = list(any)
  default     = []
}

variable "log_retention_days" {
  description = "CloudWatch logs retention period in days"
  type        = number
  default     = 14
}
