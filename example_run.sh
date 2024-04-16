#!/bin/bash

# Replace these placeholders with your actual values
python send_message.py \
  --content_sid "YOUR_CONTENT_SID" \
  --phone_numbers_file "path/to/phone_numbers.xlsx" \
  --column "phones" \
  --sal_column "Sal" \
  --sender_map "whatsapp_sender_map.json" \
  --sender "tere" \
  --messaging_service_sid "YOUR_MESSAGING_SID" \
  --use_names \

