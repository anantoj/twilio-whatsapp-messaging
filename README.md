# Twilio WhatsApp Messaging

A library for bulk sending WhatsApp messages and automatic custom responses through Twilio's WhatsApp API.

## Installation

1. Clone the repo and Install the required dependencies

```bash
git clone https://github.com/anantoj/twilio-whatsapp-messaging.git
cd twilio-whatsapp-messaging
pip install -r requirements.txt
```

## Usage

1. Create a `.env` file in the root directory of your project and add the following configuration:

```ini
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
WHATSAPP_SENDER=your_whatsapp_sender_number
```

Your twilio account SID and authentication token can be found at your twilio console.

2. Prepare your Excel file
Ensure a column containing phone numbers in E.164 format. Optionally include a "name" column for personalized messages.

3. Setup your Twilio Whatsapp sender and webhook. Refer to the [Twilio Setup](#twilio-setup) section for more info.

4. Ensure you have a JSON file for the mapping of your whatsapp sender in the following format:

```json
{
    "whatsapp_sender1": "phone_number1",
    "whatsapp_sender2": "phone_number2",
    ...
}
```

5. Run the script

```bash
python send_message.py \
  --content_sid "YOUR_CONTENT_SID" \
  --phone_numbers_file "path/to/phone_numbers.xlsx" \
  --column "phones" \
  --sal_column "Sal" \
  --sender_map "whatsapp_sender_map.json" \
  --sender "tere" \
  --messaging_service_sid "YOUR_MESSAGING_SID" \
  --use_names \
```

- `--content_sid`: The Content SID of the WhatsApp message you want to send.
- `--phone_numbers_file`: The path to your Excel file containing phone numbers.
- `--column`: The column number containing phone numbers.
- `--sal_column`: The column number containing salutations in the Excel file.
- `--sender_map`: JSON file containing sender mappings.
- `--sender`: WhatsApp sender name in the sender map.
- `--messaging_service_sid (optional)`: The Messaging Service SID for improved deliverability (requires a Twilio Messaging Service)
- `--use_names`: Use the name information provided on the excel file (optional).
Example:

```bash
python ./twilio_whatsapp_sender.py \
    --content_sid CAXXXXXXXXXXXXXXXXXXXXXXXXXXXX \
    --phone_numbers_file contacts.xlsx \
    --column "phones" \
    --sal_column "Sal" \
    --sender_map "whatsapp_sender_map.json" \
    --sender "whatsapp_sender1" \
    --messaging_service_sid MSXXXXXXXXXXXXXXXXXXXXXXXXXXXX \
    --use_names \
```

or you can just run the sample script:

```bash
sh example_run.sh
```

## Twilio Setup

Before using this library, you'll need to prepare your Twilio account with the necessary settings. If you don't have one already, head over to [console.twilio.com](https://console.twilio.com/) and create a free Twilio account.

In the Twilio Console, navigate to "Project > Settings > General." Find your Account SID and Auth Token. Copy and securely store them, as you'll need them in your .env file later.

### Setup a WhatsApp Sender

There are two options for sending personalized WhatsApp messages:

#### 1. Use Your Own Phone Number

- In the Twilio Console, go to "Messaging > Senders > WhatsApp Senders."
- Click "New WhatsApp Sender" and submit a request using your own phone number.
- This process requires approval from Facebook, which can take some time.
- Once approved, you'll receive a Display Name (for recipient display) and a WhatsApp Identifier (used in the script).

#### 2. Purchase a Twilio Phone Number for WhatsApp

- Navigate to "Numbers > Available Numbers" in the Twilio Console.
- Search for phone numbers with "WhatsApp Capability."
- Purchase a number that suits your needs.
- This number will automatically become a verified WhatsApp sender.
- You'll receive the phone number itself (used in the script).

### Create a Messaging Service

- Navigate to "Messaging > "Services" in the Twilio Console.
- Click "Create Messaging Service".
- You can skip the next setting configurations like adding senders.
- Finally, you'll receive a Messaging Service SID (used in the script).

### Setup your custom webhook

This library doesn't require a custom webhook URL for sending messages.
However, if you want to implement features like receiving responses or using advanced message flows, you might need to set up a webhook endpoint and update the script accordingly. Here's one way you can setup your custom webhook:

#### 1. Create your function in Node.js

There is an example webhook provided in [here](https://github.com/anantoj/harnis_twilio/blob/main/functions/customerOptIn.js).

#### 2. Deploy your function

- In your Twilio console, navigate to "Function and Assets" > "Functions (Classic)" > List.
- Click the "+" button and choose the "blank" template.
- Paste your Node.js function that you have created
- Create your own custom webhook link.
- Go to "Configure" to setup your NPM modules and environment variables

#### 3. Connect the webhook to your WhatsApp Sender

- In the Twilio Console, go to "Messaging > Senders > WhatsApp Senders."
- Click on the sender you want your webhook to be linked to
- In "How would you like to configure this sender?", choose Use webhooks
- Setup your webhook configuration accordingly

Congratulations, now a user messaging to your WhatsApp Sender will immediately trigger a request to your webhook!

**NOTE**: this is just one way of setting up a webhook in Twilio. You can, for instance utilize Services instead of Functions(classic). For the 3rd step shown above, you can also connect the webhook via Messaging Services. You can modify the setup to fit your own use case.
