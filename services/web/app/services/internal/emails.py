import requests
from app.core import config


class EmailService:
    def __init__(self, config):
        self.config = config

    def send(self):
        requests.post(
            self.config["EMAIL_SERVICE_URL"],
            json={
                "service_id": self.config["EMAIL_SERVICE_ID"],
                "template_id": self.config["EMAIL_SERVICE_TEMPLATE_ID"],
                "user_id": self.config["EMAIL_SERVICE_USER_ID"],
            },
        )


emailService = EmailService(
    {
        "EMAIL_SERVICE_URL": config.get_settings().EMAIL_SERVICE_URL,
        "EMAIL_SERVICE_ID": config.get_settings().EMAIL_SERVICE_ID,
        "EMAIL_SERVICE_TEMPLATE_ID": config.get_settings().EMAIL_SERVICE_TEMPLATE_ID,
        "EMAIL_SERVICE_USER_ID": config.get_settings().EMAIL_SERVICE_USER_ID,
    }
)
