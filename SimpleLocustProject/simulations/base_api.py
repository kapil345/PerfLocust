# simulations/base_api.py
import os
from locust import HttpUser
from util.environment_parser import EnvironmentParser 

class BaseAPI(HttpUser):
    """
    Base class for API performance testing.
    """
    abstract = True  # Prevent Locust from running this directly

    def __init__(self, environment):
        #  Fetch the environment dynamically (set in run_locust.py)
        self.environment_name = os.getenv("ENVIRONMENT")

        if not self.environment_name:
            raise ValueError(" Error: ENVIRONMENT variable is not set. Ensure run_locust.py sets it.")

        # Fetch the API host dynamically based on the selected environment
        self.host_manager = EnvironmentParser(self.environment_name)
        self.host = self.host_manager.get_api_host()

        if not self.host:
            raise ValueError(f"Error: No API host found for environment {self.environment_name}")

        print(f"\n🔹 API Testing in {self.environment_name} - API Host: {self.host}")

        # Make sure self.host is set BEFORE calling super().__init__()
        super().__init__(environment)  # Initialize superclass after setting host