from locust import FastHttpUser, task, between
import random
import uuid
import time


class EventUser(FastHttpUser):
    wait_time = between(0.1, 0.5)

    duplicate_events = [
        {
            "user_id": "loadtest_user_1",
            "event_type": "purchase",
            "timestamp": "2024-03-16T12:00:00Z",
            "payload": {"product": "A", "price": 100},
        },
        {
            "user_id": "loadtest_user_2",
            "event_type": "click",
            "timestamp": "2024-03-16T12:01:00Z",
            "payload": {"element": "button"},
        },
    ]

    @task(3)
    def send_unique_event(self):
        event = {
            "user_id": str(uuid.uuid4()),
            "event_type": random.choice(["purchase", "view", "click"]),
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "payload": {"item_id": random.randint(1, 1000), "value": random.random()},
        }
        self.send_request(event)

    @task(1)
    def send_duplicate_event(self):
        event = random.choice(self.duplicate_events)
        self.send_request(event)

    def send_request(self, event):
        with self.client.post(
            "/api/v1/ddup_service/events", json=event, catch_response=True
        ) as response:
            if response.status_code == 409:
                if "Duplicate" in response.text:
                    response.success()
                else:
                    response.failure("Unexpected 409 error")
            elif response.status_code != 200:
                response.failure(f"Unexpected status: {response.status_code}")
