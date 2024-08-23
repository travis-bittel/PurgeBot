data "aws_iam_policy_document" "bot_lambda_assume_role_policy" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

# The Discord secret key is stored in SSM and retrieved at runtime
resource "aws_iam_role_policy" "bot_ssm_parameter_access" {
  name = "ssm_parameter_access"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "ssm:GetParameter",
        ]
        Effect   = "Allow"
        Resource = "arn:aws:ssm:us-east-1:975050155823:parameter/purgebot-discord-secret"
      },
    ]
  })
  role = aws_iam_role.bot_lambda_role.id
}

resource "aws_iam_role" "bot_lambda_role" {
  name               = "purge_bot_lamda_role"
  assume_role_policy = data.aws_iam_policy_document.bot_lambda_assume_role_policy.json
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution_role_attachment" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.bot_lambda_role.name
}

resource "aws_lambda_function" "bot_lambda_function" {
    filename         = "../bot_lambda.zip"
    source_code_hash = filebase64sha256("../bot_lambda.zip")
    function_name    = "purgeBot"
    role             = aws_iam_role.bot_lambda_role.arn
    runtime          = "python3.9"
    handler          = "bot.main.lambda_handler"
    timeout          = 300
}

resource "aws_cloudwatch_event_rule" "bot_lambda_event_rule" {
  name                = "purge-bot-lambda-event-rule"
  description         = "Purges users every 24hrs."
  schedule_expression = "rate(24 hours)"
}

resource "aws_cloudwatch_event_target" "bot_lambda_target" {
  arn  = aws_lambda_function.bot_lambda_function.arn
  rule = aws_cloudwatch_event_rule.bot_lambda_event_rule.name
}

resource "aws_lambda_permission" "allow_invocation_from_cloudwatch" {
  statement_id  = "AllowInvocationFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.bot_lambda_function.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.bot_lambda_event_rule.arn
}
