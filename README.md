# Kubernetes Observability Lab

A beginner-friendly, fully local Kubernetes + Observability project for learning and portfolio use.

This lab deploys a simple health-check API onto a local kind cluster, adds health probes and resource limits, installs Prometheus + Grafana, and demonstrates practical troubleshooting and CI validation of Kubernetes manifests.

**Cost: £0** — No cloud account required.

## Architecture

```
Windows host
    │
    ├── Docker Desktop
    │       └── kind cluster ("observability-lab")
    │               ├── Namespace: healthcheck
    │               │       ├── Deployment (healthcheck-api)
    │               │       └── Service (ClusterIP)
    │               │
    │               └── Namespace: monitoring
    │                       ├── Prometheus
    │                       ├── Grafana
    │                       └── kube-state-metrics / node-exporter
    │
    └── kubectl / port-forward → localhost
```

## Technologies

- Kubernetes (kind)
- Docker
- kubectl
- Prometheus + Grafana (kube-prometheus-stack)
- GitHub Actions + kubeconform
- PowerShell on Windows

## Prerequisites

- Docker Desktop (WSL 2 backend recommended)
- kubectl
- kind
- Helm 3
- Git

## Quick Start

```powershell
# 1. Create the kind cluster (only needed once)
kind create cluster --name observability-lab

# 2. Load the local health-check image
kind load docker-image healthcheck-api:latest --name observability-lab

# 3. Deploy the application
kubectl apply -f kubernetes/

# 4. Access the application
kubectl port-forward -n healthcheck svc/healthcheck-api 8080:80
# → http://localhost:8080/health

# 5. Access Grafana
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
# → http://localhost:3000  (admin / admin)
```

## What You Can Explore

- Kubernetes Deployments, Services, Namespaces, probes and resource limits
- Scaling with `kubectl scale`
- Prometheus metrics and Grafana dashboards
- Common failure modes (ImagePullBackOff, probe failures, CrashLoopBackOff)
- Automated YAML validation on every push/PR

## Cleanup

```powershell
kind delete cluster --name observability-lab
```

## Limitations

- This is a single-node local cluster. It is excellent for learning but is **not** equivalent to operating a production multi-node cloud cluster.
- No persistent storage, Ingress, or external load balancer is configured.
- Monitoring retention is deliberately short to keep resource usage low.

## Possible Next Steps

- Add a simple Ingress controller
- Instrument the Flask app with Prometheus client metrics
- Add a basic alert rule in Prometheus
- Promote the same manifests to a free-tier cloud cluster (e.g. Oracle Cloud, Civo, or Azure free tier)

## CI

Every push and pull request runs `kubeconform` against the manifests in `kubernetes/`.  
Invalid YAML fails the workflow.
```