# Amazon Virtual Private Cloud (VPC) - Networking

## 1. What is a VPC?
**Amazon Virtual Private Cloud (Amazon VPC)** enables you to launch AWS resources into a logically isolated, customizable virtual software-defined network that you control. You define its IP address space, subnets, route tables, network gateways, and security perimeters.

---

## 2. Core VPC Networking Components

### 2.1 CIDR (Classless Inter-Domain Routing)
CIDR is the notation used to define the IPv4 address ranges of your VPC and subnets:
- Example: `10.0.0.0/16` provides 65,536 private IP addresses (`10.0.0.0` to `10.0.255.255`).
- Smallest allowed block in AWS VPC: `/28` (16 IP addresses).
- Largest allowed block in AWS VPC: `/16` (65,536 IP addresses).
- *AWS Reservation*: In every subnet CIDR block, AWS reserves **5 IP addresses** (`.0` network, `.1` VPC router, `.2` AWS DNS, `.3` future use, and `.255` broadcast).

### 2.2 Subnets
A **Subnet** is a subdivision of a VPC's IP address range spanning a specific single **Availability Zone (AZ)**:
- Resources within different subnets in the same VPC can communicate by default via the local router.
- Subnets are defined as either **Public** or **Private**.

### 2.3 Public vs Private Subnets
- **Public Subnet**: Subnet whose route table has a route to an **Internet Gateway (IGW)** (`0.0.0.0/0 -> igw-xxxx`). Resources can receive public IPs and communicate directly with the internet.
- **Private Subnet**: Subnet whose route table does NOT route to an Internet Gateway. Protected from inbound internet traffic. Outbound internet access is routed via a **NAT Gateway**.

### 2.4 Route Tables
A set of routing rules (routes) that determine where network traffic from your subnet or gateway is directed:
- Every VPC has a main (default) route table with a local route: `10.0.0.0/16 -> local`.
- Subnets must be explicitly associated with custom route tables to direct external traffic.

### 2.5 Internet Gateway (IGW)
A horizontally scaled, redundant, highly available VPC component that allows communication between instances in your VPC and the internet:
- Performs 1:1 Network Address Translation (NAT) for instances with public IPv4 addresses.
- Attached directly to the VPC.

### 2.6 NAT Gateway
A managed Network Address Translation service that enables instances in a **private subnet** to connect to internet services (e.g., download OS security patches, pull public dependencies), while preventing the external internet from initiating connections to those private instances:
- Deployed inside a **Public Subnet** and assigned an Elastic IP (EIP).
- Private subnets configure `0.0.0.0/0 -> nat-xxxx`.

---

## 3. Defense-in-Depth: Security Groups vs Network ACLs

| Feature | Security Groups (SG) | Network ACLs (NACL) |
| :--- | :--- | :--- |
| **Operates At** | Instance / ENI level | Subnet boundary level |
| **State Nature** | **Stateful**: Return traffic automatically permitted | **Stateless**: Inbound and outbound must be explicitly allowed |
| **Rule Rules** | Allow rules only (no deny rules) | Numbered Allow AND Deny rules evaluated sequentially |
| **Evaluation Order** | All rules evaluated together | Evaluated in numerical order (lowest rule number first) |
| **Scope** | Applies only to attached instances | Applies automatically to all instances in associated subnet |

---

## 4. Standard Multi-Tier Architecture Diagram

```text
                           Internet
                              │
                              ▼
                      [ Internet Gateway ]
                              │
            ┌─────────────────┴─────────────────┐
            │       VPC: 10.0.0.0/16            │
            │                                   │
            │  ┌─────────────────────────────┐  │
            │  │ PUBLIC SUBNET (10.0.1.0/24) │  │
            │  │  ├─ Public ALB / Bastion    │  │
            │  │  └─ NAT Gateway (EIP)       │  │
            │  └──────────────┬──────────────┘  │
            │                 │                 │
            │  ┌──────────────▼──────────────┐  │
            │  │ PRIVATE APP SUBNET (10.0.2) │  │
            │  │  └─ Backend App EC2 / EKS   │  │
            │  └──────────────┬──────────────┘  │
            │                 │                 │
            │  ┌──────────────▼──────────────┐  │
            │  │ PRIVATE DB SUBNET (10.0.3)  │  │
            │  │  └─ Isolated RDS / Aurora   │  │
            │  └─────────────────────────────┘  │
            └───────────────────────────────────┘
```
