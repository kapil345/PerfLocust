from simulations.base_api import BaseUser
from locust import task

class UITestUser(BaseUser):
    """
    Locust test class for UI performance testing.
    """
    host = "https://ui.example.com"

    @task
    def load_homepage(self):
        endpoint = "/"  # UI test endpoint
        with self.client.get(endpoint, name="Load Homepage", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Error {response.status_code}")