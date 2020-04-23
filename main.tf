#---------root/main.tf-----------

# PROVIDER - Include in ALL
provider "aws" {
    profile = "default"
    region  = var.region
}


# RESOURCE - Include in ALL EC2
resource "aws_instance" "moon_server" {
    ami                     = lookup(var.ami, var.os)
    iam_instance_profile    = var.iam_instance_profile
    instance_type           = var.instance_type
    key_name                = var.key_name
    vpc_security_group_ids  = var.security_groups
    subnet_id               = lookup(var.subnets_public, var.availability_zone)

    tags = {
        Name        = var.hostname
    }

    root_block_device {
        encrypted   = true
    }
#   Optional
    ebs_block_device {
        device_name = "/dev/xvdb"
        encrypted   = true
        volume_size = 16
    }
}

# SUB-RESOURCE - Include in EC2 with Public Subnet/EIP
resource "aws_eip" "public_ip" {
    vpc         = true
    instance    = aws_instance.moon_server.id
}

