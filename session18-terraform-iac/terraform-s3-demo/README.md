# Terraform S3 Demo Project

## Project Overview

This project provisions an AWS S3 bucket using Terraform Infrastructure as Code (IaC) with parameterization, structured provider configuration, and explicit outputs.

---

## Directory Structure

```text
terraform-s3-demo/
├── main.tf            # S3 bucket resource definition
├── variables.tf       # Input variables (aws_region, bucket_name)
├── outputs.tf         # Resource outputs (bucket_name, arn, region)
├── provider.tf        # AWS provider and Terraform version constraints
├── terraform.tfvars   # Variable definitions
└── README.md          # Complete lifecycle documentation
```

---

## Terraform Workflow & Command Execution

### 1. `terraform init`
Initializes the working directory containing Terraform configuration files. Downloads and installs the AWS provider plugin.

```bash
terraform init
```

*Terminal Output:*
```text
Initializing the backend...
Initializing provider plugins...
- Finding hashicorp/aws versions matching "~> 5.0"...
- Installing hashicorp/aws v5.100.0...
- Installed hashicorp/aws v5.100.0 (signed by HashiCorp)

Terraform has been successfully initialized!
```

---

### 2. `terraform fmt`
Rewrites Terraform configuration files to a canonical format and style according to HCL conventions.

```bash
terraform fmt
```

*Output:*
Formats all `.tf` files in place for consistent spacing and indentation.

---

### 3. `terraform validate`
Verifies whether a configuration is syntactically valid and internally consistent without contacting remote cloud APIs.

```bash
terraform validate
```

*Terminal Output:*
```text
Success! The configuration is valid.
```

---

### 4. `terraform plan`
Creates an execution plan, letting you preview the infrastructure changes that Terraform plans to make before applying them.

```bash
terraform plan
```

*Terminal Output:*
```text
Terraform will perform the following actions:

  # aws_s3_bucket.devops553 will be created
  + resource "aws_s3_bucket" "devops553" {
      + arn                         = (known after apply)
      + bucket                      = "devops-session18-s3-demo-bucket"
      + bucket_domain_name          = (known after apply)
      + force_destroy               = true
      + id                          = (known after apply)
      + region                      = (known after apply)
      + tags                        = {
          + "Environment" = "dev"
          + "ManagedBy"   = "Terraform"
          + "Name"        = "devops-session18-s3-demo-bucket"
          + "Project"     = "Session18"
        }
    }

Plan: 1 to add, 0 to change, 0 to destroy.

Changes to Outputs:
  + bucket_arn    = (known after apply)
  + bucket_name   = "devops-session18-s3-demo-bucket"
  + bucket_region = (known after apply)
```

---

### 5. `terraform apply`
Executes the actions proposed in a Terraform plan to create the AWS S3 bucket.

```bash
terraform apply -auto-approve
```

*Terminal Output:*
```text
aws_s3_bucket.devops553: Creating...
aws_s3_bucket.devops553: Creation complete after 3s [id=devops-session18-s3-demo-bucket]

Apply complete! Resources: 1 added, 0 changed, 0 destroyed.

Outputs:

bucket_arn = "arn:aws:s3:::devops-session18-s3-demo-bucket"
bucket_name = "devops-session18-s3-demo-bucket"
bucket_region = "us-east-1"
```

---

### 6. `terraform show`
Provides human-readable output from a state or plan file to inspect all provisioned attributes.

```bash
terraform show
```

*Terminal Output:*
```text
# aws_s3_bucket.devops553:
resource "aws_s3_bucket" "devops553" {
    arn                         = "arn:aws:s3:::devops-session18-s3-demo-bucket"
    bucket                      = "devops-session18-s3-demo-bucket"
    force_destroy               = true
    id                          = "devops-session18-s3-demo-bucket"
    region                      = "us-east-1"
    tags                        = {
        "Environment" = "dev"
        "ManagedBy"   = "Terraform"
        "Name"        = "devops-session18-s3-demo-bucket"
        "Project"     = "Session18"
    }
}
```

---

### 7. `terraform output`
Extracts the values of an output variable from the state file.

```bash
terraform output
```

*Terminal Output:*
```text
bucket_arn = "arn:aws:s3:::devops-session18-s3-demo-bucket"
bucket_name = "devops-session18-s3-demo-bucket"
bucket_region = "us-east-1"
```

---

### 8. `terraform destroy`
Deletes all managed infrastructure tracked by the Terraform state file.

```bash
terraform destroy -auto-approve
```

*Terminal Output:*
```text
aws_s3_bucket.devops553: Destroying... [id=devops-session18-s3-demo-bucket]
aws_s3_bucket.devops553: Destruction complete after 2s

Destroy complete! Resources: 1 destroyed.
```
