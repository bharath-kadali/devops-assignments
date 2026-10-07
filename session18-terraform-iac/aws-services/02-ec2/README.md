# Amazon Elastic Compute Cloud (EC2) - Compute

## 1. What is EC2?
**Amazon Elastic Compute Cloud (Amazon EC2)** is an on-demand, scalable web service that provides resizable virtual computing capacity in the AWS cloud. It allows organizations to boot virtual server instances in minutes, scaling capacity up or down as requirements change while paying only for compute hours consumed.

---

## 2. Core EC2 Concepts & Building Blocks

### 2.1 Amazon Machine Image (AMI)
An **AMI** is a packaged, pre-configured virtual machine template containing the operating system, initial application state, software libraries, and boot permissions.
- **AWS Provided AMIs**: Maintained Linux (Amazon Linux 2023, Ubuntu, RHEL) and Windows Server images.
- **Community & Marketplace AMIs**: Customized stacks (e.g., Bitnami WordPress, CIS-hardened OS).
- **Custom AMIs (Golden Images)**: Custom built by taking an EBS snapshot of a customized instance.

### 2.2 Instance Types
EC2 offers diverse instance families optimized for distinct workload profiles:
- **General Purpose (`t4g`, `m6i`)**: Balanced CPU, memory, and networking. Ideal for web servers, dev environments, microservices.
- **Compute Optimized (`c6i`, `c7g`)**: High compute-to-memory ratio. Ideal for batch processing, video encoding, high-performance web servers.
- **Memory Optimized (`r6i`, `x2gd`)**: Large memory footprints. Ideal for in-memory databases (Redis, Memcached), relational caches, big data analytics.
- **Storage Optimized (`i3en`, `d3`)**: High local NVMe storage IOPS. Ideal for NoSQL databases, data warehousing.
- **Accelerated Computing (`p4d`, `g5`)**: Hardware GPUs/TPUs for AI model training, machine learning inference, graphics rendering.

### 2.3 Key Pairs
EC2 uses public-key cryptography to authenticate and encrypt login sessions:
- AWS stores the **public key** on the instance during launch.
- You keep the **private key** file (`.pem` for OpenSSH or `.ppk` for PuTTY) on your local machine.
- Provides secure SSH access for Linux instances and password decryption for Windows Administrator accounts without transmitting passwords across the network.

### 2.4 Security Groups
A **Security Group** acts as a stateful virtual firewall controlling inbound and outbound network traffic to an EC2 instance:
- **Stateful**: If you send an outbound request, return traffic is automatically permitted regardless of inbound rules.
- **Default behavior**: Denies all inbound traffic by default; allows all outbound traffic.
- Operates at the network interface (ENI) level, not the OS level.

### 2.5 Elastic Block Store (EBS)
**Amazon EBS** provides persistent, high-performance block-level storage volumes for use with EC2 instances:
- Persists independently of the life of an instance (data survives stopping or restarting the instance).
- Automatically replicated within an Availability Zone to protect against hardware failure.
- Types: General Purpose SSD (`gp3`/`gp2`), Provisioned IOPS SSD (`io2`), Throughput Optimized HDD (`st1`), Cold HDD (`sc1`).

### 2.6 Public vs Private IP Addresses
- **Private IP**: Non-routable internally allocated IPv4 address used for inter-instance communication inside the VPC. Retained throughout the instance lifetime.
- **Public IP**: Automatically allocated dynamic routable IPv4 address accessible from the internet. Released and changed when an instance is stopped and started.
- **Elastic IP (EIP)**: Static, persistent public IPv4 address allocated to your account that does not change across instance stop/start cycles.

---

## 3. EC2 Instance Lifecycle

```text
 ┌───────────────┐
 │   Launching   │
 └───────┬───────┘
         │
         ▼
 ┌───────────────┐  Stop ┌───────────────┐
 │    Running    ├──────►│    Stopped    │
 └───────┬───────┘◄──────┴───────┬───────┘
         │          Start        │
         ▼                       ▼
 ┌───────────────┐       ┌───────────────┐
 │  Rebooting    │       │  Terminated   │
 └───────────────┘       └───────────────┘
```
- **Pending**: AWS is allocating compute resources and attaching EBS volumes.
- **Running**: Instance is active and billing begins.
- **Stopping / Stopped**: VM is halted on AWS hardware; OS RAM is cleared, but EBS volumes remain intact. Hourly compute charges pause.
- **Shutting-down / Terminated**: Permanently removed. Root EBS volume deleted by default unless `delete_on_termination = false`.

---

## 4. Common Use Cases

1. **Web and Application Hosting**: Running containerized applications or standard web frameworks (Nginx, Node.js, Python Flask) behind an Application Load Balancer.
2. **Batch Processing & Background Workers**: Processing queues, image transformations, or ETL pipelines triggered by SQS.
3. **Enterprise Databases**: Self-hosting complex databases requiring specialized kernel tunings (e.g., Oracle RAC, custom PostgreSQL).
4. **CI/CD Self-Hosted Runners**: Dedicated build runners for GitHub Actions or Jenkins requiring custom compilation tools.
