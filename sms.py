import boto3

sns_client = boto3.client('sns', region_name='ap-south-1')

print(sns_client.set_sms_attributes(attributes={
    'DefaultSMSType': 'Transactional',
}))


def send_sms(phone_number, message):
    return sns_client.publish(PhoneNumber=phone_number, Message=message)
