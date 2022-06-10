terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  # region = var.region_name
  # access_key = var.aws_access_key
  # secret_key = var.aws_secret_key
}