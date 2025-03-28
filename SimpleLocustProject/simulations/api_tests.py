from simulations.base import BaseUser, config
from locust import task

class APIUser(BaseUser):
    """
    Locust test class for API performance testing.
    """
    @task
    def get_booking(self):
        endpoint = config.get("endpoint", "/api/default")  # Use default if missing
        with self.client.get(endpoint, name="API GET Booking", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Error {response.status_code}")