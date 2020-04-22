#---------root/variables.tf-----------

variable "region" {
  
}


variable "ami" {
    type    = map(string)
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

variable "security_groups" {
    type    = map(list(string))
} 

variable "subnet_id" {
    default = "subnet-c80e87e7"
}
