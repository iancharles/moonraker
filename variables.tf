#---------root/variables.tf-----------

variable "region" {
  
}

variable availability_zone {
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

variable "os" {
    default = "ubuntu18"
}

variable "security_groups" {
    type    = list
} 

variable "subnets_private" {
    type    = map(string)
}

variable "subnets_public" {
    type    = map(string)
}