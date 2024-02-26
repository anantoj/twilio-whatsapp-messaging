import os
import argparse
import pandas as pd
from twilio.rest import Client
from dotenv import dotenv_values
import twilio
import json


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
    parser.add_argument(
        "--use_names",
        action="store_true",
        help="Use the name information provided on the excel file (optional)",
    )
    return parser.parse_args()


# TODO: Implement your own logic to extract names from the input excel file
def get_names(df: pd.DataFrame):
    """
    This function takes a Pandas DataFrame with columns "Contact/First Name" and "Contact/Last Name"
    and returns a list of full names using list comprehension.

    Args:
        df: Pandas DataFrame with the specified columns.

    Returns:
        A list of full names.
    """
    return [
        f"{row['Contact/First Name'] if not pd.isna(row['Contact/First Name']) else ''} {row['Contact/Last Name'] if not pd.isna(row['Contact/Last Name']) else ''}"
        for index, row in df.iterrows()
    ]


def send_whatsapp_messages(
    content_sid: str,
    phone_numbers_file: str,
    phone_column: str,
    messaging_service_sid: str,
    use_names: bool = False,
) -> None:
    """
    This function sends personalized WhatsApp messages using Twilio API.

    Args:
        content_sid (str): The SID of the message template to use.
        phone_numbers_file (str): Path to the Excel file containing phone numbers.
        phone_column (str): Name of the column containing phone numbers in the Excel file.
        messaging_service_sid (str): The SID of the Twilio Messaging Service used.
        use_names (bool, optional): Flag to personalize messages using recipient names. Defaults to False.

    Returns:
        None. Prints success/failure messages for each recipient.

    Raises:
        FileNotFoundError: If the phone numbers file is not found.
        KeyError: If required environment variables are not set.
        twilio.base.exceptions.TwilioRestException: For any Twilio API errors.

    Examples:
        >>> send_whatsapp_messages(
            "MGXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "phone_numbers.xlsx",
            "Phone Number",
            "MGXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            use_names=True
        )
    """
    config = dotenv_values(".env")
    account_sid = config["TWILIO_ACCOUNT_SID"]
    auth_token = config["TWILIO_AUTH_TOKEN"]
    client = Client(account_sid, auth_token)

    # Read phone numbers using pandas
    df = pd.read_excel(phone_numbers_file)
    phone_numbers = df[phone_column].values.flatten()
    names = get_names(df)
    for name, phone_number in zip(names, phone_numbers):
        try:
            if use_names:
                message = client.messages.create(
                    content_sid=content_sid,
                    from_=f"whatsapp:{config['WHATSAPP_SENDER']}",
                    to=f"whatsapp:{phone_number}",
                    content_variables=json.dumps({"1": name}),
                    messaging_service_sid=messaging_service_sid,
                )
            else:
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
        args.use_names,
    )
