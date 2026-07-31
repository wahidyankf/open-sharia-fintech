terraform {
  required_providers { aws = { source = "hashicorp/aws", version = "~> 5.0" } }
}

provider "aws" {
  access_key                  = "test"
  secret_key                  = "test"
  region                      = "us-east-1"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
  endpoints { ec2 = "http://localhost:4566" }
}

resource "aws_vpc" "service" { cidr_block = "10.42.0.0/16" }
resource "aws_subnet" "zone_a" {
  vpc_id            = aws_vpc.service.id
  cidr_block        = "10.42.1.0/24"
  availability_zone = "us-east-1a"
}
