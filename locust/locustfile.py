from locust import FastHttpUser, task, between, events
from datetime import datetime, timezone
import random
import uuid
import json
import logging


class EventUser(FastHttpUser):
    wait_time = between(0.1, 0.5)
    connection_timeout = 10.0
    network_timeout = 30.0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.duplicates_sent = 0
        self.uniques_sent = 0

    @events.init.add_listener
    def setup(environment, **kwargs):
        logging.info("Load test initialization complete")

    @task(4)
    def send_unique_event(self):
        event = self.generate_unique_event()
        self.send_request(event, is_duplicate=False)

    @task(1)
    def send_duplicate_event(self):
        event = random.choice(self.duplicate_events)
        self.send_request(event, is_duplicate=True)

    def generate_unique_event(self):
        return {
            "user_id": str(uuid.uuid4()),
            "event_type": random.choice(
                ["purchase", "view", "click", "add_to_cart", "remove_from_cart"]
            ),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "payload": {
                "item_id": random.randint(1, 10000),
                "price": round(random.uniform(1.0, 1000.0), 2),
                "currency": random.choice(["USD", "EUR", "GBP"]),
                "platform": random.choice(["web", "mobile", "tablet"]),
            },
        }

    def send_request(self, event, is_duplicate):

        with self.client.post(
            "/api/v1/ddup_service/events",
            json=event,
            catch_response=True,
            name=("DUPLICATE" if is_duplicate else "UNIQUE"),
        ) as response:
            self.handle_response(response, event, is_duplicate)

    def handle_response(self, response, event, is_duplicate):
        expected_status = 409 if is_duplicate else 202

        if response.status_code == expected_status:
            response.success()
            if is_duplicate:
                self.duplicates_sent += 1
            else:
                self.uniques_sent += 1
        else:
            self.log_error(response, event)

    def log_error(self, response, event):
        error_info = {
            "status": response.status_code,
            "error": response.text,
            "event": json.dumps(event),
            "headers": dict(response.headers),
        }
        logging.error(json.dumps(error_info))

    @property
    def duplicate_events(self):
        return [
            {
                "user_id": "loadtest_duplicate_user",
                "event_type": "purchase",
                "timestamp": "2024-01-01T00:00:00Z",
                "payload": {"product": "TEST", "price": 100.0},
            }
        ]
