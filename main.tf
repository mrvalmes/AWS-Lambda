provider "aws" {
  region = "us-east-1"  # Cambia a la región que prefieras
}

resource "aws_s3_bucket" "lambda_bucket" {
  bucket = "lambda-bucket-valmes-paralelo"  # Cambia a un nombre único
}

resource "aws_sqs_queue" "email_queue" {
  name = "email-queue"
}

resource "aws_sns_topic" "email_topic" {
  name = "email-topic"
}

resource "aws_sns_topic_subscription" "email_subscription" {
  topic_arn = aws_sns_topic.email_topic.arn
  protocol  = "sqs"
  endpoint  = aws_sqs_queue.email_queue.arn
}

resource "aws_iam_role" "lambda_role" {
  name = "lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "lambda_policy" {
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "sqs:ReceiveMessage",
          "sqs:DeleteMessage",
          "sqs:GetQueueAttributes",
          "sns:Publish",
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Effect   = "Allow"
        Resource = "*"
      }
    ]
  })
}

resource "aws_lambda_function" "email_lambda" {
  function_name = "email-lambda"
  role          = aws_iam_role.lambda_role.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.8"
  s3_bucket     = aws_s3_bucket.lambda_bucket.bucket
  s3_key        = "lambda_function.zip"
}