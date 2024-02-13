# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
from dotenv import dotenv_values

config = dotenv_values(".env")

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = config["TWILIO_ACCOUNT_SID"]
auth_token = config["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)

webhook = client.conversations.v1.conversations(
    config["CONVERSATION_SID"]
).webhooks.create(
    configuration_url=config["WEBHOOK_URL"],
    configuration_method="POST",
    configuration_filters="onMessageAdded",
    target="webhook",
)

print(webhook.sid)
