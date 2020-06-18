#---------root/variables.tf-----------
# Per build
variable "profile" {}

# Per VPC
variable "region" {}

variable "ami" {
    type    = map(string)
}


#VAR_PUBLIC

#VAR_PRIVATE

# Per instance rarely
variable "os" {}

variable "iam_instance_profile" {}

variable "key_name" {}

# Per instance sometimes
variable "availability_zone_BUILD_NO" {}

variable "instance_type" {}

variable "root_vol_size" {
    default = 64
}

variable "security_groups" {
    type    = list
}

# Per instance always
variable "hostname_BUILD_NO" {}






