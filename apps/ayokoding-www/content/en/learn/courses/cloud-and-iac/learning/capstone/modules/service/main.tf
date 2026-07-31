locals {
  required_tags = {
    Environment = var.environment
    Owner       = var.owner
    CostCenter  = var.cost_center
    ManagedBy   = "iac"
  }
  bucket_name = "cloud-iac-${var.environment}-service-assets"
}

resource "aws_s3_bucket" "service_assets" {
  bucket = local.bucket_name
  tags   = merge(local.required_tags, { Name = local.bucket_name })
}

data "aws_iam_policy_document" "service_reader" {
  statement {
    effect    = "Allow"
    actions   = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.service_assets.arn}/*"]
  }
}
