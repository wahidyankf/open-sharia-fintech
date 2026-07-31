variable "environment" { type = string }
output "name" { value = "service-${var.environment}" }
