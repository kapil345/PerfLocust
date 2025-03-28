# utils/environment_parser.py
import json

class EnvironmentParser:
    """
    Utility class to retrieve API & service hosts dynamically.
    """

    def __init__(self, environment):
        self.environment = environment.upper()
        self.config_path = "environments/environments.json"
        self.hosts = self._load_hosts()

    def _load_hosts(self):
        """ Load host configurations from environments.json. """
        with open(self.config_path, "r") as file:
            env_config = json.load(file)

        if self.environment not in env_config:
            raise ValueError(f"❌ Invalid environment: {self.environment}")

        return env_config[self.environment]

    def get_api_host(self):
        """ Get the API Gateway URL dynamically. """
        api_host = self.hosts.get("api_host", None)

        if not api_host:
            raise ValueError(f"❌ Error: No `api_host` found in {self.environment}")

        return api_host