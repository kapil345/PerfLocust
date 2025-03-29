#!/usr/bin/env python3
import argparse
import yaml
import os
import subprocess
import json
import time

class KubeLocustRunner:
    """
    Kubernetes-based Locust Test Runner
    Handles Locust Master/Worker Deployment in Kubernetes for Load Testing
    """

    DEFAULT_NAMESPACE = "locust-perf"
    DEFAULT_PREFIX = "locust"

    def __init__(self, config_file):
        self.config_file = config_file
        self.config = self._load_config()
        self.docker_image = self.config.get("docker_image", "locustio/locust")
        self.namespace = self.config.get("namespace", "locust-perf")
        self.kube_context = self.config.get("kube_config", "kind-locust-cluster")
        self.test_file = self.config.get("test_file", "simulations/api_tests.py")
        self.users = self.config.get("users", 5)
        self.spawn_rate = self.config.get("spawn_rate", 3)
        self.run_time = self.config.get("run_time", "1m")
        self.headless = self.config.get("headless", True)
        self.env_vars = self.config.get("env_vars", {})

    def _load_config(self):
        """Load YAML configuration file."""
        with open(self.config_file, "r") as f:
            return yaml.safe_load(f)

    def build_and_push_docker_image(self):
        """Build and push Docker image based on configuration."""
        registry = self.config.get("docker_registry", None)  # Example: "mycompany/artifactory"
        image_name = self.config.get("docker_image_name", "locust-api")
        tag = self.config.get("docker_tag", "latest")

        full_image_name = f"{registry}/{image_name}:{tag}" if registry else f"{image_name}:{tag}"
        
        print(f"🛠️  Building Docker Image: {full_image_name}...")
        subprocess.run(["docker", "build", "-t", full_image_name, "."], check=True)

        if registry:
            print(f"🚀 Pushing Image to {registry}...")
            subprocess.run(["docker", "push", full_image_name], check=True)

        self.docker_image = full_image_name  # Update image path for pod deployment
    
    def _run_kubectl(self, command):
        """Run a kubectl command."""
        full_command = f"kubectl --context={self.kube_context} {command}"
        try:
            result = subprocess.run(full_command, shell=True, check=True, capture_output=True, text=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")
            return ""

    def create_namespace(self):
        """Create Kubernetes namespace if it does not exist."""
        print(f"🔹 Creating namespace: {self.namespace}")
        self._run_kubectl(f"create namespace {self.namespace} --dry-run=client -o yaml | kubectl apply -f -")

    def create_configmap(self):
        """Create a ConfigMap for Locust test settings."""
        config_data = {
            "test_file": self.locustfile,
            "users": str(self.users),
            "spawn_rate": str(self.spawn_rate),
            "run_time": self.run_time
        }
        yaml_data = yaml.dump({"apiVersion": "v1", "kind": "ConfigMap", "metadata": {"name": f"{self.prefix}-config", "namespace": self.namespace}, "data": config_data})

        with open("temp_configmap.yaml", "w") as f:
            f.write(yaml_data)
        self._run_kubectl("apply -f temp_configmap.yaml")
        os.remove("temp_configmap.yaml")

    def create_locust_pod(self, role):
        """Deploy a Locust Master/Worker Pod in Kubernetes."""
        pod_name = f"{self.prefix}-{role}"
        is_master = role == "master"
        extra_env = "- name: LOCUST_MODE\n  value: master" if is_master else "- name: LOCUST_MODE\n  value: worker"

        pod_yaml = f"""
apiVersion: v1
kind: Pod
metadata:
  name: {pod_name}
  namespace: {self.namespace}
spec:
  restartPolicy: Never
  containers:
  - name: locust-{role}
    image: {self.image}
    command: ["locust"]
    args: ["--headless", "-f", "/mnt/locust/{self.locustfile}", "--users={self.users}", "--spawn-rate={self.spawn_rate}", "--run-time={self.run_time}", "--host=https://your-api-url.com"]
    volumeMounts:
    - name: locust-config
      mountPath: "/mnt/locust"
    env:
    - name: LOCUST_ROLE
      value: {role}
    {extra_env}
  volumes:
  - name: locust-config
    configMap:
      name: {self.prefix}-config
"""

        with open(f"temp_{role}.yaml", "w") as f:
            f.write(pod_yaml)
        self._run_kubectl(f"apply -f temp_{role}.yaml")
        os.remove(f"temp_{role}.yaml")

    def wait_for_completion(self, role):
        """Wait for the master pod to complete execution."""
        while True:
            result = subprocess.run(["kubectl", "get", "pod", master_pod, "-n", self.namespace, "-o", "jsonpath={.status.phase}", "--context", self.kube_context], capture_output=True, text=True)
            status = result.stdout.strip()
            if status == "Succeeded" or status == "Failed":
                print(f"🔴 Test Completed with status: {status}")
                break
            print("⏳ Locust Master is still running...")
            subprocess.run(["sleep", "5"])

    def cleanup(self):
        """Clean up all Locust resources after execution."""
        print(" Cleaning up Locust resources...")

    # Delete all pods with label matching locust prefix
        self._run_kubectl(f"delete pod -n {self.namespace} --selector=app={self.prefix}")

    # Delete all configmaps related to Locust
        self._run_kubectl(f"delete configmap -n {self.namespace} --selector=app={self.prefix}")

    # Delete any remaining service (if created)
        self._run_kubectl(f"delete service -n {self.namespace} --selector=app={self.prefix}")

        print(" Cleanup complete!")

    def run(self):
        """Execute the full Locust test in Kubernetes."""
        """Execute the full Locust test in Kubernetes."""
        if "build_docker" in self.config and self.config["build_docker"]:
         self.build_and_push_docker_image()
        self.create_namespace()
        self.create_configmap()
        self.create_locust_pod("master")
        self.create_locust_pod("worker")
        self.wait_for_completion("master")
        self.cleanup()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kubernetes Locust Runner")
    parser.add_argument("-f", "--file", required=True, help="Path to YAML configuration file")
    args = parser.parse_args()

    runner = KubeLocustRunner(args.file)
    runner.run()