#---------root/main.tf-----------

provider "aws" {
    profile = "default"
    region  = "us-east-1"
}

resource "aws_instance" "moon_server" {
    ami                     = var.ami
    iam_instance_profile    = var.iam_instance_profile
    instance_type           = var.instance_type
    key_name                = var.key_name
    security_groups = [
        "sg-d7ad66a0"
    ]
    subnet_id       = var.subnet_id

    tags = {
        Name        = "Moon-Server-01"
    }

    root_block_device {
        encrypted   = true
    }

    ebs_block_device {
        device_name = "/dev/xvdb"
        encrypted   = true
        volume_size = 16
    }
}