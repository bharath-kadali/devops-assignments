# Session 16: CI/CD & GitHub Actions Master Guide

## Overview

Continuous Integration (CI) and Continuous Delivery/Deployment (CD) automate the building, testing, packaging, and shipping of code. GitHub Actions is the native workflow engine directly integrated with GitHub repositories.

---

## 1. CI vs CD

| Dimension | Continuous Integration (CI) | Continuous Delivery (CD) | Continuous Deployment (CD) |
| :--- | :--- | :--- | :--- |
| **Focus** | Code integration & verification | Deployment readiness | Automatic production release |
| **Trigger** | Every commit / Pull Request | Successful CI build | Passing automated checks |
| **Key Actions** | Linting, unit tests, code compilation | Packaging, container image creation, artifact staging | Automatic deployment to staging/production clusters |
| **Human Gate** | None (fully automated) | Manual approval to push to production | None (100% automated to production) |

---

## 2. Core GitHub Actions Primitives

- **Workflows (`.github/workflows/*.yml`)**: Configurable automated processes defined in YAML.
- **Events (`on:`)**: Triggers that start workflows (e.g., `push`, `pull_request`, `workflow_dispatch`, `schedule`).
- **Jobs (`jobs:`)**: Set of steps executed on the same runner. Jobs run in **parallel** by default unless ordered with `needs:`.
- **Steps (`steps:`)**: Individual tasks within a job. Can run shell commands (`run:`) or execute reusable Actions (`uses:`).
- **Runners (`runs-on:`)**: Virtual machines or containers executing jobs (e.g., `ubuntu-latest`, `windows-latest`, `macos-latest`, or self-hosted).
- **Secrets (`${{ secrets.MY_SECRET }}`)**: Encrypted environment variables for API keys, tokens, and SSH credentials.
- **Artifacts (`actions/upload-artifact`, `actions/download-artifact`)**: Files or test reports produced by a job persisted after the run finishes.

---

## 3. End-to-End Demo Project: `10-final-cicd-pipeline`

Located at: `session-16-github-actions/session-16-github-actions/10-final-cicd-pipeline/`

### Architecture Flow:
```text
  git push (main)
         │
         ▼
  [ GitHub Actions Trigger ]
         │
         ▼
  ┌───────────────┐
  │ 1. TEST JOB   │ ──► Setup Python 3.12 -> pip install -> pytest -v
  └───────┬───────┘
          │ (on success)
          ├───────────────────────────────┐
          ▼                               ▼
  ┌───────────────┐               ┌───────────────────┐
  │ 2. BUILD JOB  │               │ 3. SECURITY SCAN  │
  │ • build.sh    │               │ • Secret scan     │
  │ • artifacts   │               │ • Key leak audit  │
  └───────┬───────┘               └─────────┬─────────┘
          │                                 │
          └───────────────┬─────────────────┘
                          │ (both passed)
                          ▼
                  ┌───────────────┐
                  │ 4. DOCKER     │ ──► Multi-stage Docker build
                  │    PACKAGE    │
                  └───────┬───────┘
                          │
                          ▼
                  ┌───────────────┐
                  │ 5. DEPLOY     │ ──► Production deployment simulation
                  │    (CD)       │
                  └───────────────┘
```

---

## 4. Deliverables Checklist

- [x] **Application Source Code**: `app/calculator.py`
- [x] **Unit Tests**: `tests/test_calculator.py`
- [x] **Dockerfile**: Multi-stage production container image
- [x] **GitHub Actions Workflow**: `.github/workflows/ci.yml`
- [x] **CI Pipeline**: Automated linting, testing, artifact bundling
- [x] **CD Pipeline**: Docker build, container tagging, deployment gate
- [x] **Execution Logs & Verification**: Live local Docker build and test executions documented
