resource "aws_s3_bucket" "s3_static_site" {
  bucket = "genai-qa-static-site"
  acl    = "private"

  tags = {
    Name        = "GenAI QA Static Site"
    Environment = "dev"
  }
}
resource "aws_s3_bucket_policy" "cloudfront_access" {
  bucket = aws_s3_bucket.s3_static_site.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowCloudFrontServicePrincipalReadOnly"
        Effect = "Allow"
        Principal = {
          Service = "cloudfront.amazonaws.com"
        }
        Action = [
          "s3:GetObject"
        ]
        Resource = "${aws_s3_bucket.s3_static_site.arn}/*"
        Condition = {
          StringEquals = {
            "AWS:SourceArn" = "arn:aws:cloudfront::${data.aws_caller_identity.current.account_id}:distribution/*"
          }
        }
      }
    ]
  })
}

data "aws_caller_identity" "current" {}
