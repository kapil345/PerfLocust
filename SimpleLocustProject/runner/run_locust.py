# runner/run_locust.py
import os
import yaml
import subprocess

class PerfRunner:
    def __init__(self):
        self.config_file = None

    def parse_args(self):
        import argparse
        parser = argparse.ArgumentParser(description="Locust Performance Test Runner")
        parser.add_argument("-f", "--file", help="Path to YAML config file", required=True)
        args = parser.parse_args()
        self.config_file = args.file

    def load_config(self):
        """ Load configuration from YAML. """
        with open(self.config_file, "r") as file:
            return yaml.safe_load(file)

    def run_locust(self):
        config = self.load_config()
        # read the yml file
        environment_name = config.get("environment", "").upper()  
        if not environment_name:
            raise ValueError("Error: No environment specified in load_test.yml")

        # setting the env variable after loading from yml file
        os.environ["ENVIRONMENT"] = environment_name  

        print(f"\n Running tests in **{environment_name}** environment")

        test_files = config.get("test_files", ["simulations/api_tests.py"])
        report_path = f"reports/locust_report_{environment_name.lower()}.html"

        for test_file in test_files:
            command = [
                "locust",
                "-f", os.path.abspath(test_file),
                "--users", str(config["users"]),
                "--spawn-rate", str(config["spawn_rate"]),
                "--run-time", config["run_time"],
                "--headless",
                f"--html={report_path}"
            ]

            print(f"Running: {test_file}")
            subprocess.run(command)
            print(f"\n Report generated: {report_path}")

if __name__ == "__main__":
    runner = PerfRunner()
    runner.parse_args()
    runner.run_locust()
