# 01 - Kubernetes Volumes Guide

## Overview

In Kubernetes, container filesystems are **ephemeral** by default. When a container crashes, terminates, or gets rescheduled, any changes made to its filesystem are permanently lost. Furthermore, containers running together in a Pod cannot share files without an external storage mechanism.

Kubernetes solves this with **Volumes**, providing persistent, shared, and lifecycle-managed storage.

---

## 1. Volume Types & Comparison Matrix

| Storage Concept | Scope / Lifetime | Shared Between Pods? | Persistence Across Pod Restarts | Use Cases |
| :--- | :--- | :--- | :--- | :--- |
| **emptyDir** | Pod lifetime | Yes (within same Pod) | Deleted on Pod removal | Caching, temp scratch space, log sharing between containers |
| **hostPath** | Node lifetime | Only if on same Node | Survives Pod restart on same Node | Node logging (`/var/log`), Docker daemon socket, local testing |
| **PersistentVolume (PV)** | Cluster lifecycle | Depends on AccessMode | Independent of Pod lifecycle | Databases, stateful apps, long-term asset storage |
| **PersistentVolumeClaim (PVC)** | Namespace lifecycle | Bound 1:1 to PV | Claims PV capacity | Developer request for storage without needing infra details |
| **StorageClass (SC)** | Cluster-wide definition | N/A (Provisioner) | Managed dynamically by Cloud/CSI | Automatic on-demand provisioning (AWS EBS, GCE PD, Minikube hostpath) |

---

## 2. Deep Dive: Core Concepts & Practical Examples

### 2.1 emptyDir

An `emptyDir` volume is created when a Pod is assigned to a Node, and exists as long as that Pod is running on that Node. All containers in the Pod can read and write the same files in the `emptyDir` volume.

#### Architecture:
```text
┌───────────────────────────────────────────────┐
│ Pod: emptydir-demo                            │
│                                               │
│  ┌─────────────────┐     ┌─────────────────┐  │
│  │ Container: app  │     │ Container: sidecar││
│  │ (writes log)    │     │ (reads log)     │  │
│  └────────┬────────┘     └────────┬────────┘  │
│           │                       │           │
│           ▼                       ▼           │
│     Mounted at /cache        Mounted at /logs │
│           │                       │           │
│           └───────────┬───────────┘           │
│                       ▼                       │
│             [ emptyDir Volume ]               │
│             (RAM or Node Temp Disk)           │
└───────────────────────────────────────────────┘
```

#### Practical Example (`emptydir-pod.yaml`):
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: emptydir-demo
spec:
  containers:
  - name: writer
    image: busybox:1.36
    command: ['sh', '-c', 'while true; do echo "$(date): Application healthy" >> /shared-data/app.log; sleep 5; done']
    volumeMounts:
    - name: cache-volume
      mountPath: /shared-data
  - name: reader
    image: busybox:1.36
    command: ['sh', '-c', 'sleep 2; tail -f /shared-data/app.log']
    volumeMounts:
    - name: cache-volume
      mountPath: /shared-data
  volumes:
  - name: cache-volume
    emptyDir: {}
```

#### Key Characteristics:
- Created empty on Pod startup.
- If a container inside the Pod crashes, the `emptyDir` data **is preserved**.
- If the Pod is evicted or deleted, the data in `emptyDir` is **permanently deleted**.

---

### 2.2 hostPath

A `hostPath` volume mounts a file or directory from the host node's filesystem directly into your Pod.

#### Practical Example (`hostpath-pod.yaml`):
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: hostpath-demo
spec:
  containers:
  - name: log-collector
    image: busybox:1.36
    command: ['sh', '-c', 'ls -la /host-var-log && sleep 3600']
    volumeMounts:
    - name: node-logs
      mountPath: /host-var-log
      readOnly: true
  volumes:
  - name: node-logs
    hostPath:
      path: /var/log
      type: Directory
```

#### Security & Operational Cautions:
- **Security risk**: Gives Pod access to underlying host filesystem (privilege escalation danger).
- **Node Affinity**: If Pod is rescheduled to a different Node, it cannot see the previous Node's `hostPath`.
- **Best Use Cases**: DaemonSets inspecting host logs or running system-level agents.

---

### 2.3 PersistentVolume (PV)

A **PersistentVolume (PV)** is a piece of storage in the cluster that has been provisioned by an administrator or dynamically provisioned using StorageClasses. It is a cluster-level resource independent of any individual Pod.

#### Lifecycle & Access Modes:
- **ReadWriteOnce (RWO)**: Volume can be mounted as read-write by a single Node.
- **ReadOnlyMany (ROX)**: Volume can be mounted read-only by many Nodes.
- **ReadWriteMany (RWX)**: Volume can be mounted as read-write by many Nodes (e.g., NFS, AWS EFS).
- **ReadWriteOncePod (RWOP)**: Mounted read-write by a single Pod (Kubernetes 1.22+).

#### Practical Example (`pv-static.yaml`):
```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: static-pv-5gi
  labels:
    type: local
spec:
  capacity:
    storage: 5Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: manual
  hostPath:
    path: "/mnt/data"
```

#### Reclaim Policies:
- **Retain**: Keep the PV and underlying data after PVC is deleted (manual reclamation).
- **Delete**: Automatically delete both the PV and external cloud volume (standard for cloud providers).
- **Recycle** (deprecated): Performs basic scrub (`rm -rf /thevolume/*`).

---

### 2.4 PersistentVolumeClaim (PVC)

A **PersistentVolumeClaim (PVC)** is a request for storage by a user/developer. PVCs consume PV resources just as Pods consume CPU and Memory resources.

#### Practical Example (`pvc-static.yaml`):
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-app-pvc
spec:
  storageClassName: manual
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 2Gi
```

#### Mounting PVC into a Pod (`pod-with-pvc.yaml`):
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app-with-pvc
spec:
  containers:
  - name: web-server
    image: nginx:alpine
    volumeMounts:
    - name: storage
      mountPath: /usr/share/nginx/html
  volumes:
  - name: storage
    persistentVolumeClaim:
      claimName: my-app-pvc
```

#### Binding Process:
The Kubernetes control plane actively searches for a PV that satisfies the PVC's requirements:
1. `accessModes` must match or include what the PVC requests.
2. `capacity` of PV must be greater than or equal to PVC request.
3. `storageClassName` must match.
Once matched, the PVC enters the `Bound` status.

---

### 2.5 StorageClass

A **StorageClass** provides a way for administrators to describe the "classes" of storage they offer (e.g., SSD vs HDD, backup policies, replication levels).

#### StorageClass Parameters:
- `provisioner`: Determines what CSI (Container Storage Interface) driver or volume plugin is used.
- `reclaimPolicy`: `Delete` or `Retain`.
- `volumeBindingMode`:
  - `Immediate`: PV is provisioned as soon as PVC is created.
  - `WaitForFirstConsumer`: Delay provisioning until a Pod requesting the PVC is scheduled to a Node (essential for topology/AZ constraints).

#### Practical Example (`storageclass.yaml`):
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-ssd
provisioner: kubernetes.io/no-provisioner # Or ebs.csi.aws.com / k8s.io/minikube-hostpath
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
reclaimPolicy: Delete
```

---

### 2.6 Dynamic Provisioning

Dynamic provisioning eliminates the need for cluster administrators to pre-provision storage manually. Instead, when a PVC requests a `StorageClass`, the storage provisioner automatically creates the physical disk in the cloud/cluster, creates the PV object, and binds it to the PVC.

#### Workflow Diagram:
```text
 Developer creates PVC
         │
         ▼
 [ PersistentVolumeClaim ]
   (requests 10Gi, storageClass: standard)
         │
         ▼
 [ Dynamic Provisioner / CSI Plugin ]
   (k8s.io/minikube-hostpath, ebs.csi.aws.com)
         │
         ├─► Creates physical block storage / host dir
         ▼
 [ PersistentVolume (auto-created) ]
         │
         ▼
 PVC is automatically BOUND to PV
         │
         ▼
 Pod mounts PVC and starts writing persistent data
```

#### Practical Example (`dynamic-pvc.yaml`):
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: dynamic-storage-claim
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: standard # Uses default cluster provisioner (e.g., minikube)
  resources:
    requests:
      storage: 1Gi
```

---

## 3. Hands-On Verification Commands

```bash
# 1. View Available Storage Classes
kubectl get storageclass
kubectl get sc

# 2. View Persistent Volumes and Claims
kubectl get pv
kubectl get pvc

# 3. Inspect Binding Details
kubectl describe pvc <claim-name>
kubectl describe pv <volume-name>

# 4. Check PVC status in Pod
kubectl describe pod <pod-name>
```

---

## Summary

- **`emptyDir`**: Temporary, fast, multi-container sharing; dies with Pod.
- **`hostPath`**: Mounts node path; useful for host monitoring and node agents.
- **`PV` & `PVC`**: Separates infrastructure provisioning (PV) from application consumption (PVC).
- **`StorageClass`**: Enables dynamic provisioning so developers get storage automatically on-demand.
