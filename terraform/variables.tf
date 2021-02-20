variable "aws_region" {
  type  = string
  default = "us-east-1"
}

variable "shared_credentials_file" {
  type  = string
  default = "~/.aws/credentials"
}

variable "aws_profile" {
  type  = string
  default = "max-private"
}

variable "key_name" {
  type = string
  default = "contrary-hackathon-key"
}

variable "stage" {
  type = string
  default = "dev"
}

variable "app_name" {
  type = string
  default = "moonshooters"
}

variable "namespace" {
  type = string
  default = "contrary"
}

variable "ami" {
  type = string
  #default = "ami-0d915a031cabac0e0"
  default = "ami-047a51fa27710816e"
}

variable "instance_type" {
  type = string
  default = "t2.small"
}
