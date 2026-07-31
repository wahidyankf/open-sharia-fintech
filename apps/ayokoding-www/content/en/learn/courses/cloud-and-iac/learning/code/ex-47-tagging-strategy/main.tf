variable "environment" {
  type    = string
  default = "learning"
}

locals {
  required_tags = { Environment = var.environment, Owner = "learning-team", ManagedBy = "iac", CostCenter = "training" }
}
output "tags" { value = merge(local.required_tags, { Name = "service-assets" }) }
