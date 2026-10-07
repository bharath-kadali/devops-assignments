# 08 - Session 19 Cloud Infrastructure Mini Project

## Architecture

This project provisions the complete Suggested Architecture using Terraform:
```text
Terraform
|
├── VPC (10.20.0.0/16)
|
├── Subnet (Public Subnet: 10.20.1.0/24)
|
├── Security Group (HTTP:80, SSH:22, Egress:All)
|
├── EC2 (Amazon Linux 2023 Web Server)
|
└── S3 (Encrypted Object Storage Bucket)
```

---

## Project Files

```text
08-mini-project/
├── versions.tf               # Terraform and AWS provider configuration (~> 5.0)
├── variables.tf              # Region, instance_type, bucket_name
├── main.tf                   # VPC, Subnet, IGW, Route Table, SG, EC2, S3
├── outputs.tf                # VPC, Subnet, SG, EC2 public IP, S3 Bucket outputs
├── terraform.tfvars.example  # Sample environment variables
└── README.md                 # Documentation
```

---

## Execution Guide

### 1. Initialize
```bash
terraform init
```

### 2. Format & Validate
```bash
terraform fmt
terraform validate
```

### 3. Plan
```bash
terraform plan
```

### 4. Apply
```bash
terraform apply -auto-approve
```

### 5. Inspect Outputs & State
```bash
terraform output
terraform state list
```

### 6. Clean Up
```bash
terraform destroy -auto-approve
```
