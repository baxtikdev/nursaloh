from base64 import b64encode

import requests

from config.settings.base import env

URL = env("URL")
USERNAME = env("USERNAME")
PASSWORD = env("PASSWORD")
credentials = f"{USERNAME}:{PASSWORD}"
encodedCredentials = str(b64encode(credentials.encode("utf-8")), "utf-8")
AUTHORIZATION = {
    "Authorization": f"Basic {encodedCredentials}",
    "Content-Type": "application/json"
}


def sent_sms_base(id, user_code, phone_number):
    data = {
        "messages": [
            {
                "recipient": f"{phone_number}",
                "message-id": f"abc{id}",

                "sms": {
                    "originator": "3700",
                    "content": {
                        "text": f"Ваш проверочный код: {user_code}"
                    }
                }
            }
        ]

    }
    response = requests.post(url=URL, json=data, headers=AUTHORIZATION)
    result = response.status_code
    if result == 200:
        return True
