# Session 18: Terraform & Infrastructure as Code

## Overview

This repository covers Infrastructure as Code (IaC) using HashiCorp Terraform alongside in-depth architectural research into fundamental AWS Cloud services.

---

## Deliverables Summary

### Task 1: Terraform S3 Demo Project
Located in [`terraform-s3-demo/`](file:///c:/Users/Bharath%20Kadali/Desktop/Year%203/Term%201/Devops/devops-homework/devops-heros/session18-terraform-iac/terraform-s3-demo/):
- `main.tf`: AWS S3 bucket resource definition
- `variables.tf`: Parameterized input variables
- `outputs.tf`: Clean output values (`bucket_name`, `bucket_arn`, `bucket_region`)
- `provider.tf`: AWS Provider and Terraform engine configuration
- `terraform.tfvars`: Environment variable definitions
- [`README.md`](file:///c:/Users/Bharath%20Kadali/Desktop/Year%203/Term%201/Devops/devops-homework/devops-heros/session18-terraform-iac/terraform-s3-demo/README.md): Complete lifecycle workflow and terminal outputs (`init`, `fmt`, `validate`, `plan`, `apply`, `show`, `output`, `destroy`)

---

### Task 2: AWS Services Research
Located in [`aws-services/`](file:///c:/Users/Bharath%20Kadali/Desktop/Year%203/Term%201/Devops/devops-homework/devops-heros/session18-terraform-iac/aws-services/):
1. [**01. IAM - Governance**](file:///c:/Users/Bharath%20Kadali/Desktop/Year%203/Term%201/Devops/devops-homework/devops-heros/session18-terraform-iac/aws-services/01-iam/README.md): IAM users, groups, roles, JSON policies, permissions, principle of least privilege, best practices.
2. [**02. EC2 - Compute**](file:///c:/Users/Bharath%20Kadali/Desktop/Year%203/Term%201/Devops/devops-homework/devops-heros/session18-terraform-iac/aws-services/02-ec2/README.md): AMIs, instance types, key pairs, security groups, EBS block storage, public vs private IPs, instance lifecycle.
3. [**03. S3 - Storage**](file:///c:/Users/Bharath%20Kadali/Desktop/Year%203/Term%201/Devops/devops-homework/devops-heros/session18-terraform-iac/aws-services/03-s3/README.md): Buckets, objects, storage classes (Standard, IA, Glacier), versioning, lifecycle transitions, encryption, bucket policies.
4. [**04. VPC - Networking**](file:///c:/Users/Bharath%20Kadali/Desktop/Year%203/Term%201/Devops/devops-homework/devops-heros/session18-terraform-iac/aws-services/04-vpc/README.md): CIDR calculations, subnets, route tables, Internet Gateway, NAT Gateway, Security Groups vs NACLs, public vs private subnets.
5. [**05. DynamoDB & RDS - Database Services**](file:///c:/Users/Bharath%20Kadali/Desktop/Year%203/Term%201/Devops/devops-homework/devops-heros/session18-terraform-iac/aws-services/05-dynamodb-rds/README.md): DynamoDB NoSQL tables/items/keys vs Amazon RDS multi-engine relational instances, backups, Multi-AZ high availability vs Read Replicas.