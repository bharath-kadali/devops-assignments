# Session 14: Kubernetes Troubleshooting Master Guide

## Overview

Kubernetes applications operate in a distributed, declarative environment. When failures happen, engineers must systematically diagnose rather than guess.

---

## Task 1: Essential Kubernetes Troubleshooting Commands

### 1. `kubectl get`
Provides a high-level overview of resources and their current high-level state.
```bash
# Basic pod listing
kubectl get pods

# List across all namespaces
kubectl get pods -A

# Watch pods change state in real time
kubectl get pods -w
```

### 2. `kubectl get -o wide`
Displays extended operational information including Node assignment, Pod IP address, readiness gates, and nominated node.
```bash
kubectl get pods -o wide
kubectl get nodes -o wide
```
*Key insight*: Essential for debugging scheduling issues, node affinity failures, and verifying Pod-to-Node placement.

### 3. `kubectl describe`
Inspects complete API metadata, controller specifications, container states, volumes, and most critically: **recent Kubernetes Events**.
```bash
kubectl describe pod <pod-name>
kubectl describe node <node-name>
kubectl describe svc <service-name>
```
*Key insight*: 90% of scheduling, image pull, and probe failures are revealed in the `Events:` section at the bottom of the describe output.

### 4. `kubectl logs`
Streams container stdout and stderr to view application-level errors, stack traces, and unhandled exceptions.
```bash
# Current container logs
kubectl logs <pod-name>

# View logs from a previous crashed container instance (crucial for CrashLoopBackOff!)
kubectl logs <pod-name> --previous

# Multi-container pod
kubectl logs <pod-name> -c <container-name>

# Stream logs live
kubectl logs -f <pod-name>
```

### 5. `kubectl exec`
Executes an interactive shell or diagnostics command directly inside a running container.
```bash
# Interactive shell session
kubectl exec -it <pod-name> -- /bin/sh

# Non-interactive diagnostics command
kubectl exec <pod-name> -- nslookup kubernetes.default
kubectl exec <pod-name> -- env
```

### 6. `kubectl events`
Displays chronologically sorted cluster events across all objects.
```bash
kubectl events --sort-by='.metadata.creationTimestamp'
kubectl events -n default
```

### 7. `kubectl explain`
Interactive documentation for any Kubernetes API resource schema, fields, and nesting syntax.
```bash
# Explain pod spec
kubectl explain pod.spec

# Deep-dive into probe syntax
kubectl explain pod.spec.containers.livenessProbe
```

### 8. `kubectl top`
Displays real-time CPU and Memory resource consumption for Nodes and Pods (requires Metrics Server).
```bash
kubectl top nodes
kubectl top pods
kubectl top pods --sort-by=cpu
kubectl top pods --sort-by=memory
```

---

## Task 2: Troubleshooting Common Kubernetes Issues

Every issue follows the standard 6-step troubleshooting methodology:
1. **Identify the Problem** (Observation)
2. **Investigate** (Inspection & Diagnostics)
3. **Find the Root Cause** (Correlation & Evidence)
4. **Fix It** (Manifest / Infrastructure remediation)
5. **Verify the Solution** (Post-fix health check)
6. **Document the Process** (Post-incident RCA)

---

### Issue 1: CrashLoopBackOff
1. **Identify:** Pod status oscillates between `Running`, `Error`, and `CrashLoopBackOff` with a mounting `RESTARTS` count.
2. **Investigate:**
   ```bash
   kubectl logs <pod-name> --previous
   kubectl describe pod <pod-name>
   ```
3. **Root Cause:** Application runtime error, missing required environment variable, invalid entrypoint/command, or configuration file not found.
4. **Fix:** Correct the missing configuration, fix application code, or adjust the container `command` / `args` in deployment manifest.
5. **Verify:** Apply updated manifest and observe `kubectl get pods` remains `Running` without restarts.
6. **Document:** Recorded failing exit code (e.g., exit code 1 or 137 OOM) and applied the appropriate environment parameter or code fix.

---

### Issue 2: ImagePullBackOff
1. **Identify:** Pod status displays `ImagePullBackOff` or `ErrImagePull`.
2. **Investigate:**
   ```bash
   kubectl describe pod <pod-name>
   ```
3. **Root Cause:** Non-existent image tag (e.g., `nginx:typo999`), typo in image repository path, or cluster lacks access credentials (`imagePullSecrets`) for private registries.
4. **Fix:** Update image tag to a valid image in manifest, or configure `imagePullSecrets` linked to a Docker registry secret.
5. **Verify:** `kubectl apply -f manifest.yaml` -> Pod pulls image successfully and transitions to `Running`.
6. **Document:** Verified image repository path in registry before deploying.

---

### Issue 3: ErrImagePull
1. **Identify:** Pod immediately shows `ErrImagePull` before entering exponential backoff (`ImagePullBackOff`).
2. **Investigate:** Look at the exact event message:
   ```bash
   kubectl describe pod <pod-name> | grep -A 5 Events:
   ```
3. **Root Cause:** DNS resolution failure to registry, network timeout between Node and registry, or 401 Unauthorized response from registry.
4. **Fix:** Verify node internet connectivity, check firewall rules, and configure correct registry auth token.
5. **Verify:** Run `kubectl get pod -w` and verify transition from `Pulling` to `Pulled` and `Created`.
6. **Document:** Ensure registry endpoint is routable from cluster nodes.

---

### Issue 4: Pending Pods
1. **Identify:** Pod status remains permanently stuck in `Pending`.
2. **Investigate:**
   ```bash
   kubectl describe pod <pod-name>
   ```
3. **Root Cause:**
   - **Insufficient Resources**: `0/1 nodes available: insufficient cpu/memory`.
   - **Taints & Tolerations**: Node has a taint that the Pod does not tolerate.
   - **Unbound PVC**: Pod references a PersistentVolumeClaim that is still `Pending`.
   - **NodeSelector / Affinity mismatch**: No nodes have matching labels.
4. **Fix:** Lower resource requests, add more cluster worker nodes, fix PVC binding, or correct `nodeSelector`.
5. **Verify:** Pod gets scheduled to a node and starts running (`kubectl get pod -o wide`).
6. **Document:** Document cluster capacity and right-size resource requests.

---

### Issue 5: ContainerCreating
1. **Identify:** Pod status is stuck in `ContainerCreating` for minutes.
2. **Investigate:**
   ```bash
   kubectl describe pod <pod-name>
   ```
3. **Root Cause:**
   - Failed volume attachment (`AttachVolume.Attach failed`).
   - CNI network plugin unable to allocate IP address.
   - ConfigMap or Secret referenced by volume or `envFrom` does not exist.
4. **Fix:** Create the missing ConfigMap/Secret or detach stuck volume on storage controller.
5. **Verify:** Volume attaches successfully, container initializes and transitions to `Running`.
6. **Document:** Ensure prerequisite secrets and storage provisions exist before triggering pod deployment.

---

### Issue 6: Service Connectivity Issues
1. **Identify:** Clients receive connection refused, HTTP 502/503, or timeout when calling the Service.
2. **Investigate:**
   ```bash
   kubectl get svc <service-name>
   kubectl describe svc <service-name>
   kubectl get endpoints <service-name>
   ```
3. **Root Cause:**
   - **Empty Endpoints**: Service selector does not match Pod labels.
   - **TargetPort Mismatch**: `targetPort` does not match the actual listening port of the container.
   - **Failed Readiness Probe**: Pod is running, but readiness probe is failing, so endpoint controller removes its IP.
4. **Fix:** Align `spec.selector` in Service YAML with `metadata.labels` in Pod template; ensure `targetPort` matches listening port; verify readiness probe endpoint returns 200 OK.
5. **Verify:** `kubectl get endpoints <service-name>` lists active Pod IPs; `curl <service-ip>:<port>` succeeds.
6. **Document:** Standardize label taxonomy across services and deployments.

---

### Issue 7: DNS Issues
1. **Identify:** Pod cannot resolve Service name (e.g., `curl http://backend-service` fails with `Could not resolve host`).
2. **Investigate:**
   ```bash
   # Test resolution from inside debug pod
   kubectl run dns-test --image=busybox:1.36 --rm -it --restart=Never -- nslookup kubernetes.default
   # Check CoreDNS health
   kubectl get pods -n kube-system -l k8s-app=kube-dns
   kubectl logs -n kube-system -l k8s-app=kube-dns
   ```
3. **Root Cause:** CoreDNS pods crashed/pending, upstream DNS forwarder timeout in Corefile, or Pod's `/etc/resolv.conf` has invalid nameserver IP.
4. **Fix:** Restart CoreDNS deployment, fix Corefile upstream DNS config, or check cluster network CNI connectivity.
5. **Verify:** `nslookup backend-service.default.svc.cluster.local` resolves to ClusterIP immediately.
6. **Document:** CoreDNS health check included in routine cluster monitoring.

---

### Issue 8: Pod Networking Issues
1. **Identify:** Pod cannot communicate with other Pods on different nodes or external gateways.
2. **Investigate:**
   ```bash
   # Ping pod IP directly from another pod
   kubectl exec -it <pod-a> -- ping <pod-b-ip>
   # Check NetworkPolicies
   kubectl get netpol -A
   # Check CNI pods
   kubectl get pods -n kube-system
   ```
3. **Root Cause:** Strict NetworkPolicy blocking ingress/egress traffic, CNI plugin crash/misconfiguration, or node iptables/IPVS rule corruption.
4. **Fix:** Create permissive NetworkPolicy rule or restart CNI daemonset agent on the node.
5. **Verify:** Bidirectional TCP connection established via `nc -zv <target-ip> <target-port>`.
6. **Document:** Audit and test all NetworkPolicies in staging before applying to production.

---

### Issue 9: Configuration Issues
1. **Identify:** Application boots but runs with incorrect flags, default fallback values, or fails to connect to database.
2. **Investigate:**
   ```bash
   # Inspect environment variables inside running container
   kubectl exec -it <pod-name> -- env
   # Check mounted volume config files
   kubectl exec -it <pod-name> -- cat /etc/config/app.properties
   ```
3. **Root Cause:** Stale ConfigMap data, missing Secret key in `secretKeyRef`, typo in environment variable key names, or failure to restart pods after updating immutable ConfigMaps.
4. **Fix:** Update ConfigMap/Secret and trigger rollout: `kubectl rollout restart deployment <deploy-name>`.
5. **Verify:** Container environment shows newly updated configuration parameters.
6. **Document:** Implement GitOps and automated rollout restarts on ConfigMap hash changes.

---

## Task 3: Mini Project - Hands-On Troubleshooting Scenario

### Scenario Setup
We deploy a broken application scenario with misconfigured image and service selector:
```bash
cd mini-project
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f broken-pod.yaml
```

### Problem Statement & Investigation
1. **Broken Pod Issue**:
   ```bash
   kubectl get pod project-broken-pod
   ```
   *Output*:
   ```text
   NAME                 READY   STATUS             RESTARTS   AGE
   project-broken-pod   0/1     ImagePullBackOff   0          45s
   ```
   *Investigation*:
   ```bash
   kubectl describe pod project-broken-pod
   ```
   *Event Log*: `Failed to pull image "nginx:999-not-found": rpc error: code = NotFound desc = failed to pull and unpack image`
   *Root Cause*: Image tag `999-not-found` does not exist on Docker Hub.
   *Fix*: Update image to `nginx:1.25-alpine` and re-apply.
   *Verification*: Status transitions to `1/1 Running`.

2. **Service Routing Issue**:
   ```bash
   kubectl get endpoints troubleshooting-service
   ```
   *Output*:
   ```text
   NAME                      ENDPOINTS
   troubleshooting-service   <none>
   ```
   *Root Cause*: Selector in `service.yaml` was mismatched (`wrong-app` instead of `troubleshooting-app`).
   *Fix*: Correct selector in `service.yaml` to `app: troubleshooting-app`.
   *Verification*:
   ```bash
   kubectl get endpoints troubleshooting-service
   NAME                      ENDPOINTS
   troubleshooting-service   10.244.0.51:80,10.244.0.52:80
   ```

---

## Deliverables Summary
- **Commands practiced**: `kubectl get`, `get -o wide`, `describe`, `logs`, `logs --previous`, `exec`, `events`, `explain`, `top`.
- **Common issues solved**: CrashLoopBackOff, ImagePullBackOff, ErrImagePull, Pending, ContainerCreating, Service selector mismatch, CoreDNS failure, CNI networking, ConfigMap mismatch.
- **Mini-project**: Resolved broken image and fixed service endpoint routing.