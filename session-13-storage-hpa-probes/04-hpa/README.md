# 04 - Kubernetes Horizontal Pod Autoscaler (HPA) Hands-on Lab

## Overview

The **Horizontal Pod Autoscaler (HPA)** automatically adjusts the number of Pod replicas in a deployment or replica set based on observed CPU utilization, memory, or custom metrics.

---

## Architecture Flow

```text
       [ Traffic Spike / Load ]
                   │
                   ▼
       [ Application Pods (hpa-demo) ]
                   │
                   ▼ (CPU Usage rises > 50%)
          [ Metrics Server ]
                   │
                   ▼ (Resource Metrics API)
        [ HPA Controller (hpa-demo) ]
                   │
                   ▼ (Scales Deployment)
    [ Deployment: hpa-demo (1 -> 2 -> ... Pods) ]
```

---

## Step 1: Deploy Application & Service

### Manifest: `deployment.yaml`
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hpa-demo
spec:
  replicas: 1
  selector:
    matchLabels:
      app: hpa-demo
  template:
    metadata:
      labels:
        app: hpa-demo
    spec:
      containers:
      - name: nginx
        image: nginx:1.25
        resources:
          requests:
            cpu: 100m
            memory: 64Mi
          limits:
            cpu: 200m
            memory: 128Mi
```

### Manifest: `service.yaml`
```yaml
apiVersion: v1
kind: Service
metadata:
  name: hpa-demo-service
spec:
  selector:
    app: hpa-demo
  ports:
  - port: 80
    targetPort: 80
  type: ClusterIP
```

Apply commands:
```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

Output:
```text
deployment.apps/hpa-demo created
service/hpa-demo-service created
```

---

## Step 2: Configure HPA

### Manifest: `hpa.yaml`
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: hpa-demo
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: hpa-demo
  minReplicas: 1
  maxReplicas: 5
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50
```

Apply HPA:
```bash
kubectl apply -f hpa.yaml
```

---

## Step 3: Verify HPA Initial State

```bash
kubectl get hpa
kubectl get pods -l app=hpa-demo
```

Live Terminal Output:
```text
NAME       REFERENCE             TARGETS       MINPODS   MAXPODS   REPLICAS   AGE
hpa-demo   Deployment/hpa-demo   cpu: 0%/50%   1         5         1          18d

NAME                        READY   STATUS    RESTARTS   AGE
hpa-demo-5d6676989b-vmwr2   1/1     Running   1          15d
```

---

## Step 4: Deploy Load Generator & Increase Application Load

Launch a busybox pod generating heavy concurrent HTTP requests against `hpa-demo-service`:

```bash
kubectl run load-generator --image=busybox:1.36 --restart=Never -- /bin/sh -c "while true; do wget -q -O- http://hpa-demo-service > /dev/null; done"
```

Increase concurrency with background workers:
```bash
kubectl exec load-generator -- /bin/sh -c "(while true; do wget -q -O- http://hpa-demo-service > /dev/null; done &); (while true; do wget -q -O- http://hpa-demo-service > /dev/null; done &); (while true; do wget -q -O- http://hpa-demo-service > /dev/null; done &)"
```

---

## Step 5: Observe CPU Utilization & Pod Scaling

### Checking top pods:
```bash
kubectl top pods -l app=hpa-demo
```
Output:
```text
NAME                        CPU(cores)   MEMORY(bytes)   
hpa-demo-5d6676989b-vmwr2   69m          14Mi            
```

### Checking HPA reaction:
```bash
kubectl get hpa
```
Output:
```text
NAME       REFERENCE             TARGETS        MINPODS   MAXPODS   REPLICAS   AGE
hpa-demo   Deployment/hpa-demo   cpu: 69%/50%   1         5         2          18d
```

### Checking scaled Pods:
```bash
kubectl get pods -l app=hpa-demo
```
Output:
```text
NAME                        READY   STATUS    RESTARTS   AGE
hpa-demo-5d6676989b-ttpnw   1/1     Running   0          25s
hpa-demo-5d6676989b-vmwr2   1/1     Running   1          15d
```

---

## Step 6: Detailed HPA Inspection (`kubectl describe hpa`)

```bash
kubectl describe hpa hpa-demo
```

Output:
```text
Name:                                                  hpa-demo
Namespace:                                             default
Reference:                                             Deployment/hpa-demo
Metrics:                                               ( current / target )
  resource cpu on pods  (as a percentage of request):  69% (69m) / 50%
Min replicas:                                          1
Max replicas:                                          5
Deployment pods:                                       2 current / 2 desired
Conditions:
  Type            Status  Reason              Message
  ----            ------  ------              -------
  AbleToScale     True    ReadyForNewScale    recommended size matches current size
  ScalingActive   True    ValidMetricFound    the HPA was able to successfully calculate a replica count from cpu resource utilization (percentage of request)
  ScalingLimited  False   DesiredWithinRange  the desired count is within the acceptable range
Events:
  Type    Reason             Age   From                       Message
  ----    ------             ----  ----                       -------
  Normal  SuccessfulRescale  32s   horizontal-pod-autoscaler  New size: 2; reason: cpu resource utilization (percentage of request) above target
```

---

## Step 7: Scale-Down Verification

Stop and remove the load generator:
```bash
kubectl delete pod load-generator
```

After the stabilization window (default cooldown is 5 minutes for scale down):
```bash
kubectl get hpa
```
Output:
```text
NAME       REFERENCE             TARGETS       MINPODS   MAXPODS   REPLICAS   AGE
hpa-demo   Deployment/hpa-demo   cpu: 0%/50%   1         5         1          18d
```

---

## Summary of Essential Commands

- `kubectl get hpa`: Displays current metrics and replica counts.
- `kubectl get pods`: Shows individual running Pods and replica count changes.
- `kubectl top pods`: Reports live CPU (millicores) and Memory consumption per Pod.
- `kubectl describe hpa <name>`: Provides events detailing why and when scaling decisions occurred.
