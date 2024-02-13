import os
from twilio.rest import Client
from dotenv import dotenv_values

config = dotenv_values(".env")
# Replace with your actual Account SID and Auth Token
account_sid = config["TWILIO_ACCOUNT_SID"]
auth_token = config["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)

# Replace with your approved WhatsApp template content SID
template_content_sid = config["TEMPLATE_CONTENT_SID"]

def create_customer_conversation(customer_number):
    """
    Creates a new conversation for a customer, sends an initial message,
    and sets up a webhook.

    Args:
        customer_number (str): The phone number of the customer in E.164 format.

    Returns:
        str: The conversation SID.
    """

    conversation = client.conversations.v1.conversations.create()

    # Do not add marketing number initially
    print(type(conversation.sid))

    participant = client.conversations.v1.conversations(
        conversation.sid
    ).participants.create(
        messaging_binding_address=customer_number,
        messaging_binding_proxy_address=config["WHATSAPP_SENDER"],
    )
    message = client.conversations.v1.conversations(conversation.sid).messages.create(
        author=config["WHATSAPP_SENDER"], body="Ahoy there!"
    )
    print(message.sid)

    client.conversations.v1.conversations(conversation.sid).webhooks.create(
        configuration_url=config["WEBHOOK_URL"],
        configuration_method="POST",
        configuration_filters="onMessageAdded",
        target="webhook",
    )

    return conversation.sid


def main():
    # Your customer list
    customer_list = [config["CUSTOMER_NUMBER"]]
    # TODO: implement multiple number inputs

    for customer_number in customer_list:
        conversation_sid = create_customer_conversation(customer_number)
     


if __name__ == "__main__":
    main()
