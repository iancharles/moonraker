data "aws_ami" "ubuntu16" {
  # executable_users = ["self"]
  most_recent      = true
#  name_regex       = "^myami-\\d{3}"
  owners           = ["self"]

  filter {
    name   = "name"
    values = ["*ubuntu-16*"]
  }
}
data "aws_ami" "ubuntu18" {
  # executable_users = ["self"]
  most_recent      = true
#  name_regex       = "^myami-\\d{3}"
  owners           = ["self"]

  filter {
    name   = "name"
    values = ["*ubuntu-18*"]
  }
}

data "aws_ami" "suse" {
  # executable_users = ["self"]
  most_recent      = true
#  name_regex       = "^myami-\\d{3}"
  owners           = ["self"]

  filter {
    name   = "name"
    values = ["*SUSE*"]
  }
}

