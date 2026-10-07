# Session 17: Complete CI/CD & DevSecOps Master Guide

## Overview

DevSecOps integrates security controls, vulnerability assessments, and compliance gates into every stage of the CI/CD pipeline—shifting security left rather than treating it as an afterthought.

---

## 1. Complete DevSecOps Pipeline Flow

```text
               ┌───────────────────────┐
               │ 1. Developer Pushes   │
               │    Code to GitHub     │
               └──────────┬────────────┘
                          │
                          ▼
               ┌───────────────────────┐
               │ 2. Build & Unit Test  │ (pytest, coverage analysis)
               └──────────┬────────────┘
                          │
                          ▼
               ┌───────────────────────┐
               │ 3. SAST Scan          │ (Static Application Security Testing - Bandit/CodeQL)
               └──────────┬────────────┘
                          │
                          ▼
               ┌───────────────────────┐
               │ 4. SCA Scan           │ (Software Composition Analysis - pip-audit/Safety)
               └──────────┬────────────┘
                          │
                          ▼
               ┌───────────────────────┐
               │ 5. Secret Scanning    │ (Gitleaks / TruffleHog credential leak audit)
               └──────────┬────────────┘
                          │
                          ▼
               ┌───────────────────────┐
               │ 6. Docker Build       │ (Build container image with unique Git SHA)
               └──────────┬────────────┘
                          │
                          ▼
               ┌───────────────────────┐
               │ 7. Container Image    │ (Trivy scanner for OS and library CVEs)
               │    Scan               │
               └──────────┬────────────┘
                          │
                          ▼
               ┌───────────────────────┐
               │ 8. Security Gate      │ (Halt pipeline if CRITICAL/HIGH CVEs exist)
               └──────────┬────────────┘
                          │ (passed)
                          ▼
               ┌───────────────────────┐
               │ 9. Push to Registry   │ (Push immutable image to Container Registry)
               └──────────┬────────────┘
                          │
                          ▼
               ┌───────────────────────┐
               │ 10. Deploy to K8s     │ (Rolling update Deployment & Service)
               └───────────────────────┘
```

---

## 2. Security Tooling Matrix

| Security Phase | Tool Used | What It Analyzes | Failure Threshold (Gate) |
| :--- | :--- | :--- | :--- |
| **Unit Testing** | `pytest` | Business logic, endpoints, status codes | Any failing test |
| **SAST** | `Bandit` / `CodeQL` | Source code vulnerabilities, insecure functions, hardcoded keys | High/Medium severity alerts |
| **SCA** | `pip-audit` | Python dependency vulnerabilities via PyPI advisory DB | Known unpatched vulnerabilities |
| **Secret Scanning**| `Gitleaks` | Committed API tokens, private keys, passwords | Any active secret detected |
| **Container Scanning** | `Trivy` | Base OS packages, outdated runtime dependencies | Vulnerabilities with severity `CRITICAL` |
| **Security Gates** | Custom exit codes | Aggregate score / severity count across all tools | Exits with non-zero exit code |

---

## 3. Demo Application Implementation (`session-17-devsecops/demo`)

### Application Architecture:
- **Backend**: Flask Python microservice (`app/app.py`)
- **Frontend**: Responsive UI (`app/templates/index.html`, `static/css/styles.css`)
- **Tests**: Comprehensive pytest test suite (`tests/test_app.py`)
- **Container**: Security-hardened Dockerfile with unprivileged user (`Dockerfile`)
- **Kubernetes Manifests**: `k8s/deployment.yaml` and `k8s/service.yaml`
- **Workflow**: Automated multi-stage GitHub Actions pipeline (`.github/workflows/devsecops.yml`)

---

## 4. GitHub Actions Workflow Configuration

Key workflow stages defined in `.github/workflows/devsecops.yml`:

```yaml
# 1. Unit Tests
- name: Run unit tests with coverage
  run: pytest --cov=app --cov-report=term-missing

# 2. SAST Analysis
- name: CodeQL SAST Analysis
  uses: github/codeql-action/analyze@v3

# 3. SCA Dependency Audit
- name: Scan dependencies with pip-audit
  run: pip-audit

# 4. Secret Scan
- name: Scan for secrets with Gitleaks
  uses: gitleaks/gitleaks-action@v2
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

# 5. Docker Build & Trivy Image Scan
- name: Build Docker image
  run: docker build -t devsecops-app:${{ github.sha }} .
- name: Scan image with Trivy
  run: trivy image --exit-code 1 --severity CRITICAL devsecops-app:${{ github.sha }}

# 6. Push to Registry & Deploy to Kubernetes
- name: Deploy to Kubernetes
  run: |
    sed -i "s|__IMAGE_TAG__|${{ github.sha }}|g" k8s/deployment.yaml
    kubectl apply -f k8s/deployment.yaml
    kubectl apply -f k8s/service.yaml
    kubectl rollout status deployment/session17-python --timeout=60s
```

---

## 5. Deliverables Verification

- [x] **Application Source Code**: `demo/app/`
- [x] **Dockerfile**: `demo/Dockerfile`
- [x] **GitHub Actions Workflow**: `demo/.github/workflows/devsecops.yml`
- [x] **Security Tools Configuration**: SAST, SCA, Secret Scanning, Container Image Scanning, Security Gates
- [x] **Kubernetes Manifests**: `demo/k8s/deployment.yaml`, `demo/k8s/service.yaml`
- [x] **README Documentation**: Fully documented pipeline architecture and security policy (`SECURITY.md`).
