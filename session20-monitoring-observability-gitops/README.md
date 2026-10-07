# Session 20: Monitoring, Observability & GitOps — Master Guide

## Overview

This session covers two fundamental pillars of modern cloud-native operations:
1. **Monitoring & Observability** — Understanding system health through metrics (Prometheus), dashboards (Grafana), and structured insights.
2. **GitOps** — Using Git as the single source of truth to drive declarative Kubernetes deployments via ArgoCD.

---

## 1. Monitoring vs Observability

| Dimension | Monitoring | Observability |
| :--- | :--- | :--- |
| **Nature** | Reactive — alerts on known failure modes | Proactive — enables exploration of unknown system behavior |
| **Data Used** | Pre-defined metrics and alerts | Metrics + Logs + Distributed Traces |
| **Question Answered** | "Is the system down?" | "Why is the system misbehaving?" |
| **Tool Examples** | Nagios, Zabbix, Uptime Robot | Prometheus + Grafana + Jaeger + ELK Stack |

---

## 2. The Three Pillars of Observability

```text
                   ┌─────────────────────────────────────────────┐
                   │         OBSERVABILITY                        │
                   │                                             │
                   │  ┌─────────────┐  ┌───────────┐  ┌───────┐  │
                   │  │  METRICS    │  │   LOGS    │  │TRACES │  │
                   │  │             │  │           │  │       │  │
                   │  │ Numbers     │  │ Events    │  │Request│  │
                   │  │ over time   │  │ (text)    │  │ path  │  │
                   │  │             │  │           │  │       │  │
                   │  │ Prometheus  │  │ Loki /    │  │Jaeger │  │
                   │  │ Grafana     │  │ ELK Stack │  │Zipkin │  │
                   │  └─────────────┘  └───────────┘  └───────┘  │
                   └─────────────────────────────────────────────┘
```

### 2.1 Metrics
- **What they are**: Numerical measurements captured at specific time intervals (time-series data).
- **Examples**: `http_requests_total`, `process_cpu_seconds_total`, `node_memory_available_bytes`
- **Tool**: **Prometheus** scrapes and stores time-series metrics from application `/metrics` endpoints.

### 2.2 Logs
- **What they are**: Timestamped text records of discrete events emitted by an application or system.
- **Examples**: `[2026-10-07 23:00:00] ERROR: Database connection timeout`, HTTP access logs.
- **Tool**: **Loki** (log aggregation by Grafana Labs), **Elasticsearch** (ELK Stack).

### 2.3 Traces
- **What they are**: A distributed trace records the end-to-end journey of a single request as it traverses multiple microservices.
- **Vocabulary**: A trace consists of multiple **spans**, each representing one operation (HTTP call, DB query, cache lookup).
- **Tool**: **Jaeger**, **Zipkin**, **Tempo**.

---

## 3. Prometheus — Metrics Architecture

```text
                     ┌──────────────────────────────────────┐
                     │           Prometheus Server           │
                     │                                      │
                     │   ┌────────────────────────────────┐  │
                     │   │         Time-Series DB         │  │
                     │   │  (TSDB — stores all metrics)   │  │
                     │   └─────────────┬──────────────────┘  │
                     │                 │                      │
                     │          PromQL Query Engine           │
                     └──────────────────────────────────────┘
                              │                │
              ┌───────────────┘                └────────────────────┐
              ▼                                                     ▼
  Scrape /metrics endpoint                             Alertmanager
  (HTTP GET every 15s)                             (Email, Slack, PagerDuty)
              │
  ┌───────────┴──────────────────┐
  │ Application 1 (port 8080)    │
  │ Application 2 (port 9100)    │
  │ Node Exporter (host metrics) │
  └──────────────────────────────┘
```

### Key PromQL Queries:
```promql
# Is each target reachable?
up

# Total HTTP requests
http_requests_total

# Aggregation: total requests across all instances
sum(http_requests_total)

# Rate of requests over last 5 minutes
rate(http_requests_total[5m])

# CPU usage percentage
100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
```

---

## 4. Grafana — Dashboard Visualization

Grafana connects to Prometheus (and other data sources) via its **Data Sources** configuration and renders metrics as:
- **Time Series panels** (line and bar charts)
- **Gauge and Stat panels** (current value big text)
- **Table panels** (tabular raw output)
- **Heatmap panels** (latency distributions)

### Docker Compose Setup:
```yaml
services:
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      GF_SECURITY_ADMIN_PASSWORD: admin
    depends_on:
      - prometheus
```

Access Grafana at `http://localhost:3000` → Login: `admin`/`admin` → Add Prometheus data source (`http://prometheus:9090`).

---

## 5. GitOps Principles

GitOps applies Git workflow disciplines to operational infrastructure:

1. **Declarative**: The entire system is described declaratively in YAML configuration files.
2. **Versioned & Immutable**: Git is the single source of truth; all changes are tracked with commit history.
3. **Pulled Automatically**: Approved changes from Git are automatically applied to the cluster without manual `kubectl apply`.
4. **Continuously Reconciled**: Software agents continuously compare the desired state (Git) vs actual state (Kubernetes) and reconcile any drift.

---

## 6. ArgoCD — GitOps Reconciliation Engine

```text
            Developer
                |
                | git push
                v
           Git Repository
           (YAML manifests)
                |
                | Polls every 3 minutes (or webhook)
                v
         ┌─────────────────────┐
         │       ArgoCD        │
         │  Reconciliation     │
         │  Loop               │
         └──────────┬──────────┘
                    |
        ┌───────────┴───────────┐
        | Desired State (Git)   |
        | != Actual State (k8s) |
        └───────────┬───────────┘
                    |
                    v
            kubectl apply
                    |
                    v
            Kubernetes Cluster
            (now matches Git)
```

### ArgoCD Key Features:
- **Automated Sync**: Automatically applies Git changes to the cluster.
- **Self-Healing**: Automatically reverts `kubectl` manual changes back to Git state.
- **Prune**: Deletes Kubernetes resources when removed from Git.
- **Web UI**: Visual dashboard showing Application health and sync status.

---

## 7. Mini Project — Complete Deliverables

Located in `08-mini-project/`:

### Resources Applied:
```bash
# 1. Install ArgoCD
kubectl create namespace argocd
kubectl apply -n argocd --server-side --force-conflicts \
  -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# 2. Wait for ArgoCD pods
kubectl get pods -n argocd -w

# 3. Apply the ArgoCD Application
kubectl apply -f app/argocd-application.yaml

# 4. Verify sync
kubectl get applications -n argocd
kubectl get all -n session20

# 5. GitOps demo — scale via git commit
# Edit app/deployment.yaml: replicas: 2 → 3, commit & push

# 6. Self-healing demo
kubectl scale deployment session20-mini -n session20 --replicas=1
# ArgoCD reconciles back to Git state (replicas: 3)

# 7. Cleanup
kubectl delete -f app/argocd-application.yaml
```

### Viva Answers:
1. **Monitoring vs Observability**: Monitoring checks known metrics; Observability explores unknown causes.
2. **Metrics vs Logs vs Traces**: Numbers / Text events / Request paths.
3. **Prometheus**: Open-source metrics scraper and time-series database.
4. **Grafana**: Visualization layer querying Prometheus for dashboards and alerts.
5. **GitOps**: Operational model where Git is the single source of truth for cluster state.
6. **Git as Source of Truth**: All desired infrastructure state is committed and versioned in Git.
7. **ArgoCD**: Continuously reconciles live cluster state with desired state stored in Git.
8. **Desired State**: What the YAML files in Git describe the system should look like.
9. **Actual State**: What is currently running in the Kubernetes cluster.
10. **Reconciliation**: The automatic process of applying differences between desired and actual state.
11. **Self-Healing**: ArgoCD reverts unauthorized manual kubectl changes back to Git definition.
12. **Replicas 2→3 in Git**: ArgoCD detects the diff within 3 minutes → runs `kubectl scale` → cluster reaches 3 replicas.
