#---------root/s3.tf-----------


resource "aws_s3_bucket" "VAR_NAME" {
  bucket = "VAR_NAME"
  acl    = "private"
  
  versioning {
    enabled = true
  }

  logging {
    target_bucket = "VAR_LOGS"
    target_prefix = "VAR_NAME/"
  }
}


