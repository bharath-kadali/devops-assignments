# AWS Identity and Access Management (IAM) - Governance

## 1. What is IAM?
**AWS Identity and Access Management (IAM)** is a global web service that provides fine-grained access control across AWS services and resources. It allows you to specify who is authenticated (signed in) and authorized (has permissions) to perform actions on AWS resources without additional charges.

---

## 2. Core IAM Entities

### 2.1 Users
An **IAM User** represents a human user or an interactive service identity within your AWS account.
- Consists of a friendly name and permanent credentials.
- **Console access**: Protected via password + Multi-Factor Authentication (MFA).
- **Programmatic access**: Authenticated using Access Key ID and Secret Access Key via AWS CLI, SDKs, or APIs.

### 2.2 Groups
An **IAM Group** is a collection of IAM users.
- Simplifies permission management: You attach policies directly to a group, and all members inherit those permissions.
- A user can belong to multiple groups.
- Groups cannot be nested (groups cannot contain other groups).

### 2.3 Roles
An **IAM Role** is an IAM identity that you can create in your account that has specific permissions, but is **not** associated with a specific person.
- Roles do not use long-term credentials (no permanent access keys or passwords).
- Instead, trusted entities (EC2 instances, Lambda functions, cross-account administrators) assume the role and receive temporary security credentials via the **AWS Security Token Service (STS)**.
- Common use case: Allowing an EC2 instance or Kubernetes pod to access an S3 bucket without embedding hardcoded AWS credentials in code.

---

## 3. Policies & Permissions

### 3.1 Policies
An **IAM Policy** is a JSON document that defines one or more permissions.
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowS3ReadOnly",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::my-production-bucket",
        "arn:aws:s3:::my-production-bucket/*"
      ]
    }
  ]
}
```

### 3.2 Types of Policies
1. **Identity-based Policies**: Attached to Users, Groups, or Roles.
   - **AWS Managed Policies**: Maintained and updated by AWS (e.g., `AdministratorAccess`, `AmazonS3ReadOnlyAccess`).
   - **Customer Managed Policies**: Created and customized by your organization.
   - **Inline Policies**: Embedded directly into a single user, group, or role.
2. **Resource-based Policies**: Attached directly to resources (e.g., S3 Bucket Policies, KMS Key Policies, SQS Queues).

---

## 4. Principle of Least Privilege
The **Principle of Least Privilege (PoLP)** dictates that identities should only be granted the minimum permissions strictly required to perform their intended tasks, for the shortest duration necessary.
- Start with zero permissions.
- Grant read-only access where write/delete is not required.
- Scope down `Resource: "*"` to specific resource ARNs whenever possible.
- Use condition keys (e.g., `aws:PrincipalArn`, `aws:SourceIp`, `aws:MultiFactorAuthPresent`).

---

## 5. IAM Security Best Practices

1. **Lock Down the AWS Root User**:
   - Never use the root account for daily administrative tasks.
   - Enable hardware or authenticator-app MFA immediately on the root user.
   - Delete all root access keys.
2. **Enforce Multi-Factor Authentication (MFA)**:
   - Mandatory MFA for all privileged users and console logins.
3. **Use IAM Roles for Applications & Workloads**:
   - Use EC2 Instance Profiles, ECS Task Roles, or EKS IAM Roles for Service Accounts (IRSA) rather than saving static access keys in containers or servers.
4. **Regularly Rotate Credentials & Review Inactive Accounts**:
   - Regularly audit and disable credentials unused for more than 90 days using the IAM Credential Report.
5. **Implement Permission Boundaries & SCPs**:
   - Use Service Control Policies (SCPs) in AWS Organizations to set cluster-wide maximum permission ceilings.

---

## 6. Common Real-World Use Cases

- **Developer Access**: Human developers assigned to groups (e.g., `DevelopersGroup`) granted access to non-production accounts via federated SSO / IAM Identity Center.
- **CI/CD Pipelines**: GitHub Actions assuming an IAM Role via OpenID Connect (OIDC) to push Docker images to Amazon ECR without storing permanent AWS Access Keys in GitHub Secrets.
- **EC2 Instance Profile**: Web servers running on EC2 assuming a role that allows uploading customer images directly to S3.
