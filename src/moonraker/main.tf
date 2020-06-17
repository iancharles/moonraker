#---------root/main.tf-----------

# PROVIDER - Include in ALL
provider "aws" {
    profile = var.profile
    region  = var.region
    shared_credentials_file = "/home/ian/.aws/credentials"
}
