#---------root/variables.tf-----------

variable "ami" {
    default = "ami-0042c75bb13991538"
}

variable "hostname" {

}


variable "iam_instance_profile" {
    default = "EC2-S3-Access"
}


variable "instance_type" {
    default = "t3.micro"
}

variable "key_name" {
    default = "moon-east"
}


variable "subnet_id" {
    default = "subnet-c80e87e7"
}
