#---------root/variables.tf-----------

# Per VPC
variable "region" {}

variable "ami" {
    type    = map(string)
}


variable "subnets_private" {
    type    = map(string)
}

variable "subnets_public" {
    type    = map(string)
}


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