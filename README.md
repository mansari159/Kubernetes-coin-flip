# Kubernetes Coin-Flip Load Balancer System

A minimal Kubernetes deployment demonstrating a coin-flip computation system with Nginx load balancing and distributed Flask workers.

## Overview

This project deploys a simple yet complete microservices architecture in Kubernetes:

- **Nginx Load Balancer Pod**: Single Nginx container routing requests
- **Worker Pod**: Two Flask containers performing coin-flip calculations
- **Service**: NodePort service exposing the system on port 30080

## Architecture

```
┌──────────────────┐
│   External Client│
│  (Port 30080)    │
└────────┬─────────┘
         │
    ┌────▼──────┐
    │NodePort   │
    │Service    │
    └────┬──────┘
         │
    ┌────▼──────────────────┐
    │   Nginx Pod           │
    │  Load Balancer        │
    │  (Port 80)            │
    └────┬──────────────────┘
         │
    ┌────▼──────────────────┐
    │   Worker Pod          │
    │  ├─ Flask Worker 1    │
    │  │  (Port 5000)       │
    │  └─ Flask Worker 2    │
    │     (Port 5000)       │
    └───────────────────────┘
```

## Features

✅ **Lightweight**: Only 17 files, ~40KB total  
✅ **Production-Ready**: Proper Kubernetes patterns  
✅ **Scalable**: Easy to add more workers  
✅ **Load Balanced**: Nginx round-robin distribution  
✅ **Stateless**: No persistence required  

## Prerequisites

Before deploying, ensure you have:

### Required Software
- **Kubernetes cluster** (minikube, kubeadm, EKS, GKE, AKS, etc.)
  ```bash
  kubectl cluster-info
  kubectl get nodes
  ```

- **Docker** (for building container images)
  ```bash
  docker --version
  ```

- **kubectl** (Kubernetes command-line tool)
  ```bash
  kubectl version --client
  ```

- **curl** (for testing)
  ```bash
  curl --version
  ```

### Setup Minikube (if needed)

If you don't have a Kubernetes cluster running:

```bash
# Install minikube
curl -LO https://github.com/kubernetes/minikube/releases/latest/download/minikube-linux-amd64
chmod +x minikube-linux-amd64
sudo mv minikube-linux-amd64 /usr/local/bin/minikube

# Start cluster
minikube start --driver=docker --cpus=2 --memory=2048

# Verify
kubectl get nodes
```

## Quick Start (3 Steps)

### Step 1: Prepare Files

```bash
# Create working directory
mkdir -p ~/k8s-coinflip
cd ~/k8s-coinflip

# Copy all 17 files to this directory
cp /path/to/MINIMAL_SETUP/* .

# Verify files
ls -la
```

### Step 2: Build Docker Image

```bash
# Build the worker image (takes 2-3 minutes)
docker build -t coin-worker:latest .

# Verify
docker images | grep coin-worker
```

### Step 3: Deploy to Kubernetes

```bash
# Apply all Kubernetes manifests
kubectl apply -f 0-configmap.yaml
kubectl apply -f 1-namespace.yaml
kubectl apply -f 2-nginx-pod.yaml
kubectl apply -f 3-worker-pod.yaml
kubectl apply -f 4-service.yaml

# Wait for pods to start
sleep 30

# Check status
kubectl get pods -n coinflip
```

## Testing

### Check Deployment Status

```bash
# View all pods
kubectl get pods -n coinflip

# View services
kubectl get svc -n coinflip

# Check pod details
kubectl describe pod nginx-pod -n coinflip
kubectl describe pod worker-pod -n coinflip
```

### Test the Endpoint

```bash
# Get node IP
NODE_IP=$(minikube ip)
echo "Node IP: $NODE_IP"

# Test health (should return JSON)
curl http://$NODE_IP:30080/compute \
  -H 'Content-Type: application/json' \
  -d '{"heads":3}'
```

### Expected Response

```json
{"heads_required": 3, "total_flips": 15}
```

The response shows:
- `heads_required`: The requested number of consecutive heads
- `total_flips`: Total coin flips needed to achieve that

## API Endpoint

### POST /compute

Performs coin flip calculations.

**Request:**
```bash
curl -X POST http://NODE_IP:30080/compute \
  -H 'Content-Type: application/json' \
  -d '{"heads":5}'
```

**Request Body:**
```json
{
  "heads": 5
}
```

**Response:**
```json
{
  "heads_required": 5,
  "total_flips": 45
}
```

**Parameters:**
- `heads` (integer): Number of consecutive heads to achieve (1-20 recommended)

**Status Code:** 200 OK

## File Structure

### Application Code
```
app.py              Flask application with /compute endpoint
requirements.txt    Python dependencies (Flask==2.3.2)
Dockerfile          Docker image build configuration
nginx.conf          Nginx load balancing configuration
```

### Kubernetes Configuration
```
0-configmap.yaml    Stores Nginx configuration in Kubernetes
1-namespace.yaml    Creates isolated "coinflip" namespace
2-nginx-pod.yaml    Defines Nginx load balancer pod
3-worker-pod.yaml   Defines worker pod with 2 Flask containers
4-service.yaml      Exposes service on NodePort 30080
```

### Documentation
```
SUPER_SIMPLE.md              Start here - 3 commands only
README_PROJECT.md            This file
COPY_PASTE_THIS.txt         Commands ready to copy-paste
00_START_HERE.txt           Project overview
WHAT_EACH_FILE_DOES.txt     Detailed file descriptions
ARCHITECTURE.txt            System architecture details
RUN_THIS.txt                Complete deployment guide
STEPS.txt                   Step-by-step walkthrough
```

### Scripts
```
deploy.sh           Automated deployment script (optional)
```

## Common Operations

### View Logs

```bash
# Nginx logs
kubectl logs -n coinflip nginx-pod

# Worker logs (all containers)
kubectl logs -n coinflip worker-pod

# Follow logs in real-time
kubectl logs -n coinflip nginx-pod -f
```

### Scale Workers

To add more workers, edit `3-worker-pod.yaml`:

```yaml
containers:
- name: worker-1
  image: coin-worker:latest
  ports:
  - containerPort: 5000

- name: worker-2
  image: coin-worker:latest
  ports:
  - containerPort: 5000

- name: worker-3          # Add new container
  image: coin-worker:latest
  ports:
  - containerPort: 5000
```

Then apply:
```bash
kubectl apply -f 3-worker-pod.yaml
```

### Execute Commands in Pod

```bash
# Get shell in nginx pod
kubectl exec -it nginx-pod -n coinflip -- sh

# Get shell in worker pod
kubectl exec -it worker-pod -n coinflip -- sh
```

### Delete Everything

```bash
# Delete entire namespace (removes all resources)
kubectl delete namespace coinflip
```

## Troubleshooting

### Pods Not Starting

**Problem:** Pods stuck in "Pending" or "CrashLoopBackOff"

**Solution:**
```bash
# Check pod details
kubectl describe pod nginx-pod -n coinflip

# Check logs
kubectl logs nginx-pod -n coinflip

# Check events
kubectl get events -n coinflip
```

### Service Not Accessible

**Problem:** Cannot reach service on port 30080

**Solution:**
```bash
# Verify service exists
kubectl get svc -n coinflip

# Check service endpoints
kubectl get endpoints -n coinflip

# Try different node IP
kubectl get nodes -o wide
```

### Image Pull Errors

**Problem:** "ImagePullBackOff" error

**Solution:**
```bash
# Verify image is built
docker images | grep coin-worker

# Rebuild if needed
docker build -t coin-worker:latest .
```

### Connection Refused

**Problem:** Cannot connect to pod

**Solution:**
```bash
# Test connectivity from debug pod
kubectl run -it --rm debug --image=alpine --restart=Never -- sh

# Inside debug pod:
apk add curl
curl http://worker-pod:5000/
```

## Load Balancing

Nginx uses **round-robin** load balancing by default. With two workers, requests alternate:

1. Request 1 → Worker 1
2. Request 2 → Worker 2
3. Request 3 → Worker 1
4. Request 4 → Worker 2
...and so on.

View logs to see distribution:
```bash
kubectl logs -n coinflip worker-pod
```

## How It Works

### Request Flow

1. **Client Request**
   ```bash
   curl -X POST http://NODE_IP:30080/compute \
     -H 'Content-Type: application/json' \
     -d '{"heads":3}'
   ```

2. **Service Routing**
   - NodePort Service (port 30080) receives request
   - Routes to Nginx pod (port 80)

3. **Load Balancing**
   - Nginx receives request
   - Reads upstream configuration pointing to 2 workers
   - Routes to one of the Flask containers (port 5000)

4. **Computation**
   - Flask worker receives request
   - Performs coin flip calculation
   - Returns JSON response

5. **Response**
   - Response flows back through Nginx → Service → Client

### Why Two Containers in One Pod?

- **Shared Network Namespace**: Containers can reach each other on localhost
- **Resource Efficiency**: Shared system resources
- **Tight Coupling**: Both workers are part of same logical unit
- **Simple Load Balancing**: Nginx routes locally

## Performance Considerations

- **CPU**: 2 cores recommended for minikube
- **Memory**: 2GB recommended for minikube
- **Throughput**: Limited by single Nginx pod
- **Scaling**: Add more containers to worker pod or use Deployment

## Production Enhancements

For production use, consider:

1. **Deployment instead of Pod**
   - Automatic pod restart
   - Easy scaling with replicas
   - Health checks and probes

2. **Resource Limits**
   - CPU and memory requests/limits
   - Prevent resource hogging

3. **Monitoring**
   - Prometheus for metrics
   - Grafana for dashboards
   - Log aggregation (ELK, Loki)

4. **Security**
   - Pod security policies
   - Network policies
   - RBAC authorization

5. **Ingress**
   - Replace NodePort with Ingress
   - Domain-based routing
   - TLS/SSL support

## Files Size Reference

| File | Size | Purpose |
|------|------|---------|
| app.py | 587B | Flask application |
| Dockerfile | 148B | Container build |
| nginx.conf | 246B | Load balancer config |
| requirements.txt | 13B | Dependencies |
| *.yaml | 50-400B each | Kubernetes manifests |
| Total | ~40KB | Complete system |

## Environment Variables

The Flask application doesn't require any environment variables. Configuration is done through Kubernetes manifests:

- Pod names and labels
- Container ports
- ConfigMap references

## Data Persistence

This system is **stateless**. No data is persisted:
- Each request is independent
- No database required
- No persistent volumes needed
- Safe to restart pods

## Networking

### Internal Communication
- Pods communicate via Kubernetes DNS
- Service DNS name: `nginx-service` (if using Services)
- Pod name: `nginx-pod`, `worker-pod`

### External Access
- NodePort Service on port 30080
- Accessible from: `http://NODE_IP:30080`
- Get node IP: `minikube ip` or `kubectl get nodes`

## Cleanup

### Delete Specific Resource
```bash
kubectl delete pod nginx-pod -n coinflip
kubectl delete pod worker-pod -n coinflip
kubectl delete svc nginx-service -n coinflip
```

### Delete Everything
```bash
kubectl delete namespace coinflip
```

### Remove Docker Image
```bash
docker rmi coin-worker:latest
