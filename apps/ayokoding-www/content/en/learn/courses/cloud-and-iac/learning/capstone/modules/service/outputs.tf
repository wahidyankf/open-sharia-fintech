output "bucket_name" {
  description = "The non-secret bucket name created for the environment."
  value       = aws_s3_bucket.service_assets.bucket
}

output "reader_policy_json" {
  description = "A least-privilege document that permits object reads in this bucket only."
  value       = data.aws_iam_policy_document.service_reader.json
}
