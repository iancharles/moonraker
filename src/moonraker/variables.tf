#---------root/variables.tf-----------

# Per VPC
variable "region" {}

variable "ami" {
    type    = map(string)
}


#VAR_PUBLIC

#VAR_PRIVATE


# Per build
variable "availability_zone" {}


variable "iam_instance_profile" {}


variable "instance_type" {}

variable "key_name" {}

variable "os" {}

variable "security_groups" {
    type    = list
}

# per instance
variable "hostname" {}

variable "root_vol_size" {
    default = 64
}