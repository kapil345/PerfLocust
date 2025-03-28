from simulations.base_api import BaseAPI
from locust import task
from constants.api_constants import BOOKING_ENDPOINTS

class ApiTests(BaseAPI):
    """
    Locust test class for API performance testing
    """

    @task
    def get_booking(self):
        endpoint =  BOOKING_ENDPOINTS["GET_BOOKING"]  
        full_url = f"{self.host}{endpoint}"
        print(f"\n API Test: GET {full_url}")
        with self.client.get(endpoint, name="GET Booking Test", catch_response=True) as response:
            if response.status_code == 200:
                 print(f" Success: ${self.host}${endpoint}")
                 response.success()
            else:
                print(f"Failure ({response.status_code}): {self.host}{endpoint}")
                response.failure(f"Error {response.status_code}")
