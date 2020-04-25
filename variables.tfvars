# build notes
# vpc                 = "vpc-06db524c77128c292"

# account specific
region              = "us-east-2"

ami = {
    "ubuntu16"  = "ami-0564dd36709a7a5b2"
    "ubuntu18"  = "ami-0e8d1a9b450baa691"
    "suse"      = "ami-0eb964f1cd28eb94d"
}

subnets_private = {
    "us-east-2a"    = "subnet-09fad3f8b283a63ef"
    "us-east-2b"    = "subnet-0e0cc0412cd1417c7"
    "us-east-2c"    = "subnet-070bc9c800825dbd2"
}
subnets_public = {
    "us-east-2a"    = "subnet-0ca766e0aba0bb36e"
    "us-east-2b"    = "subnet-0947b6bebe5425ec2"
    "us-east-2c"    = "subnet-08b783efe3bfed00e"   
}
# build specific

availability_zone       = "us-east-2b"

iam_instance_profile    = "EC2-S3-Access"
instance_type           = "t2.micro"
key_name                = "moon-cb-ohio"
os                      = "suse"
security_groups         = ["sg-044dbdc57f842cb04",]

# instance specific
hostname    = "moon-example-2"