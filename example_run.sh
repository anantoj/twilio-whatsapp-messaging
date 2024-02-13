#!/bin/bash

# Replace these placeholders with your actual values
python send_message.py \
  --content_sid "YOUR_CONTENT_SID" \
  --phone_numbers_file "path/to/phone_numbers.xlsx" \
  --column "phones" \
  --messaging_service_sid "YOUR_MESSAGING_SID" \