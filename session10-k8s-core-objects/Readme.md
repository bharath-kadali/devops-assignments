# Session 10: Kubernetes Core Objects

**Author:** [Bharath Kadali]
**Course:** SST DevOps & Cloud [SWE]
**Session:** 10 - Kubernetes Core Objects
**Repository:** devops-heros / session10-k8s-core-objects

---

## Task 1: Cluster Health Verification & Baseline Environment Checks

Verify that the local Kubernetes cluster control plane, DNS components, and worker nodes are operational.

**Commands:**
```bash
kubectl version --output=yaml
kubectl cluster-info
kubectl get nodes -o wide
```

**Screenshot:**
`![Cluster Health](./screenshots/01-cluster-health.png)`

---

## Task 2: Standard Pod Deployment, Extended Inspection & Teardown

Deploy a standalone Nginx pod and verify readiness.

**Commands:**
```bash
kubectl apply -f pod.yml
kubectl get pods
kubectl get pods -o wide
kubectl logs nginx-pod
kubectl delete -f pod.yml
kubectl get pods
```

**Screenshot:**
`![Nginx Pod Operations](./screenshots/02-nginx-pod-operations.png)`

---

## Task 3: Error State Simulation — ErrImagePull & ImagePullBackOff

Demonstrate Kubernetes error handling when pulling a non-existent container image.

**Commands:**
```bash
kubectl apply -f pod-lifecycle/06-imagepullbackoff.yaml
kubectl get pods lifecycle-image-error
kubectl describe pod lifecycle-image-error | grep -A 10 Events:
kubectl delete -f pod-lifecycle/06-imagepullbackoff.yaml
```

**Screenshot:**
`![ImagePullBackOff Error](./screenshots/03-imagepullbackoff-error.png)`

---

## Task 4: Capturing Transient Pod Lifecycle Stages

Capture transient pod lifecycle stages (ContainerCreating -> Running -> Completed).

**Commands:**
```bash
# Terminal 1
kubectl get pods -w

# Terminal 2
kubectl apply -f hello.yml
kubectl get pods hello-pod
kubectl logs hello-pod
kubectl delete -f hello.yml
```

**Screenshot:**
`![Pod Lifecycle Stages](./screenshots/04-pod-lifecycle-stages.png)`

---

## Task 5: Exhaustive Pod Lifecycle States & Probes Lab

Validate core lifecycle states, health checks, multi-container pods, and graceful termination.

**Commands:**
```bash
cd pod-lifecycle/

# Run through the YAMLs: 02-pending, 05-crashloopbackoff, 07-readiness, 08-liveness, 09-startup, 10-init-container, 11-multi-container, 12-termination.
```

**Screenshots:**
`![Lifecycle Probes & Crashloop](./screenshots/05-lifecycle-probes-crashloop.png)`
`![Init & Multi-Container](./screenshots/05-lifecycle-init-multicontainer.png)`

---

## Task 6: Core Controller Objects Exploration (ReplicaSet & StatefulSet)

Deploy ReplicaSet for self-healing and StatefulSet for ordinal naming.

**Commands:**
```bash
kubectl apply -f replicaset.yml
kubectl get pods -l app=nginx
# Delete a pod manually to test self-healing
kubectl apply -f k8s-core-objects/statefulset.yml
kubectl get pods -l app=mysql
```

**Screenshot:**
`![Controllers RS and StatefulSet](./screenshots/06-controllers-rs-statefulset.png)`

---

## Task 7: DaemonSet Architecture & Host Agent Deployment

Deploy a DaemonSet to run exactly one pod per node.

**Commands:**
```bash
kubectl apply -f k8s-core-objects/deamonset.yml
kubectl get ds node-exporter
kubectl get pods -l app=node-exporter -o wide
```

**Screenshot:**
`![DaemonSet Verification](./screenshots/07-daemonset-verification.png)`

---

## Task 8: Deployment Upgrades, Rolling Updates & Instant Rollbacks

Demonstrate declarative zero-downtime rolling updates.

**Commands:**
```bash
cd 01-rolling-update/
kubectl apply -f deployment-v1.yaml
kubectl apply -f service.yaml
kubectl apply -f deployment-v2.yaml
kubectl rollout history deployment/app-rolling
kubectl rollout undo deployment/app-rolling
```

**Screenshot:**
`![Rolling Update and Rollback](./screenshots/08-rolling-update-and-rollback.png)`

---

## Task 9: Real-World Troubleshooting Scenarios Lab

Resolve a broken image rollout and selector mismatch.

**Commands:**
```bash
cd troubleshooting/
kubectl apply -f broken-image.yaml
kubectl rollout status deployment/yatri-backend --timeout=30s
kubectl rollout undo deployment/yatri-backend
# Attempt selector-mismatch and fix labels
```

**Screenshot:**
`![Troubleshooting Drills](./screenshots/09-troubleshooting-drills.png)`

---

## Task 10: Theoretical & Architectural Conceptual Writeup

### 1. The 4 Ports Clarified
- **`containerPort`**: Port opened inside the application container process (informational in PodSpec).
- **`targetPort`**: Port on the backend pod where the Kubernetes Service routes incoming traffic.
- **`port`**: Port exposed internally by the Kubernetes Service (ClusterIP).
- **`nodePort`**: Static high port (30000–32767) exposed across every worker node's external IP.

### 2. Labels vs. Selectors
- **Labels**: Key-value pairs attached to objects (e.g., `app: nginx`, `env: prod`) for metadata identification.
- **Selectors**: Query filters used by controllers (Deployments, Services) to group and route to matching labelled pods.

### 3. The 4 Deployment Strategies
- **RollingUpdate**: Progressively replaces old pods with new pods; zero downtime.
- **Recreate**: Kills all v1 pods before starting any v2 pods; causes brief downtime, but avoids version conflicts.
- **Blue-Green**: Deploys two complete environments (Blue=Live, Green=New); cutover and rollback happen instantly via service selector flip. Requires 2x compute capacity.
- **Canary**: Deploys a small fraction of v2 pods (e.g., 10%) alongside v1 stable pods to validate real-world production metrics prior to full rollout.

### 4. `maxSurge` vs. `maxUnavailable` Math
- For `replicas: 4`, `maxSurge: 1`, `maxUnavailable: 0`:
  - Max allowed pods during rollout: $4 + 1 = 5$.
  - Min available pods: $4 - 0 = 4$ (Guarantees 100% service capacity throughout rollout).

### 5. Resource Requests vs. Limits & Units
- **Requests**: Guaranteed minimum CPU/memory allocated by the scheduler to place the pod on a node.
- **Limits**: Maximum ceiling enforced by Linux cgroups. CPU throttling occurs if CPU limit is exceeded; container is OOM-killed if memory limit is exceeded.
- **Units**: 1 GB = $10^9$ bytes (decimal, SI); 1 GiB = $2^{30}$ bytes = $1,073,741,824$ bytes (binary, IEC). Kubernetes uses mebibytes (`Mi`) and gibibytes (`Gi`).

---

## Task 11: Blue-Green Deployment Execution & Instant Selector Cutover

Deploy Blue/Green deployments side-by-side and flip traffic.

**Commands:**
```bash
cd 02-blue-green/
kubectl apply -f deployment-blue.yaml
kubectl apply -f deployment-green.yaml
kubectl apply -f service-blue.yaml
# Flip to green
kubectl apply -f service-green.yaml
```

**Screenshot:**
`![Blue-Green Cutover](./screenshots/11-blue-green-cutover.png)`

---

## Task 12: Canary Deployment Execution & Pod-Ratio Traffic Splitting

Deploy a 90/10 Canary traffic split.

**Commands:**
```bash
cd 03-canary/
kubectl apply -f deployment-stable.yaml
kubectl apply -f service.yaml
kubectl apply -f deployment-canary.yaml
# Run curl loop to test traffic distribution
```

**Screenshot:**
`![Canary Traffic Split](./screenshots/12-canary-traffic-split.png)`

---

## Task 13: Recreate Deployment Execution & Downtime Outage Demonstration

Demonstrate Recreate downtime outage.

**Commands:**
```bash
cd 04-recreate/
kubectl apply -f deployment-v1.yaml
kubectl apply -f service.yaml
kubectl apply -f deployment-v2.yaml
# Run continuous curl loop to capture outage
```

**Screenshot:**
`![Recreate Downtime Outage](./screenshots/13-recreate-downtime-outage.png)`