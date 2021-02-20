provider "aws" {
  #version = "~> 3.0"
  region                  = var.aws_region
  shared_credentials_file = var.shared_credentials_file
  profile                 = var.aws_profile
}
