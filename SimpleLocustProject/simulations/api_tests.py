from simulations.base import BaseUser
from locust import task

class APIUser(BaseUser):
    """
    Locust test class for API performance testing.
    """
    host = "https://restful-booker.herokuapp.com"  #Each test defines its own host

    @task
    def get_booking(self):
        endpoint = "/booking?firstname=Jim"  #Each test defines its own endpoint
        with self.client.get(endpoint, name="API GET Booking", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Error {response.status_code}")
