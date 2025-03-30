# PerfLocust


How to execute test from kubernetes pods


<img width="1313" alt="Image" src="https://github.com/user-attachments/assets/4fb2f2ea-04f2-439a-bb89-3a9176d2ab16" />
Create the pod

# Locust Kubernetes Performance Testing

This project enables you to run Locust-based performance tests locally, via Docker containers, and from Kubernetes pods.

---

## 📁 Project Structure

```
SimpleLocustProject/
├── runner/
│   └── run_locust.py
│   └── kube_locust_runner.py
├── environments/
│   └── load_test.yml
│   └── kube_locust_config.yml
├── simulations/
│   └── api_tests.py
├── constants/
│   └── api_constants.py
├── Dockerfile
└── locust-pod.yaml
```

---

## ✅ Running Locally (Without Docker)

Install dependencies and run using:

```bash
pip install -r requirements.txt
python runner/run_locust.py -f environments/load_test.yml
```

---

## 🐳 Running From Docker (Local Image)

### Step 1: Build Docker Image
```bash
docker build -t locust-perf-image .
```

### Step 2: Run Container
```bash
docker run --rm \
  --entrypoint python \
  -v $(pwd)/runner/run_locust.py:/opt/locust/runner/run_locust.py \
  -v $(pwd)/environments/load_test.yml:/opt/locust/environments/load_test.yml \
  locust-perf-image /opt/locust/runner/run_locust.py -f environments/load_test.yml
```

---

## ☁️ Running in Kubernetes

### Option 1: Using Prebuilt Image from Docker Hub

#### Step 1: Push your image
```bash
docker tag locust-perf-image kapilautomation/locust-perf-image:latest
docker push kapilautomation/locust-perf-image:latest
```

#### Step 2: Modify Pod YAML
Update `locust-pod.yaml`:
```yaml
spec:
  containers:
  - name: locust
    image: kapilautomation/locust-perf-image:latest
    imagePullPolicy: Always
```

#### Step 3: Deploy to Cluster
```bash
kubectl apply -f locust-pod.yaml
```

To check logs:
```bash
kubectl logs locust-standalone
```

---

### Option 2: Using Python Kubernetes Runner

 Running Locust via Pod Runner (Kubernetes)
This project supports executing Locust performance tests inside Kubernetes pods using a Python-based runner.

📁 Pre-requisites
Kubernetes cluster (local via kind or remote)

Locust Docker image built & pushed (e.g. kapilautomation/locust-perf-image:latest)

Valid Locust test files inside your image

kubectl configured and connected to the right cluster

Namespace created (e.g., locust-perf)

🧪 Step-by-Step: Run Pod with Locust via Code


Run the Python-based Kubernetes Pod Runner:

```bash
python runner/kube_locust_runner.py -f environments/kube_locust_config.yml
```

Verify Pod is Created:

```bash
kubectl get pods -n locust-perf
```
Check Logs of the Running Pod:

```bash
kubectl logs -f locust-standalone -n locust-perf
```

📄 Sample Config (kube_locust_config.yml)

```bash
namespace: locust-perf
docker_image: kapilautomation/locust-perf-image:latest
test_file: runner/run_locust.py
config_file: environments/load_test.yml
pod_name: locust-standalone
```

✅ Notes
Runner auto-creates the namespace (if not exists).

Old pods with the same name are deleted before re-deployment.

Test execution logs are accessible via kubectl logs.

---

## 🔧 Troubleshooting
- Use `kubectl describe pod <name>` and `kubectl logs <name>` to debug.
- Ensure your image is pushed if not using local kind cluster.
- For kind clusters, load the image:
```bash
kind load docker-image locust-perf-image --name kind-locust-cluster
```

---

## 📌 Notes
- Locust requires test file to be mounted or copied to `/opt/locust/...` inside container.
- Avoid using `imagePullPolicy: Always` if working with local images.

---

## 📜 License
Private project by Kapil Kumar | For internal use only

