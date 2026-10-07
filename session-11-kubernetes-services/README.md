# Session 11: Kubernetes Services

**Author:** [Bharath Kadali]
**Course:** SST DevOps & Cloud [SWE]
**Session:** 11 - Kubernetes Services
**Repository:** devops-heros / session-11-kubernetes-services

---

## Task 1: Kubernetes Port Architecture & Clarification Drill

```text
Client Browser ──► [nodePort: 30080] (Host IP)
                        │
                        ▼
                   [port: 8080] (Service VIP)
                        │
                        ▼
                   [targetPort: 80] (Pod Network)
                        │
                        ▼
                   [containerPort: 80] (Container Engine / Nginx)
```

**Screenshot:**
`![Port Architecture](./screenshots/01-port-architecture.png)`

---

## Task 2: Type 1 Service — ClusterIP (Default Internal Networking)

**Commands:**
```bash
cd 01-clusterip/
kubectl apply -f app-deployment.yaml
kubectl apply -f service.yaml
kubectl get svc web-service-clusterip
kubectl get endpoints web-service-clusterip
kubectl apply -f client-pod.yaml
kubectl exec -it curl-client -- curl -s http://web-service-clusterip:8080
```

**Screenshots:**
`![ClusterIP Service](./screenshots/02-clusterip-service.png)`
`![ClusterIP Execution](./screenshots/02-clusterip-execution.png)`

---

## Task 3: Type 2 Service — NodePort (Host-Level External Ingress)

**Commands:**
```bash
cd 02-nodeport/
kubectl apply -f app-deployment.yaml
kubectl apply -f service.yaml
kubectl get svc web-service-nodeport
MINIKUBE_IP=$(minikube ip)
curl -I http://${MINIKUBE_IP}:30080
```

**Screenshots:**
`![NodePort Output](./screenshots/03-nodeport-service.png)`
`![NodePort Execution](./screenshots/03-nodeport-execution.png)`

---

## Task 4: Type 3 Service — LoadBalancer (Cloud-Native Ingress Simulation)

**Commands:**
```bash
cd 03-loadbalancer/
kubectl apply -f app-deployment.yaml
kubectl apply -f service.yaml
minikube tunnel
kubectl get svc web-service-loadbalancer
```

**Screenshots:**
`![LoadBalancer Service](./screenshots/04-loadbalancer-service.png)`
`![LoadBalancer Execution](./screenshots/04-loadbalancer-execution.png)`

---

## Task 5: Type 4 Service — ExternalName (CoreDNS CNAME Alias Redirection)

**Commands:**
```bash
cd 04-externalname/
kubectl apply -f service.yaml
kubectl apply -f client-pod.yaml
kubectl get svc external-database-service
kubectl exec -it dns-test-client -- nslookup external-database-service
```

**Screenshots:**
`![ExternalName Service](./screenshots/05-externalname-service.png)`
`![ExternalName Output](./screenshots/05-externalname-output.png)`

---

## Task 6: Type 5 Service — Headless Service

**Commands:**
```bash
cd 05-headless/
kubectl apply -f service.yaml
kubectl apply -f app-statefulset.yaml
kubectl apply -f client-pod.yaml
kubectl exec -it headless-dns-client -- nslookup web-service-headless
```

**Screenshots:**
`![Headless Output](./screenshots/06-headless-output.png)`
`![Headless Execution](./screenshots/06-headless-execution.png)`

---

## Task 7: Services Without Selectors (Manual Endpoints Mapping)

**Commands:**
```bash
# Create Service and then create Endpoints pointing to external IP.
# Refer to manual instructions.
kubectl get endpoints external-legacy-db
```

**Screenshots:**
`![Empty Endpoints](./screenshots/07-empty-endpoints.png)`
`![Manual Endpoints Map](./screenshots/07-manual-endpoints.png)`

---

## Task 8: FQDN & CoreDNS Deep Dive Architecture Analysis

**Commands:**
```bash
kubectl get pods -n kube-system -l k8s-app=kube-dns -o wide
kubectl exec -it curl-client -- cat /etc/resolv.conf
kubectl exec -it curl-client -- nslookup web-service-clusterip
```

**Screenshots:**
`![Resolv Conf Output](./screenshots/08-resolv-conf.png)`
`![CoreDNS nslookup](./screenshots/08-coredns-nslookup.png)`

---

## Task 9: Pod Identity & Lifecycle Invariance Drill

**Commands:**
```bash
# Apply deployment and statefulset, delete one pod of each, and observe recreation.
```

**Screenshots:**
`![Pre Delete Stats](./screenshots/09-pre-delete-stats.png)`
`![Post Delete Stats](./screenshots/09-post-delete-stats.png)`

---

## Task 10: Master Architectural Matrix — Deployment vs. StatefulSet vs. DaemonSet

| Architectural Metric | Deployment | StatefulSet | DaemonSet |
| --- | --- | --- | --- |
| **Primary Workload Type** | Stateless microservices, Web APIs | Clustered databases, Distributed queues | Node-level infrastructure agents |
| **Pod Naming Scheme** | Random hash (`<deploy>-<rs-hash>-<random>`) | Deterministic ordinal (`<name>-0, 1, 2`) | Deterministic node hash (`<ds>-<random>`) |
| **Pod Identity Persistence** | Ephemeral (disposable upon death) | Invariant (identity, IP, hostname stick) | Bound to individual worker node |
| **Startup / Shutdown Order** | Non-ordered, parallel | Strictly sequential (`0 -> 1 -> 2`, reversed on termination) | Parallel across all eligible nodes |
| **Storage Mechanism** | Shared volume or ephemeral emptyDir | Dedicated PersistentVolume per ordinal via `volumeClaimTemplates` | HostPath mounts or node-local storage |
| **Associated Service Type** | Standard `ClusterIP` / `NodePort` / `LoadBalancer` | **Headless Service** (`clusterIP: None`) mandatory for discovery | None or local `ClusterIP` |
| **Scaling Behavior** | Scales arbitrarily across healthy nodes | Scales ordinally (adds/removes at the tail) | Scales automatically when nodes join/leave |

**Screenshot:**
`![Matrix Output](./screenshots/10-architectural-matrix.png)`

---

## Task 11: Production Cost Optimization & Service Selection Decision Tree

```text
Need to expose service outside cluster?
│
├── NO ──► Need direct pod-to-pod discovery (Kafka/DB)?
│           ├── YES ──► Use HEADLESS SERVICE (clusterIP: None)
│           └── NO  ──► Use CLUSTERIP (Default)
│
└── YES ──► Connecting to an external 3rd-party domain (AWS RDS / Stripe)?
            ├── YES ──► Use EXTERNALNAME
            └── NO  ──► Are you on Public Cloud (AWS/GCP/Azure)?
                         ├── YES (HTTP/HTTPS) ──► Expose 1 INGRESS via LOADBALANCER,
                         │                        apps as internal CLUSTERIP
                         ├── YES (TCP/UDP)    ──► Direct LOADBALANCER
                         └── NO (On-Prem/Dev) ──► NODEPORT
```

**Screenshot:**
`![Cost Optimization Tree](./screenshots/11-cost-optimization-tree.png)`

---

## Task 12: Minikube Docker-Driver Port Binding & Tunnel Gotcha Analysis

Docker driver limits direct Node IP reachability from the host on macOS and Windows. 
Workarounds: `minikube tunnel` or `minikube service <svc> --url`.

**Commands:**
```bash
NODE_IP=$(minikube ip)
curl --connect-timeout 2 -s http://${NODE_IP}:30080
minikube service web-service-nodeport --url
```

**Screenshots:**
`![Direct Node Failure](./screenshots/12-direct-node-failure.png)`
`![Minikube Tunnel Solution](./screenshots/12-minikube-tunnel.png)`
