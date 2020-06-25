#---------root/ec2.tf-----------

# 10 - RESOURCE - Include in ALL EC2
resource "aws_instance" "ec2-BUILD_NO" {
    ami                     = data.aws_ami.VAR_OS.id
    iam_instance_profile    = var.iam_instance_profile
    instance_type           = var.instance_type
    key_name                = var.key_name_BUILD_NO
    vpc_security_group_ids  = var.security_groups
    subnet_id               = lookup(var.subnets_private, var.availability_zone_BUILD_NO)

    tags = {
        Name        = var.hostname_BUILD_NO
    }

    user_data = file("user_data_BUILD_NO.sh")

    # 23 - Root EBS Volume
    root_block_device {
        volume_size = var.root_vol_size
        encrypted   = true
    }
#   27 - Optional - EBS Block Device
#VAR_EBS
}
