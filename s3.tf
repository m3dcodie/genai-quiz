resource "aws_s3_bucket" "s3_static_site" {
  bucket = var.artifact_s3_bucket

  tags = {
    Name = "GenAI QA Static Site"
  }
}

resource "aws_s3_object" "quiz_html" {
  bucket       = var.artifact_s3_bucket
  key          = "multiple-choise/index.html"
  source       = "${path.module}/html/multiple-choise/index.html"
  content_type = "text/html"
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


