variable "aws_region" {
  description = "AWS region for the Session 19 mini project."
  type        = string
  default     = "ap-south-1"
}

variable "instance_type" {
  description = "EC2 instance size"
  type        = string
  default     = "t2.micro"
}

variable "bucket_name" {
  description = "Unique name for the S3 bucket"
  type        = string
  default     = "session19-cloud-storage-bucket"
}
