from locust import HttpUser, task, between

class WordPressUser(HttpUser):
    wait_time = between(1, 2.5)

    @task(1)
    def load_300kb_picture(self):
        self.client.get("/?p=8")

    @task(2)
    def load_1mb_picture(self):
        self.client.get("/?p=5")

    @task(3)
    def load_400kb_text(self):
        self.client.get("/?p=11")
