#terraform {
  #backend "s3" {
    #bucket = "contrary-hackathon-21"
    #key    = "terraform.tfstate"
    #region = "us-east-1"
  #}
#}

resource "aws_s3_bucket" "state" {
  bucket = "contrary-hackathon-21"
  acl = "private"

  tags = {
    stage = var.stage
    namespace = var.namespace
    app_name = var.app_name
  }
}

resource "tls_private_key" "key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "aws_key_pair" "generated_key" {
  key_name   = "${var.namespace}-${var.app_name}-${var.stage}-key"
  public_key = tls_private_key.key.public_key_openssh
}

resource "aws_security_group" "tcp_whitelist" {
  name        = "${var.namespace}-${var.app_name}-${var.stage}-allow-tcp"
  description = "Allow SSH inbound traffic"

  ingress {
    description = "SSH port IP whitelist"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Port 80 IP whitelist"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Port 443 IP whitelist"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    name = "allow_http"
    stage = var.stage
    app = var.app_name
  }
}

#resource "aws_eip" "elastic_ip" {
  #instance = aws_instance.ec2.id
#}

resource "aws_instance" "ec2" {
  ami           = var.ami
  instance_type = var.instance_type
  key_name = aws_key_pair.generated_key.key_name

  connection {
      type     = "ssh"
      user     = "ec2-user"
      host = self.public_ip
      private_key = tls_private_key.key.private_key_pem
      timeout = "30"
  }

  provisioner "file" {
    source      = "setup.sh"
    destination = "/tmp/setup.sh"
  }

  provisioner "remote-exec" {
    inline = [
      "chmod +x /tmp/setup.sh",
      "sudo /tmp/setup.sh",
    ]
  }

  security_groups  = [
    aws_security_group.tcp_whitelist.name
  ]

  tags = {
    stage = var.stage
    app = var.app_name
  }
}
