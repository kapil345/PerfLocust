import argparse
import yaml
import subprocess
import time
import os

class LocustKubeRunner:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = self._load_config()
        self.namespace = self.config.get("namespace", "default")
        self.pod_name = self.config.get("pod_name", "locust-standalone")
        self.image = self.config.get("docker_image", "kapilautomation/locust-perf-image:latest")
        self.command = self.config.get("command", ["python"])
        self.args = self.config.get("args", ["/opt/locust/runner/run_locust.py", "-f", "environments/load_test.yml"])

    def _load_config(self):
        with open(self.config_file, 'r') as f:
            return yaml.safe_load(f)

    def _run_kubectl(self, command):
        full_cmd = f"kubectl --namespace={self.namespace} {command}"
        try:
            result = subprocess.run(full_cmd, shell=True, check=True, capture_output=True, text=True)
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error executing kubectl command: {e.stderr}")

    def create_namespace(self):
        print(f"🔧 Creating namespace: {self.namespace}")
        self._run_kubectl(f"create namespace {self.namespace} --dry-run=client -o yaml | kubectl apply -f -")

    def delete_existing_pod(self, pod_name):
        print(f"🧹 Deleting old pod: {pod_name}")
        subprocess.run(f"kubectl delete pod {pod_name} --namespace={self.namespace}", shell=True)
    
    def create_pod(self):
        pod_manifest = {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {
                "name": self.pod_name,
                "labels": {
                    "app": "locust"
                }
            },
            "spec": {
                "containers": [
                    {
                        "name": "locust",
                        "image": self.image,
                        "imagePullPolicy": "Always",
                        "command": self.command,
                        "args": self.args
                    }
                ],
                "restartPolicy": "Never"
            }
        }

        pod_file = "temp_locust_pod.yaml"
        with open(pod_file, "w") as f:
            yaml.dump(pod_manifest, f)

        print(f" Deploying Pod: {self.pod_name}")
        self._run_kubectl(f"apply -f {pod_file}")
        os.remove(pod_file)

    def run(self):
        self.create_namespace()
        self.delete_existing_pod("locust-standalone")
        self.create_pod()
        # Placeholder: self.create_configmap()
        # Placeholder: self.setup_reporting()
        # Placeholder: self.cleanup()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Locust tests via Kubernetes")
    parser.add_argument("-f", "--file", required=True, help="Path to kube config YAML")
    args = parser.parse_args()

    runner = LocustKubeRunner(args.file)
    runner.run()