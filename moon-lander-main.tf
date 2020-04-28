#### BEGIN DEFAULT TEMPLATE
#---------moon/main.tf-----------

# PROVIDER - Include in ALL
provider "aws" {
    profile = "default"
    region  = var.region
}


# 11 - RESOURCE - Include in ALL EC2
resource "aws_instance" "moon_node" {
    ami                     = lookup(var.ami, var.os)
    iam_instance_profile    = var.iam_instance_profile
    instance_type           = var.instance_type
    key_name                = var.key_name
    vpc_security_group_ids  = var.security_groups
    subnet_id               = lookup(var.subnets_public, var.availability_zone)

    tags = {
        Name        = var.hostname
    }

    # 24 - Root EBS Volume
    root_block_device {
        encrypted   = true
    }
    #### END DEFAULT TEMPLATE

    #### BEGIN MOONRAKER-GENERATED VALUES


}
