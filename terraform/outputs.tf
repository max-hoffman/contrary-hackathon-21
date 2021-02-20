output "ec2-url" {
  value =  aws_instance.ec2.public_dns
}

output "public-key" {
  value = tls_private_key.key.public_key_pem
}

output "private-key" {
  value = tls_private_key.key.private_key_pem
}
