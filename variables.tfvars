ami = {
    "us-east-1" = "ami-0042c75bb13991538"
    "us-east-2" = "ami-0e8d1a9b450baa691"
    "us-west-2" = "ami-04c29899aa9bf924a"
}
hostname        = "moon-example-2"
instance_type   = "t2.micro"
key_name        = "moon-east"
region          = "us-east-1"
security_groups = {
    "us-east-1" = ["sg-f6ff3482",]
    "us-east-2" = ["sg-044dbdc57f842cb04",]
    "us-west-2" = ["sg-96cb9df1",]
}
# subnet_id       = "subnet-1ab2e551"