#---------root/ec2_variables.tf-----------

# variable "ami" {
#     type    = map(string)
# }


#VAR_PUBLIC

#VAR_PRIVATE

# Per instance rarely
variable "os" {}

variable "iam_instance_profile" {}


# Per instance sometimes

variable "instance_type" {}

variable "root_vol_size" {
    default = 64
}

variable "security_groups" {
    type    = list
}

# Per instance always
