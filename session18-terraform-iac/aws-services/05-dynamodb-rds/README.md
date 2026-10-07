# Amazon DynamoDB & Amazon RDS - Database Services

## Part 1: Amazon DynamoDB (NoSQL)

### 1.1 What is DynamoDB?
**Amazon DynamoDB** is a fully managed, serverless, key-value and document NoSQL database designed to deliver single-digit millisecond latency at any scale. It offers built-in high availability, multi-Region replication, and automatic throughput scaling.

### 1.2 Core DynamoDB Data Modeling Concepts
- **Tables**: A collection of data items (similar to a collection in MongoDB or a table in SQL, but schema-less).
- **Items**: A group of attributes that is uniquely identifiable among all of the other items (similar to a row in a relational database or a JSON document). Maximum item size is 400 KB.
- **Attributes**: A fundamental data element, requiring no pre-declaration (similar to a column/field). Can be scalar (string, number, binary, boolean), document (list, map), or set.
- **Primary Keys**:
  - **Partition Key (PK) / Hash Key**: A single attribute used by DynamoDB's internal hash function to partition and distribute items across physical storage nodes.
  - **Sort Key (SK) / Range Key**: An optional secondary attribute used to sort items with the same partition key. Enables composite primary keys (e.g., `PK: UserId`, `SK: OrderTimestamp`).

### 1.3 DynamoDB Key Use Cases
- High-concurrency shopping carts and session stores.
- Mobile gaming leaderboards and real-time player states.
- IoT telemetry ingestion pipelines with time-series sort keys.
- Serverless web applications powered by AWS Lambda.

---

## Part 2: Amazon Relational Database Service (RDS)

### 2.1 What is RDS?
**Amazon Relational Database Service (Amazon RDS)** is a managed web service that simplifies the setup, operation, and scaling of traditional relational databases in the cloud. It automates administrative tasks such as hardware provisioning, database setup, patching, and backups.

### 2.2 Supported Database Engines
1. **Amazon Aurora** (MySQL & PostgreSQL compatible proprietary cloud-native database)
2. **PostgreSQL**
3. **MySQL**
4. **MariaDB**
5. **Oracle Database**
6. **Microsoft SQL Server**

### 2.3 DB Instances
A **DB Instance** is an isolated database environment running in the cloud with dedicated compute resources (CPU, Memory) and storage (gp3, io2). Instances run inside dedicated DB Subnet Groups within your private VPC subnets.

### 2.4 Security & Compliance
- **VPC Isolation**: Deployed in private subnets with no public IP.
- **Security Groups**: Network access restricted strictly to application server security groups.
- **Encryption**: KMS-managed encryption at rest for database storage, automated backups, and snapshots; TLS/SSL in transit.
- **IAM Authentication**: Passwordless database authentication via IAM database tokens.

### 2.5 Backups & Recovery
- **Automated Backups**: Continuous transaction log archiving with point-in-time recovery (PITR) down to any second within the retention window (up to 35 days).
- **Manual Snapshots**: User-initiated full storage snapshots preserved until explicitly deleted, even after instance termination.

### 2.6 High Availability: Multi-AZ vs Read Replicas

| Dimension | Multi-AZ Deployment | Read Replicas |
| :--- | :--- | :--- |
| **Primary Purpose** | **High Availability & Disaster Recovery** | **Read Performance Scalability** |
| **Replication Type** | **Synchronous** | **Asynchronous** |
| **Secondary Target** | Standby instance in a second AZ | Active read-only instances (up to 15) |
| **Failover Behavior** | **Automatic**: DNS flips to standby in 60–120s | Manual promotion to standalone DB |
| **Traffic Handling** | Standby cannot serve read/write queries | Serves read traffic (`SELECT` queries) |
| **Cross-Region** | No (within same Region) | Yes (can replicate across AWS Regions) |

### 2.7 RDS Key Use Cases
- Complex relational ERP and CRM transactional business applications.
- Applications requiring ACID compliance and complex multi-table `JOIN` queries.
- Legacy application migrations from on-premises databases to the cloud.

---

## Part 3: Architecture Comparison: DynamoDB vs RDS

| Requirement | Choose Amazon DynamoDB | Choose Amazon RDS |
| :--- | :--- | :--- |
| **Data Schema** | Semi-structured / rapidly evolving schema | Rigid, well-defined relational tables |
| **Transactions / Queries**| Simple Key-Value / Query by partition key | Complex queries, joins, aggregations |
| **Scale & Traffic** | Massive spikes (100k+ IOPS), unpredictable traffic | Predictable transactional workload |
| **Management** | Serverless, no patching, auto-scales | Managed instance sizes, scheduled maintenance |
