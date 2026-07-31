terraform { required_version = ">= 1.5.0" }
variable "bucket_name" {
  type    = string
  default = "cloud-iac-hcl-example"
}

locals {
  lifecycle_enabled = true
}
