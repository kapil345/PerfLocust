import argparse
import yaml
import subprocess
import os

class PerfRunner:
    def __init__(self):
        self.config_file = None

    def parse_args(self):
        parser = argparse.ArgumentParser(description="Locust Performance Test Runner")
        parser.add_argument("-f", "--file", help="Path to YAML config file", required=True)
        args = parser.parse_args()
        self.config_file = args.file

    def load_config(self):
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"Config file {self.config_file} not found.")
        
        with open(self.config_file, "r") as file:
            return yaml.safe_load(file)

    def run_locust(self):
        config = self.load_config()

        command = [
            "locust",
            "-f", os.path.abspath("simulations/api_tests.py"),  # Corrected folder
            "--users", str(config["users"]),
            "--spawn-rate", str(config["spawn_rate"]),
            "--run-time", config["run_time"],
            "--host", config["host"]
        ]

        print(f"Running Locust: {' '.join(command)}")
        subprocess.run(command)

if __name__ == "__main__":
    runner = PerfRunner()
    runner.parse_args()
    runner.run_locust()