terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  access_key                  = "test"
  secret_key                  = "test"
  region                      = "us-east-1"
  s3_use_path_style           = true
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
  endpoints { s3 = "http://localhost:4566" }
}

module "service" {
  source      = "../../modules/service"
  environment = "stage"
}

output "bucket_name" { value = module.service.bucket_name }
