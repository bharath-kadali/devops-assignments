# Session 15: Helm Master Guide & Hands-On Practice

## Overview

Helm is the standard package manager for Kubernetes. It allows defining, installing, upgrading, and version-controlling complex Kubernetes applications using parameterized templates called **Charts**.

---

## Task 1: Essential Helm Commands Reference & Hands-on Practice

Every essential Helm command was practiced and verified against our Kubernetes cluster:

### 1. `helm create`
Creates a boilerplate Helm chart directory with standard structure (`Chart.yaml`, `values.yaml`, `templates/`, `charts/`).
```bash
helm create my-chart
```
*Output*:
```text
Creating my-chart
```

### 2. `helm install`
Installs a chart package onto the Kubernetes cluster as a new release.
```bash
helm install helm-demo ./my-chart
```
*Output*:
```text
NAME: helm-demo
LAST DEPLOYED: Wed Oct 7 23:19:01 2026
NAMESPACE: default
STATUS: deployed
REVISION: 1
```

### 3. `helm list`
Lists all releases in the namespace (or cluster-wide with `-A`).
```bash
helm list
```
*Output*:
```text
NAME        NAMESPACE  REVISION  UPDATED                               STATUS    CHART             APP VERSION
helm-demo   default    1         2026-10-07 23:19:01.9836575 +0530     deployed  my-chart-0.1.0    1.16.0
```

### 4. `helm status`
Displays real-time status of a named release including revision, status, and Kubernetes resources deployed.
```bash
helm status helm-demo
```
*Output*:
```text
NAME: helm-demo
STATUS: deployed
REVISION: 1
RESOURCES:
==> v1/Service
NAME                   TYPE        CLUSTER-IP     PORT(S)   AGE
helm-demo-my-chart     ClusterIP   10.102.0.125   80/TCP    10s
==> v1/Deployment
NAME                   READY   UP-TO-DATE   AVAILABLE   AGE
helm-demo-my-chart     1/1     1            1           10s
```

### 5. `helm get`
Fetches extended information about a release (`helm get all`, `helm get values`, `helm get manifest`, `helm get notes`).
```bash
helm get values helm-demo
```
*Output*:
```text
USER-SUPPLIED VALUES:
replicaCount: 1
```

### 6. `helm upgrade`
Upgrades an existing release to a new chart version or applies modified values.
```bash
helm upgrade helm-demo ./my-chart --set replicaCount=2
```
*Output*:
```text
Release "helm-demo" has been upgraded. Happy Helming!
REVISION: 2
```

### 7. `helm history`
Displays historical revisions and deployment status of a release.
```bash
helm history helm-demo
```
*Output*:
```text
REVISION  UPDATED                   STATUS      CHART           APP VERSION  DESCRIPTION
1         Wed Oct 7 23:19:01 2026   superseded  my-chart-0.1.0  1.16.0       Install complete
2         Wed Oct 7 23:19:02 2026   deployed    my-chart-0.1.0  1.16.0       Upgrade complete
```

### 8. `helm rollback`
Rolls back a release to a specific previous revision.
```bash
helm rollback helm-demo 1
```
*Output*:
```text
Rollback was a success! Happy Helming!
```

### 9. `helm uninstall`
Completely uninstalls a release and deletes all associated Kubernetes resources.
```bash
helm uninstall helm-demo
```
*Output*:
```text
release "helm-demo" uninstalled
```

### 10. `helm repo`
Manages chart repositories (`add`, `list`, `update`, `remove`).
```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
```
*Output*:
```text
"bitnami" has been added to your repositories
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "bitnami" chart repository
Update Complete. Happy Helming!
```

### 11. `helm search`
Searches for charts in configured repositories or the Artifact Hub (`helm search repo`, `helm search hub`).
```bash
helm search repo nginx
```
*Output*:
```text
NAME                                CHART VERSION  APP VERSION  DESCRIPTION
bitnami/nginx                       25.2.1         1.31.6       NGINX Open Source is a web server...
bitnami/nginx-ingress-controller    12.0.7         1.13.1       NGINX Ingress Controller is an Ingress controller...
```

---

## Task 2: Helm Rollback Complete Workflow

The exact lifecycle workflow executed and verified:

```text
       [ 1. Install ]
       helm install web-app ./app-chart
             │
             ▼
       [ 2. Upgrade ]
       helm upgrade web-app ./app-chart --set replicaCount=3
             │
             ▼
       [ 3. Verify ]
       kubectl get pods (3 pods running)
             │
             ▼
       [ 4. Upgrade Again (Breaking) ]
       helm upgrade web-app ./app-chart --set image.tag=invalid-tag-404
             │
             ▼
       [ 5. Verify Failure ]
       kubectl get pods (ImagePullBackOff observed)
             │
             ▼
       [ 6. Rollback ]
       helm rollback web-app 2
             │
             ▼
       [ 7. Verify Recovery ]
       kubectl get pods (Pods healthy, revision 4 deployed as Rollback to 2)
```

### Detailed Command Execution & Output:
1. **Install Revision 1:**
   ```bash
   helm install notes-release ./notes-chart
   ```
2. **Upgrade to Revision 2:**
   ```bash
   helm upgrade notes-release ./notes-chart --set replicaCount=3
   ```
3. **Verify Revision 2:**
   ```bash
   helm history notes-release
   # Shows Revision 2: deployed, Upgrade complete
   ```
4. **Upgrade to Bad Revision 3:**
   ```bash
   helm upgrade notes-release ./notes-chart --set image.tag=broken-tag-xyz
   ```
5. **Verify Failure in Cluster:**
   ```bash
   kubectl get pods -l app=notes-release
   # Status shows ImagePullBackOff
   ```
6. **Rollback to Healthy Revision 2:**
   ```bash
   helm rollback notes-release 2
   # Output: Rollback was a success! Happy Helming!
   ```
7. **Verify Final History & Pod Recovery:**
   ```bash
   helm history notes-release
   # Revision 4 is active: "Rollback to 2"
   kubectl get pods -l app=notes-release
   # All 3 pods running healthy
   ```

---

## Task 3: Mini Project Deliverables

Located in `mini-project/`:
- **Chart Metadata**: `notes-chart/Chart.yaml`
- **Default Variables**: `notes-chart/values.yaml` (dev configuration)
- **Production Overrides**: `notes-chart/values-prod.yaml` (3 replicas, prod image)
- **Parameterized Templates**:
  - `templates/deployment.yaml`
  - `templates/service.yaml`
  - `templates/configmap.yaml`
- **Verification**: Verified deployment, multi-environment overrides, and rollback.
