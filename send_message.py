import os
import argparse
import pandas as pd
from twilio.rest import Client
from dotenv import dotenv_values
import twilio


def parse_args():
    parser = argparse.ArgumentParser(description="Send WhatsApp messages using Twilio")
    parser.add_argument("--content_sid", help="The content SID to use for the messages")
    parser.add_argument(
        "--phone_numbers_file",
        help="The path to the Excel file containing phone numbers",
    )
    parser.add_argument(
        "--column",
        type=str,
        help="The column number containing phone numbers (1-based)",
    )
    parser.add_argument(
        "--messaging_service_sid", help="The messaging service SID (optional)"
    )
    return parser.parse_args()


def send_whatsapp_messages(
    content_sid, phone_numbers_file, phone_column, messaging_service_sid
):
    config = dotenv_values(".env")
    account_sid = config["TWILIO_ACCOUNT_SID"]
    auth_token = config["TWILIO_AUTH_TOKEN"]
    client = Client(account_sid, auth_token)

    # Read phone numbers using pandas
    df = pd.read_excel(phone_numbers_file)

    for phone_number in df[phone_column].values.flatten():
        try:
            message = client.messages.create(
                content_sid=content_sid,
                from_=f"whatsapp:{config['WHATSAPP_SENDER']}",  
                to=f"whatsapp:{phone_number}",
                messaging_service_sid=messaging_service_sid, 
            )
            # TODO: implement case with name template
            print(f"Message sent to {phone_number} (SID: {message.sid})")
        except twilio.base.exceptions.TwilioRestException as e:
            print(f"Error sending message to {phone_number}: {e}")


if __name__ == "__main__":
    args = parse_args()

    send_whatsapp_messages(
        args.content_sid,
        args.phone_numbers_file,
        args.column,
        args.messaging_service_sid,
    )
