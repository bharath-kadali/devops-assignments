# Session 12: Ingress, ConfigMaps & Secrets

**Author:** [Your Name]
**Course:** SST DevOps & Cloud [SWE]
**Session:** 12 - Ingress, ConfigMaps & Secrets
**Repository:** devops-heros / session-12-ingress-configmaps-secrets

---

## Task 1: Non-Sensitive Configuration Decoupling via ConfigMaps

**Commands:**
```bash
kubectl apply -f 01-configmap/app-config.yaml
kubectl describe configmap yatri-app-config
kubectl get configmap yatri-app-config -o jsonpath='{.data.ENVIRONMENT}'
```

**Screenshot:**
`![ConfigMap Outputs](./screenshots/01-configmap-output.png)`

---

## Task 2: ConfigMap Live Update & Pod Immobility Verification Drill

**Commands:**
```bash
kubectl patch configmap yatri-app-config --type merge -p '{"data":{"ENVIRONMENT":"staging"}}'
kubectl exec -it deploy/yatri-backend -- env | grep ENVIRONMENT
kubectl rollout restart deployment/yatri-backend
kubectl exec -it deploy/yatri-backend -- env | grep ENVIRONMENT
```

**Screenshot:**
`![ConfigMap Live Update](./screenshots/02-configmap-update.png)`

---

## Task 3: Sensitive Data Isolation via Kubernetes Secrets

**Commands:**
```bash
kubectl apply -f 02-secret/db-secret.yaml
kubectl describe secret yatri-db-secret
kubectl get secret yatri-db-secret -o jsonpath='{.data.POSTGRES_PASSWORD}' | base64 --decode
```

**Screenshot:**
`![Kubernetes Secret Validation](./screenshots/03-secret-validation.png)`

---

## Task 4: The Trailing Newline Secret Gotcha

**Commands:**
```bash
echo "secretpassword" | base64
echo -n "secretpassword" | base64
```

**Screenshot:**
`![Newline Gotcha Analysis](./screenshots/04-newline-gotcha.png)`

---

## Task 5: Enterprise Secret Management & Pipeline Integration Analysis

**Enterprise Secret Management Architecture:**
1. **The Vulnerability**: Hardcoded base64 secrets in Git represent a major security risk, lacking rotation or RBAC.
2. **External Secret Operators**: Tools like ESO or Vault Agent Injector synchronize secrets from external sources (AWS Secrets Manager/Azure Key Vault/HashiCorp Vault) into Kubernetes dynamically.
3. **CI/CD Integration**: Pipelines inject secrets at deploy-time using variables instead of storing them statically.

**Screenshot:**
`![Secret Management Operators](./screenshots/05-enterprise-secrets.png)`

---

## Task 6: Combined ConfigMap and Secret Pod Injection Architecture

**Commands:**
```bash
kubectl apply -f 04-full-demo/configmap.yaml
kubectl apply -f 04-full-demo/secret.yaml
kubectl apply -f 04-full-demo/backend.yaml
kubectl rollout status deployment/yatri-backend
kubectl exec -it deploy/yatri-backend -- env | grep -E "ENVIRONMENT|LOG_LEVEL|POSTGRES|DEFAULT_CURRENCY"
```

**Screenshot:**
`![Combined Injection Pod](./screenshots/06-combined-injection.png)`

---

## Task 7: Architectural Comparative Study — Ingress Resource vs. Ingress Controller

| Concept | Description |
| --- | --- |
| **Ingress Resource** | Declarative Kubernetes Layer 7 API specification (contains hostnames, paths, TLS certs). Does nothing by itself. |
| **Ingress Controller** | Active reverse proxy pod (NGINX, Traefik, HAProxy, Envoy) that runs a control loop, dynamically generates proxy configuration, and routes traffic. |

**Screenshot:**
`![Ingress Comparison](./screenshots/07-ingress-comparison.png)`

---

## Task 8: NGINX Ingress Controller Activation & Lifecycle Verification

**Commands:**
```bash
minikube addons enable ingress
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=120s
```

**Screenshot:**
`![Ingress Controller Enable](./screenshots/08-ingress-enable.png)`

---

## Task 9: Local DNS Resolution & System Hosts File Mapping

**Commands:**
```bash
MINIKUBE_IP=$(minikube ip)
echo "${MINIKUBE_IP}  yatri.local" | sudo tee -a /etc/hosts
```

**Screenshot:**
`![Local DNS Map](./screenshots/09-local-dns-mapping.png)`

---

## Task 10: Layer 7 Path-Based Routing Implementation

**Commands:**
```bash
kubectl apply -f 04-full-demo/ingress.yaml
kubectl describe ingress yatri-ingress
curl -s http://yatri.local/ | grep -i "<title>"
curl -s http://yatri.local/api/
```

**Screenshot:**
`![Path Routing Check](./screenshots/10-path-routing.png)`

---

## Task 11: Virtual Host-Based Routing (Subdomain Routing)

**Commands:**
```bash
curl -s -H "Host: portal.campus.local" http://${MINIKUBE_IP}/ | grep -i "<title>"
curl -s -H "Host: api.campus.local" http://${MINIKUBE_IP}/api/
```

**Screenshot:**
`![Subdomain Routing](./screenshots/11-subdomain-routing.png)`

---

## Task 12: Hybrid Ingress Routing Architecture

**Commands:**
```bash
kubectl apply -f 03-ingress/ingress-tls.yaml
kubectl get ingress campus-ingress-tls
kubectl describe ingress campus-ingress-tls
```

**Screenshot:**
`![Hybrid Routing Verification](./screenshots/12-hybrid-routing.png)`

---

## Task 13: Ingress TLS/HTTPS Termination & Secret Binding

**Commands:**
```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout tls.key -out tls.crt -subj "/CN=campus.local/O=CampusDevOps"
kubectl create secret tls campus-tls-cert --cert=tls.crt --key=tls.key
kubectl apply -f 03-ingress/ingress-tls.yaml
curl -k -v --resolve portal.campus.local:443:${INGRESS_IP} https://portal.campus.local/
```

**Screenshot:**
`![TLS Setup](./screenshots/13-tls-setup.png)`

---

## Task 14: End-to-End Multi-Tier Microservice Integration

**Commands:**
```bash
bash 04-full-demo/run-demo.sh
kubectl get configmap,secret,ingress,deploy,svc,pods -l app=yatri-app
bash 04-full-demo/cleanup.sh
```

**Screenshot:**
`![End To End Automation](./screenshots/14-end-to-end-demo.png)`
