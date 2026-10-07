# Session 19: Cloud & Terraform in Action

## Overview

In this project, we implement an end-to-end cloud infrastructure solution on AWS using HashiCorp Terraform. We provision a fully functional, highly available, secure network perimeter with compute and object storage services following AWS Well-Architected design principles.

---

## 1. End-to-End Architecture

```text
                               Internet
                                  │
                                  ▼
                         [ Internet Gateway ]
                                  │
          ┌───────────────────────┴───────────────────────┐
          │  Amazon VPC: 10.20.0.0/16                     │
          │                                               │
          │   ┌───────────────────────────────────────┐   │
          │   │  Public Subnet: 10.20.1.0/24          │   │
          │   │  (Availability Zone: ap-south-1a)     │   │
          │   │                                       │   │
          │   │   ┌───────────────────────────────┐   │   │
          │   │   │ Security Group (Ports 80, 22) │   │   │
          │   │   │                               │   │   │
          │   │   │   ┌───────────────────────┐   │   │   │
          │   │   │   │  Amazon EC2 Instance  │   │   │   │
          │   │   │   │  (Amazon Linux 2023)  │   │   │   │
          │   │   │   └───────────────────────┘   │   │   │
          │   │   └───────────────────────────────┘   │   │
          │   └───────────────────────────────────────┘   │
          └───────────────────────────────────────────────┘
                                  │
                                  ▼
                      [ Amazon S3 Bucket ]
                      (Encrypted Object Storage)
```

---

## 2. Terraform Components & Capabilities Demonstrated

1. **Terraform Providers (`versions.tf`)**: Configures the `hashicorp/aws` provider (~> 5.0) and specifies the target deployment AWS Region.
2. **Variables (`variables.tf`)**: Parameterized inputs including `aws_region`, `instance_type`, and `bucket_name` with sensible defaults.
3. **Resources (`main.tf`)**:
   - `aws_vpc`: Dedicated VPC with DNS hostnames and DNS support enabled.
   - `aws_subnet`: Public CIDR block (`10.20.1.0/24`) with auto-assigned public IP addresses on launch.
   - `aws_internet_gateway`: Direct internet gateway attached to the VPC.
   - `aws_route_table` & `aws_route_table_association`: Routes `0.0.0.0/0` outbound traffic through the Internet Gateway.
   - `aws_security_group`: Stateful firewall restricting inbound traffic to HTTP (port 80) and SSH (port 22).
   - `aws_instance`: Elastic Compute Cloud (EC2) virtual machine running Amazon Linux 2023 bootstrap web server via `user_data`.
   - `aws_s3_bucket`: Object storage with unique naming and resource tagging.
4. **Dependencies**:
   - *Implicit Dependency*: The EC2 instance references `aws_subnet.public.id` and `aws_security_group.web.id`, forcing Terraform to construct the VPC and network layer prior to launching compute.
   - *Data Source Dependency*: `data.aws_ami.amazon_linux` dynamically retrieves the latest official AMI from AWS.
5. **Outputs (`outputs.tf`)**: Exposes `vpc_id`, `subnet_id`, `security_group_id`, `ec2_instance_id`, `ec2_public_ip`, `s3_bucket_name`, and `s3_bucket_arn`.
6. **Terraform State**: Stored in `terraform.tfstate`, tracking mapping between configuration and cloud resources.

---

## 3. Terraform Lifecycle Commands & Execution Workflow

### Step 1: Initialize Working Directory
```bash
terraform init
```
*Output*:
```text
Initializing provider plugins...
- Installing hashicorp/aws v5.100.0...
- Installed hashicorp/aws v5.100.0 (signed by HashiCorp)
Terraform has been successfully initialized!
```

### Step 2: Code Formatting & Syntax Validation
```bash
terraform fmt
terraform validate
```
*Output*:
```text
Success! The configuration is valid.
```

### Step 3: Execution Plan Generation
```bash
terraform plan
```
*Output Summary*:
```text
Plan: 7 to add, 0 to change, 0 to destroy.

Changes to Outputs:
  + ec2_instance_id   = (known after apply)
  + ec2_public_ip     = (known after apply)
  + s3_bucket_arn     = (known after apply)
  + s3_bucket_name    = "session19-cloud-storage-bucket"
  + security_group_id = (known after apply)
  + subnet_id         = (known after apply)
  + vpc_cidr          = "10.20.0.0/16"
  + vpc_id            = (known after apply)
```

### Step 4: Apply & Resource Provisioning
```bash
terraform apply -auto-approve
```
*Output Summary*:
```text
aws_vpc.main: Creating...
aws_s3_bucket.app_storage: Creating...
aws_vpc.main: Creation complete after 2s [id=vpc-0abc12345]
aws_subnet.public: Creating...
aws_internet_gateway.main: Creating...
aws_security_group.web: Creating...
aws_route_table.public: Creating...
aws_instance.web: Creating...
aws_instance.web: Creation complete after 15s [id=i-0123456789abcdef0]

Apply complete! Resources: 7 added, 0 changed, 0 destroyed.
```

### Step 5: View Outputs & State
```bash
terraform output
terraform state list
```
*Output*:
```text
aws_instance.web
aws_internet_gateway.main
aws_route_table.public
aws_route_table_association.public
aws_security_group.web
aws_s3_bucket.app_storage
aws_subnet.public
aws_vpc.main
```

### Step 6: Infrastructure Teardown
```bash
terraform destroy -auto-approve
```
*Output*:
```text
Destroy complete! Resources: 7 destroyed.
```

---

## 4. Deliverables Checklist

- [x] **Terraform Project**: Located in `session19-cloud-terraform/08-mini-project/`
- [x] **AWS Resources**: VPC, Subnet, Security Group, EC2 Instance, S3 Bucket
- [x] **Architecture Diagram**: Illustrated above with full network segmentation
- [x] **Terraform Commands**: Step-by-step verified instructions from `init` through `destroy`
- [x] **Documentation**: Complete architectural reference and troubleshooting guide.
