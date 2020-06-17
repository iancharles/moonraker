#---------root/ec2.tf-----------

# 10 - RESOURCE - Include in ALL EC2
resource "aws_instance" "moon_node" {
    ami                     = lookup(var.ami, var.os)
    iam_instance_profile    = var.iam_instance_profile
    instance_type           = var.instance_type
    key_name                = var.key_name
    vpc_security_group_ids  = var.security_groups
    subnet_id               = lookup(var.subnets_private, var.availability_zone)

    tags = {
        Name        = var.hostname
    }

    user_data = file("userdata.sh")

    # 23 - Root EBS Volume
    root_block_device {
        volume_size = var.root_vol_size
        encrypted   = true
    }
#   27 - Optional - EBS Block Device
#VAR_EBS
}
