# Exercise 10.4 — Performance & Load testing for the ESBot REST API.
#
# This Locust file exercises the *non-LLM* endpoints only (health, session CRUD,
# message history) so that results are deterministic and reproducible without a
# live AI inference engine. Run the backend with LLM_PROVIDER=mock.
#
# Usage examples (see docs/api/performance/report.md for the three profiles):
#
#   # Smoke test (1-2 users, short)
#   locust -f locustfile.py --headless -u 2 -r 2 -t 30s \
#       --host http://localhost:8000 --html smoke.html
#
#   # Load test (NFR: 50 users, 60s ramp-up, 5 min sustained)
#   locust -f locustfile.py --headless -u 50 -r 1 -t 5m \
#       --host http://localhost:8000 --html load.html
#
#   # Stress test (ramp 50 -> 200+ users)
#   locust -f locustfile.py --headless -u 200 -r 1 -t 10m \
#       --host http://localhost:8000 --html stress.html

from locust import HttpUser, task, between


class ESBotUser(HttpUser):
    """Simulates a client browsing sessions and reading message history."""

    # Think time between requests, in seconds.
    wait_time = between(0.1, 0.5)

    def on_start(self):
        """Each virtual user creates one session to operate on."""
        self.session_id = None
        response = self.client.post(
            "/api/v1/sessions",
            json={"user_id": "loadtest", "title": "perf"},
            name="POST /sessions",
        )
        if response.status_code == 200:
            self.session_id = response.json().get("id")

    @task(5)
    def health(self):
        """Liveness check — the cheapest endpoint, highest weight."""
        self.client.get("/api/v1/health", name="GET /health")

    @task(3)
    def list_sessions(self):
        self.client.get(
            "/api/v1/sessions?user_id=loadtest", name="GET /sessions"
        )

    @task(2)
    def get_messages(self):
        if self.session_id is not None:
            self.client.get(
                f"/api/v1/sessions/{self.session_id}/messages",
                name="GET /sessions/{id}/messages",
            )

    @task(1)
    def create_session(self):
        self.client.post(
            "/api/v1/sessions",
            json={"user_id": "loadtest", "title": "perf"},
            name="POST /sessions",
        )
