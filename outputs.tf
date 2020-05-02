#-----------root/outputs.tf------------#

output "instance_ip_addr" {
  value       = "Public IP: ${aws_instance.moon_node.public_ip}"
  description = "The public IP address of the main server instance."
}
