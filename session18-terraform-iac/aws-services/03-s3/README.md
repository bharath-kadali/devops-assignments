# Amazon Simple Storage Service (S3) - Storage

## 1. What is S3?
**Amazon Simple Storage Service (Amazon S3)** is an industry-leading object storage service offering industry-leading scalability, data availability, security, and performance. S3 is designed for 99.999999999% (11 9's) of data durability.

---

## 2. Core S3 Concepts

### 2.1 Buckets
A **Bucket** is a top-level container for objects stored in Amazon S3.
- Bucket names are globally unique across all AWS accounts in all regions worldwide.
- Named using DNS-compliant strings between 3 and 63 characters long.
- Tied to a specific AWS Region when created.

### 2.2 Objects
An **Object** is the fundamental entity stored in Amazon S3:
- Consists of object data (the file itself) and metadata (key-value pairs describing the object).
- Identified uniquely inside a bucket by a **Key** (the path/filename, e.g., `photos/2026/vacation.jpg`).
- Objects can range in size from 0 bytes up to 5 TB.

---

## 3. S3 Storage Classes

| Storage Class | Durability | Availability | Minimum Storage Duration | Retrieval Cost | Ideal Use Case |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **S3 Standard** | 99.999999999% | 99.99% | None | None | Frequently accessed data, active websites, mobile assets |
| **S3 Intelligent-Tiering** | 99.999999999% | 99.9% | None | Auto tier fee | Data with unknown or unpredictable access patterns |
| **S3 Standard-IA (Infrequent Access)** | 99.999999999% | 99.9% | 30 days | Per-GB fee | Long-term storage, backups, disaster recovery accessed infrequently |
| **S3 One Zone-IA** | 99.999999999% | 99.5% | 30 days | Per-GB fee | Non-critical, reproducible data kept in a single AZ |
| **S3 Glacier Flexible Retrieval** | 99.999999999% | 99.99% | 90 days | Per-GB fee | Archives retrieved in minutes to hours |
| **S3 Glacier Deep Archive** | 99.999999999% | 99.99% | 180 days | Per-GB fee | Lowest cost cloud storage; retrieved in 12–48 hours; regulatory compliance |

---

## 4. Key Features & Governance

### 4.1 Versioning
- Keeps multiple variants of an object in the same bucket.
- Protects against accidental overwrites and deletions (a delete simply places a "Delete Marker" that can be restored).
- Once enabled on a bucket, versioning cannot be disabled—only suspended.

### 4.2 Lifecycle Policies
Automated rules to transition objects between storage classes or expire (delete) them after specified time intervals:
```text
Day 0: Upload to S3 Standard
  │
  ├─► Day 30: Transition to S3 Standard-IA
  │
  ├─► Day 90: Transition to S3 Glacier Flexible Retrieval
  │
  └─► Day 365: Expire / Permanently Delete
```

### 4.3 Encryption
- **Encryption at Rest**:
  - **SSE-S3**: AWS-managed keys using 256-bit AES (enabled by default).
  - **SSE-KMS**: AWS Key Management Service keys offering audit trails and key rotation policies.
  - **SSE-C**: Customer-provided encryption keys.
- **Encryption in Transit**: Enforced via TLS/HTTPS using bucket policies enforcing `aws:SecureTransport: "true"`.

### 4.4 Bucket Policies
JSON access policies attached directly to the S3 bucket to control read/write permissions at scale:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "EnforceHTTPSOnly",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::my-company-assets",
        "arn:aws:s3:::my-company-assets/*"
      ],
      "Condition": {
        "Bool": {
          "aws:SecureTransport": "false"
        }
      }
    }
  ]
}
```

---

## 5. Common Use Cases

1. **Static Website Hosting**: Hosting HTML, CSS, JavaScript, and SPA frontends via S3 and CloudFront CDN.
2. **Data Lakes & Big Data Analytics**: Staging raw, transformed, and analytical parquet/CSV data queried with AWS Athena, EMR, or Snowflake.
3. **Application Media Storage**: User avatar uploads, documents, PDF reports, and video uploads.
4. **Backup & Disaster Recovery**: Storing database dumps, system images, and snapshots with Glacier lifecycle transitions.
