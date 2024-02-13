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

message = client.conversations.v1.conversations(
    config["CONVERSATION_SID"]
).messages.create(
    author=f"whatsapp:{config["MARKETING_NUMBER"]}",
    content_sid=config["TEMPLATE_CONTENT_SID"],
)

print(message.sid)
