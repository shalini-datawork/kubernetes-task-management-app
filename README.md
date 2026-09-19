# Kubernetes Task Management App

A containerized Task Management application built with **FastAPI, PostgreSQL, Nginx, Docker, and Kubernetes**.

This project was created as a hands-on Kubernetes learning and portfolio project. It covers application deployment, networking, persistent storage, configuration, security, health checks, autoscaling, rolling updates, rollback, Helm, and Kubernetes troubleshooting.

---

## 🎯 Project Overview

The application provides a simple web interface for creating and retrieving tasks.

The application is composed of:

* **Frontend** — HTML, CSS, JavaScript served by Nginx
* **Backend** — FastAPI REST API running with Uvicorn
* **Database** — PostgreSQL running as a Kubernetes StatefulSet
* **Ingress** — Routes browser traffic to the frontend and API
* **Kubernetes** — Manages deployment, networking, storage, scaling, and recovery
* **Helm** — Provides repeatable Kubernetes deployments and environment-specific values

The primary goal of the project was to learn how a multi-component application behaves when deployed and managed on Kubernetes.

---

## 🏗️ Architecture

```text
                         ┌──────────────────────┐
                         │       Browser        │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Kubernetes Ingress   │
                         │    task-app.local    │
                         └──────────┬───────────┘
                                    │
                     ┌──────────────┴──────────────┐
                     │                             │
                     ▼                             ▼
             ┌───────────────┐             ┌───────────────┐
             │    Frontend   │             │    Backend    │
             │     Nginx     │             │    FastAPI    │
             │  2 replicas   │             │  2+ replicas  │
             └───────────────┘             └───────┬───────┘
                                                   │
                                                   ▼
                                          ┌─────────────────┐
                                          │   PostgreSQL    │
                                          │   StatefulSet   │
                                          │ Persistent Data │
                                          └─────────────────┘
```

### Request flow

```text
Browser
   │
   ▼
Ingress
   │
   ├── /       → Frontend Service → Nginx
   │
   └── /api/*  → Backend Service  → FastAPI
                                      │
                                      ▼
                                  PostgreSQL
```

---

## 🚀 Application Features

* Create tasks
* Retrieve tasks
* FastAPI REST API
* Nginx-based frontend
* PostgreSQL database
* Persistent task storage
* Health-check endpoints
* Kubernetes deployment
* Helm-based deployment configuration
* Development and production Helm values

---

## 🛠️ Technology Stack

| Technology              | Purpose                        |
| ----------------------- | ------------------------------ |
| Python                  | Backend programming language   |
| FastAPI                 | REST API framework             |
| Uvicorn                 | Application server             |
| PostgreSQL              | Persistent relational database |
| HTML / CSS / JavaScript | Frontend                       |
| Nginx                   | Frontend web server            |
| Docker                  | Containerization               |
| Kubernetes              | Container orchestration        |
| Helm                    | Kubernetes package management  |
| Git                     | Version control                |
| GitHub                  | Source-code hosting            |

---

# 🐳 Docker

The application is containerized using Docker.

## Backend

The backend container uses:

* Python 3.12
* FastAPI
* Uvicorn
* PostgreSQL connectivity

The backend exposes port `8000`.

## Frontend

The frontend container uses:

* Nginx Alpine
* HTML
* CSS
* JavaScript

The frontend communicates with the backend through the Kubernetes Ingress.

---

# ☸️ Kubernetes Concepts Demonstrated

This project was used to practice a broad range of Kubernetes concepts.

## Workloads

* Pods
* Deployments
* ReplicaSets
* StatefulSets
* DaemonSet concepts
* Jobs
* CronJobs
* Init Containers

## Networking

* ClusterIP Services
* NodePort
* Service DNS
* CoreDNS
* Ingress
* NetworkPolicy
* Endpoint troubleshooting
* EndpointSlice troubleshooting
* Pod-to-Service communication
* Egress concepts

## Configuration and Security

* ConfigMaps
* Kubernetes Secrets
* ServiceAccounts
* RBAC
* Roles
* Permission testing with `kubectl auth can-i`
* SecurityContext
* Non-root containers
* NetworkPolicy
* Pod security concepts

## Storage

* PersistentVolumes
* PersistentVolumeClaims
* StorageClasses
* StatefulSet persistent storage
* PostgreSQL data persistence

## Reliability

* Liveness probes
* Readiness probes
* PodDisruptionBudget
* Kubernetes self-healing
* Rolling updates
* Rollout history
* Rollbacks

## Scaling and Scheduling

* Resource requests
* Resource limits
* Horizontal Pod Autoscaler
* CPU-based scaling
* NodeSelector
* Node Affinity
* Pod scheduling
* Tolerations

---

# 🗄️ PostgreSQL and Persistent Storage

PostgreSQL runs as a Kubernetes **StatefulSet**.

Persistent storage is provided through:

```text
StatefulSet
    │
    ▼
PersistentVolumeClaim
    │
    ▼
PersistentVolume / StorageClass
```

The project includes hands-on testing of database persistence, including verifying that task data remains available after PostgreSQL pod recreation.

The database is exposed through a headless Kubernetes Service to support StatefulSet networking.

---

# 🔐 Configuration and Secret Management

Application configuration is separated from the container images using Kubernetes ConfigMaps.

Sensitive credentials are kept outside the Git repository.

Example files are provided:

```text
backend-secret.example.yaml
postgres-secret.example.yaml
```

Local secret files are intentionally excluded using `.gitignore`.

For Helm deployments, local credentials can be supplied through:

```text
task-app/secrets.local.yaml
```

This file is intentionally excluded from Git.

> Never commit real passwords, API keys, tokens, or other credentials to the repository.

---

# 🛡️ RBAC

The project includes hands-on RBAC exercises using:

* ServiceAccounts
* Roles
* RoleBindings
* Resource permissions
* `kubectl auth can-i`

Example permission testing included verifying that a ServiceAccount could:

```text
get pods
list services
watch pods
```

while being denied permissions such as:

```text
delete pods
get secrets
```

This demonstrates the Kubernetes principle of granting only the permissions required by a workload.

---

# 🌐 Ingress

The application is exposed through Kubernetes Ingress using:

```text
task-app.local
```

Traffic is separated between the frontend and backend:

```text
/       → Frontend
/api/*  → Backend
```

Ingress routing and rewrite behavior were tested using `curl` and browser requests.

The project also included troubleshooting an API `404` caused by an incorrect path/rewrite configuration.

---

# ❤️ Health Checks

The backend exposes:

```text
/health
/config
/db-health
/tasks
```

Kubernetes uses the health endpoint for:

* Readiness probes
* Liveness probes

This allows Kubernetes to distinguish between containers that are running and containers that are actually ready to receive traffic.

---

# 📈 Horizontal Pod Autoscaling

The backend uses Kubernetes Horizontal Pod Autoscaling.

The demonstrated HPA configuration is:

```text
Minimum replicas: 2
Maximum replicas: 5
CPU target: 50%
```

The project includes a hands-on CPU load test to observe Kubernetes automatically increase backend replicas when CPU utilization rises.

After the load was removed, the HPA was observed scaling the backend back down.

Resource requests were configured so that Kubernetes could calculate CPU utilization for HPA.

---

# 🔄 Rolling Updates and Rollback

The backend Deployment uses Kubernetes `RollingUpdate`.

The project included hands-on testing of:

* Container image version updates
* Rollout status
* Rollout history
* Rolling updates
* Failed image deployment
* Rollback to a previous version

For example, an attempted image update produced an `ImagePullBackOff` when the expected image was not available.

After correcting the deployment, rollout and rollback behavior were tested using Kubernetes rollout commands.

---

# 🧪 Troubleshooting Practiced

One of the main goals of this project was learning how to troubleshoot Kubernetes rather than only deploying successful workloads.

Hands-on troubleshooting included:

* `CrashLoopBackOff`
* `ImagePullBackOff`
* `OOMKilled`
* Failed readiness probes
* Failed liveness probes
* NetworkPolicy connectivity
* Service and Endpoint connectivity
* EndpointSlice behavior
* DNS resolution
* HPA behavior
* Pod self-healing
* Kubernetes events
* Resource usage with `kubectl top`
* Ingress path and rewrite issues
* PostgreSQL startup and persistence issues

These exercises helped connect Kubernetes concepts with real failure scenarios.

---

# 📦 Helm

The project includes a Helm chart for repeatable Kubernetes deployments.

The chart includes:

* `Chart.yaml`
* `Chart.lock`
* Configurable values
* Development values
* Production values
* Helm templates
* Dependency management
* Bitnami PostgreSQL dependency
* Environment-specific configuration

Example Helm values files:

```text
values.yaml
values-dev.yaml
values-prod.yaml
```

Local credentials are supplied separately through:

```text
secrets.local.yaml
```

and are excluded from Git.

---

# 🚀 Helm Deployment

Update Helm dependencies:

```bash
helm dependency update ./task-app
```

Install the application:

```bash
helm upgrade --install task-app ./task-app \
  -n helm-lab \
  --create-namespace \
  -f task-app/values.yaml \
  -f task-app/secrets.local.yaml
```

Development configuration:

```bash
helm upgrade --install task-app-dev ./task-app \
  -n helm-lab \
  -f task-app/values-dev.yaml \
  -f task-app/secrets.local.yaml
```

Production configuration:

```bash
helm upgrade --install task-app-prod ./task-app \
  -n helm-lab \
  -f task-app/values-prod.yaml \
  -f task-app/secrets.local.yaml
```

> `secrets.local.yaml` contains local credentials and is intentionally excluded from Git.

---

# 🔍 Deployment Verification

Check Kubernetes resources:

```bash
kubectl get pods -n helm-lab
kubectl get svc -n helm-lab
kubectl get ingress -n helm-lab
kubectl get pvc -n helm-lab
kubectl get hpa -n helm-lab
```

Check Helm releases:

```bash
helm list -n helm-lab
```

Check resource consumption:

```bash
kubectl top pods -n helm-lab
```

---

# 📁 Project Structure

```text
.
├── app.py
├── requirements.txt
├── Dockerfile
├── README.md
├── .gitignore
│
├── frontend/
│   ├── Dockerfile
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── backend.yaml
├── backend-configmap.yaml
├── backend-network-policy.yaml
├── backend-pdb.yaml
├── backend-secret.example.yaml
├── frontend.yaml
├── ingress.yaml
│
├── postgres.yaml
├── postgres-network-policy.yaml
├── postgres-secret.example.yaml
│
├── database-pod.yaml
├── postgres-policy-backup.yaml
├── postgres-restrictive.yaml
│
├── task-app/
│   ├── Chart.yaml
│   ├── Chart.lock
│   ├── values.yaml
│   ├── values-dev.yaml
│   ├── values-prod.yaml
│   └── templates/
│
└── labs/
    ├── rbac/
    ├── scheduling/
    └── security/
```

> Local secret files and other excluded files are intentionally not shown as tracked repository files.

---

# 🧪 Kubernetes Learning Labs

The `labs/` directory contains additional hands-on Kubernetes exercises performed while developing the project.

## RBAC

Exercises covering:

* ServiceAccounts
* Roles
* RoleBindings
* Resource permissions
* `kubectl auth can-i`

## Scheduling

Exercises covering:

* NodeSelector
* Node Affinity
* Tolerations
* Scheduling constraints
* Scheduling failures

## Security

Exercises covering:

* SecurityContext
* Non-root containers
* Kubernetes security concepts

---

# 🎓 Key Learning Outcomes

Through this project, I practiced how to:

* Containerize a multi-component application with Docker
* Deploy applications using Kubernetes
* Separate frontend, backend, and database workloads
* Expose applications using Kubernetes Services and Ingress
* Persist PostgreSQL data using Kubernetes storage
* Manage configuration using ConfigMaps
* Protect credentials using Secrets
* Control workload permissions using RBAC
* Secure communication using NetworkPolicy
* Configure readiness and liveness probes
* Manage CPU resources using requests and limits
* Automatically scale workloads using HPA
* Perform rolling deployments
* Investigate failed deployments
* Roll back Kubernetes deployments
* Use Helm for repeatable deployments
* Troubleshoot Kubernetes networking, storage, scheduling, and workload failures

---

# 💼 Portfolio Project

This project demonstrates hands-on experience building and operating a containerized application on Kubernetes.

Rather than focusing only on successful deployment, the project also includes deliberate testing of common Kubernetes failure and operational scenarios such as:

```text
Deployment
   ↓
Configuration
   ↓
Networking
   ↓
Persistent Storage
   ↓
Security
   ↓
Health Checks
   ↓
Scaling
   ↓
Rolling Updates
   ↓
Rollback
   ↓
Troubleshooting
```

The project serves as a practical foundation for further work with **Kubernetes, cloud platforms, CI/CD, observability, and data engineering infrastructure**.
