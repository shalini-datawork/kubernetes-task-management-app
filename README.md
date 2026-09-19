# Kubernetes Task Management App

A containerized Task Management application built with **FastAPI, PostgreSQL, Nginx, Docker, and Kubernetes**, with a Helm chart for repeatable deployments.

This project was built as a hands-on Kubernetes learning and portfolio project, covering application deployment, networking, persistent storage, security, scaling, scheduling, Helm, and troubleshooting.

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
                                          │   Persistent DB │
                                          └─────────────────┘
```

## 🚀 Application Features

* Create and retrieve tasks
* FastAPI REST API
* Nginx frontend
* PostgreSQL database
* Persistent task storage
* Health and database-health endpoints
* Kubernetes-based deployment
* Helm-based deployment
* Development and production Helm configurations

## 🐳 Docker

The application is containerized using Docker.

### Backend

* Python 3.12
* FastAPI
* Uvicorn
* PostgreSQL connectivity

### Frontend

* Nginx Alpine
* HTML/CSS/JavaScript
* API requests routed through Kubernetes Ingress

## ☸️ Kubernetes Concepts Demonstrated

### Workloads

* Pods
* Deployments
* ReplicaSets
* StatefulSets
* DaemonSet concepts
* Jobs and CronJobs

### Networking

* ClusterIP Services
* NodePort
* Service DNS
* Ingress
* NetworkPolicy
* Endpoint and EndpointSlice troubleshooting

### Configuration and Security

* ConfigMaps
* Kubernetes Secrets
* RBAC
* ServiceAccounts
* SecurityContext
* Non-root containers
* NetworkPolicy
* Pod Security concepts

### Storage

* PersistentVolume
* PersistentVolumeClaim
* StorageClass
* StatefulSet persistent storage
* PostgreSQL data persistence

### Reliability

* Liveness probes
* Readiness probes
* PodDisruptionBudget
* Self-healing
* Rolling updates
* Rollbacks

### Scaling and Scheduling

* Resource requests and limits
* Horizontal Pod Autoscaler
* NodeSelector
* Node Affinity
* Pod scheduling
* Tolerations

### Helm

The project includes a Helm chart with:

* Configurable values
* Development values
* Production values
* Templates
* Helm dependency management
* Bitnami PostgreSQL dependency
* Helm-based environment configuration

## 🔐 Secret Management

Real passwords and credentials are **not stored in this repository**.

Sensitive files are excluded using `.gitignore`.

Example files are provided:

```text
backend-secret.example.yaml
postgres-secret.example.yaml
```

Replace the placeholder values locally before applying them.

For the Helm deployment, local credentials can be supplied through:

```text
task-app/secrets.local.yaml
```

This file is intentionally excluded from Git.

## 📁 Project Structure

```text
.
├── app.py
├── requirements.txt
├── Dockerfile
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
├── frontend.yaml
├── ingress.yaml
├── postgres.yaml
├── postgres-network-policy.yaml
│
├── labs/
│   ├── rbac/
│   ├── scheduling/
│   └── security/
│
├── task-app/
│   ├── Chart.yaml
│   ├── Chart.lock
│   ├── values.yaml
│   ├── values-dev.yaml
│   ├── values-prod.yaml
│   └── templates/
│
├── backend-secret.example.yaml
├── postgres-secret.example.yaml
├── .gitignore
└── README.md
```

## 🧪 Kubernetes Learning Labs

The `labs/` directory contains additional hands-on Kubernetes exercises completed while developing the project.

### RBAC

Examples covering:

* ServiceAccounts
* Roles
* Permissions
* `kubectl auth can-i`

### Scheduling

Examples covering:

* NodeSelector
* Node Affinity
* Tolerations
* Scheduling failures

### Security

Examples covering:

* SecurityContext
* Running containers as non-root

## 📈 Scaling

The backend is configured with resource requests and an HPA.

Example production configuration:

```text
Minimum replicas: 3
Maximum replicas: 5
CPU target: 60%
```

The project also includes experiments with CPU load to observe HPA behavior.

## 🔄 Deployment Strategy

The backend deployment uses Kubernetes RollingUpdate.

The project includes hands-on testing of:

* Image version updates
* Rolling updates
* Rollout status
* Rollout history
* Rollback to a previous version

## 🩺 Health Checks

The backend exposes:

```text
/health
/config
/db-health
/tasks
```

Kubernetes uses health endpoints for liveness and readiness checks.

## 🔍 Troubleshooting Practiced

The project includes hands-on troubleshooting of:

* CrashLoopBackOff
* ImagePullBackOff
* OOMKilled
* Failed readiness probes
* Failed liveness probes
* NetworkPolicy connectivity
* Service/Endpoint connectivity
* DNS resolution
* HPA behavior
* Pod self-healing
* Kubernetes events
* Resource usage with `kubectl top`

## 📦 Helm Deployment

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

For development:

```bash
helm upgrade --install task-app-dev ./task-app \
  -n helm-lab \
  -f task-app/values-dev.yaml \
  -f task-app/secrets.local.yaml
```

For production:

```bash
helm upgrade --install task-app-prod ./task-app \
  -n helm-lab \
  -f task-app/values-prod.yaml \
  -f task-app/secrets.local.yaml
```

> `secrets.local.yaml` contains local credentials and is intentionally excluded from Git.

## 🧹 Verify Deployment

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

Check resources:

```bash
kubectl top pods -n helm-lab
```

## 🎯 What This Project Demonstrates

This project demonstrates practical experience with:

* Docker containerization
* FastAPI
* PostgreSQL
* Kubernetes application deployment
* Kubernetes networking
* Persistent storage
* Configuration management
* Secret management
* RBAC
* Network security
* Resource management
* Autoscaling
* Scheduling
* Application health monitoring
* Rolling deployments and rollback
* Helm
* Kubernetes troubleshooting

## 📌 Portfolio Project

This project was created as a hands-on Kubernetes portfolio project to demonstrate the ability to deploy, configure, secure, scale, troubleshoot, and manage a multi-component application on Kubernetes.
