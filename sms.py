import os

import boto3

sns_client = boto3.client('sns',
                          region_name='ap-south-1',
                          aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID", None),
                          aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY", None),
                          )

sns_client.set_sms_attributes(attributes={
    'DefaultSMSType': 'Transactional',
})

print("AWS SDK setup successful")


def send_sms(phone_number, message, mock=False):
    if mock:
        print(phone_number, message, flush=True)
    else:
        return sns_client.publish(PhoneNumber=phone_number, Message=message)
