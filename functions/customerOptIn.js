const os = require('os');

exports.handler = function (context, event, callback) {
    const whatsAppSender = os.environ.WHATSAPP_SENDER;
    const contentSid = os.environ.TEMPLATE_CONTENT_SID;
    const marketingNumber = os.environ.MARKETING_NUMBER;
    const messagingServiceSid = os.environ.MESSAGING_SERVICE_SID;

    const client = context.getTwilioClient();
    const from = event.From;

    const customerNumber = from.replace('whatsapp:', '');
    const customerName = event.ProfileName
    const buttonPressed = event.ButtonText

    client.messages.create({
        contentSid: contentSid,
        from: whatsAppSender,
        contentVariables: JSON.stringify({
            1: customerNumber,
            2: buttonPressed
        }),
        messagingServiceSid: messagingServiceSid,
        to: marketingNumber
    })
        .then(message => console.log(message.sid))
        .catch(error => console.error(error));
    console.log("Successfully sent message to Marketing Number.")
};