from locust import HttpUser, task, between

class SimpleUser(HttpUser):
    wait_time = between(1, 3)
    host = "https://restful-booker.herokuapp.com"

    @task
    def get_bookings(self):
        self.client.get("/booking?firstname=Jim")

