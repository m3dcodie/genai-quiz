variable "artifact_s3_bucket" {
  description = "S3 Bucket for lambdas and others"
  type        = string
  default     = "mst-artifact-bucket"
}
