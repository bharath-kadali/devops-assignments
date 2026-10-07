# 08 - Session 20 Mini Project: GitOps with ArgoCD

## Overview

A complete GitOps mini-project demonstrating:

```text
Git → ArgoCD → Kubernetes → Application
```

ArgoCD continuously reconciles the cluster state against the desired state in Git.

---

## Architecture

```text
              Developer
                  |
                  | git push
                  v
            Git Repository
            (bharath-kadali/devops-assignments)
                  |
            session20-monitoring-observability-gitops/08-mini-project/app/
                  |
                  | Polls every 3 minutes
                  v
           ┌─────────────────────┐
           │       ArgoCD        │
           │   namespace: argocd │
           │   (Reconciler)      │
           └──────────┬──────────┘
                      |
                      v
               Kubernetes
              namespace: session20
                      |
          ┌───────────┴───────────┐
          |                       |
      Deployment              Service
      (2 replicas)          (ClusterIP:80)
          |
        Pods (nginx:1.27-alpine)
```

---

## Resources in This Project

| File | Kind | Purpose |
|:-----|:-----|:--------|
| `app/namespace.yaml` | Namespace | Creates `session20` namespace |
| `app/deployment.yaml` | Deployment | 2 nginx replicas |
| `app/service.yaml` | Service | ClusterIP exposing port 80 |
| `app/argocd-application.yaml` | Application | ArgoCD Application object (applied once) |

---

## Step 1 — Install ArgoCD

```bash
kubectl create namespace argocd

kubectl apply -n argocd --server-side --force-conflicts \
  -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

Wait for all pods to be `Running`:

```bash
kubectl get pods -n argocd -w
```

**Live Output:**

```text
NAME                                                READY   STATUS    RESTARTS   AGE
argocd-application-controller-0                     1/1     Running   0          3m12s
argocd-applicationset-controller-76fd8cdd4f-zdvjp   1/1     Running   0          3m15s
argocd-dex-server-66c78cf887-kcz5r                  1/1     Running   0          3m15s
argocd-notifications-controller-7fb9868fd6-qncrw    1/1     Running   0          3m15s
argocd-redis-bdbdffcb4-s4nlj                        1/1     Running   0          3m15s
argocd-repo-server-d89c7967d-mnddd                  1/1     Running   0          3m13s
argocd-server-776b7cdd4d-bjqzm                      1/1     Running   0          3m13s
```

---

## Step 2 — Apply the ArgoCD Application

```bash
kubectl apply -f app/argocd-application.yaml
```

**Output:**

```text
application.argoproj.io/session20-mini created
```

---

## Step 3 — Verify Sync & Deployment

```bash
kubectl get applications -n argocd
kubectl get all -n session20
```

**Live Output:**

```text
NAME             SYNC STATUS   HEALTH STATUS
session20-mini   Synced        Healthy

NAME                                  READY   STATUS    RESTARTS   AGE
pod/session20-mini-68946db7dd-x4m8j   1/1     Running   0          11m
pod/session20-mini-68946db7dd-xsxvn   1/1     Running   0          11m

NAME                     TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE
service/session20-mini   ClusterIP   10.110.229.54   <none>        80/TCP    11m

NAME                             READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/session20-mini   2/2     2            2           11m

NAME                                        DESIRED   CURRENT   READY   AGE
replicaset.apps/session20-mini-68946db7dd   2         2         2       11m
```

---

## Step 4 — GitOps in Action: Scale via Git Commit

Change `replicas: 2` → `replicas: 3` in `app/deployment.yaml`, then:

```bash
git add app/deployment.yaml
git commit -m "Scale application to three replicas"
git push
```

Watch ArgoCD sync:

```bash
kubectl get deployment -n session20 -w
```

Expected result (within ~3 minutes):

```text
NAME             READY   UP-TO-DATE   AVAILABLE
session20-mini   3/3     3            3
```

---

## Step 5 — Demonstrate Self-Healing

ArgoCD's `selfHeal: true` means any manual change is reconciled back to Git state.

```bash
# Manual scale down (anti-GitOps)
kubectl scale deployment session20-mini -n session20 --replicas=1
```

Because Git still says `replicas: 2`, ArgoCD reconciles the cluster back to 2 replicas.

This demonstrates:

```text
Git       = desired state
Kubernetes = actual state
ArgoCD    = reconciler
```

---

## Cleanup

```bash
kubectl delete -f app/argocd-application.yaml
kubectl delete namespace session20
kubectl delete namespace argocd
```

---

## Viva Answer Key

1. **Monitoring vs Observability** — Monitoring alerts on known thresholds; Observability explains unknown system behavior via metrics + logs + traces.
2. **Metrics vs Logs vs Traces** — Numbers over time / Text events / Request paths across services.
3. **Prometheus** — Open-source metrics scraper and time-series database; exposes PromQL.
4. **Grafana** — Dashboard platform that visualizes data from Prometheus and other sources.
5. **GitOps** — Operational model where Git is the single source of truth for cluster state.
6. **Git as source of truth** — All infrastructure YAML is versioned in Git; no untracked kubectl changes.
7. **ArgoCD** — Continuously compares Git desired state against cluster actual state, applies differences.
8. **Desired State** — What the YAML in Git describes the system should look like.
9. **Actual State** — What is currently running in the Kubernetes cluster right now.
10. **Reconciliation** — Automatic process of applying differences to reach desired state.
11. **Self-Healing** — ArgoCD reverts manual kubectl changes back to Git definition automatically.
12. **Replicas 2→3 in Git** — ArgoCD detects the diff within 3 minutes, runs scale, cluster has 3 pods.
