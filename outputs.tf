#-----------root/outputs.tf------------#

output "instance_ip_addr" {
  value       = "Private IP: ${aws_instance.moon_node.private_ip}"
  description = "The private IP address of the main server instance."
}
