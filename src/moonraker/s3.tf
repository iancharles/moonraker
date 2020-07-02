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

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm     = "AES256"
      }
    }
  }
}



