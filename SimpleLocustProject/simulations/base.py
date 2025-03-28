import os
import yaml
from locust import HttpUser

# Default config file path (updated to use environments/)
DEFAULT_CONFIG_PATH = "environments/load_test.yml"

def load_config():
    """
    Load YAML configuration file from the environment variable or use the default path.
    """
    config_path = os.getenv("CONFIG_PATH", DEFAULT_CONFIG_PATH)

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path, "r") as file:
        return yaml.safe_load(file)

# Load configuration once for reuse
config = load_config()

class BaseUser(HttpUser):
    """
    Base class for Locust tests with shared configuration.
    """
    abstract = True  # Mark this as an abstract class
    host = config.get("host", "https://default-api.com")  # Default host if not provided
