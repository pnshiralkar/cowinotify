import datetime
import time

import pytz as pytz
import requests

from config import PINCODES_PHONE_NUMBERS, RESEND_SMS_INTERVAL, CHECK_INTERVAL, MOCK_SMS
from sms import send_sms

cache = {}
"""
cache = {
    'pincode': {
        'message': 'message',
        'time': datetime,
    },
    ...
}
"""


def get_time_now():
    tz = pytz.timezone('Asia/Kolkata')
    return datetime.datetime.now(tz=tz)


def check_availability(pincode, date):
    """
    available, message = check_availability('415110', '03-05-2021')
    """
    resp = requests.get(
        f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={pincode}&date={date}"
    )
    # print(resp.json())
    available_in_pincode = False
    message = f'Vaccine available at {pincode}\n\n'
    for center in resp.json()['centers']:
        available = False
        min_18_dates = []
        min_45_dates = []
        for session in center['sessions']:
            if session['available_capacity'] > 0:
                if not available:
                    available = True
                    available_in_pincode = True
                if session['min_age_limit'] <= 18:
                    min_18_dates.append(session['date'])
                elif session['min_age_limit'] <= 45:
                    min_45_dates.append(session['date'])
        if available:
            message += f"\n{center['name']}:\n"
            if len(min_18_dates) > 0:
                message += f"  18+ {min_18_dates}\n"
            if len(min_45_dates) > 0:
                message += f"  45+ {min_45_dates}\n"
    return available_in_pincode, message


def check():
    num_sms_sent = 0
    date = get_time_now().strftime("%d-%m-%Y")
    for pc in PINCODES_PHONE_NUMBERS:
        available, message = check_availability(pc, date)
        if available:
            should_send = False
            if pc not in cache:
                should_send = True
            else:
                delta = get_time_now() - cache[pc]['time']
                if cache[pc]['message'] != message or delta.seconds >= RESEND_SMS_INTERVAL:
                    should_send = True

            if should_send:
                cache[pc] = {
                    'message': message,
                    'time': get_time_now()
                }
                for phone in PINCODES_PHONE_NUMBERS[pc]:
                    num_sms_sent += 1
                    send_sms(phone, message, mock=MOCK_SMS)
    return num_sms_sent


def main():
    while True:
        num_sms_sent = check()
        print(f"Checked at {get_time_now().strftime('%d-%m-%Y %I:%M %p')} : Sent {num_sms_sent} SMS")
        time.sleep(CHECK_INTERVAL)


if __name__ == '__main__':
    main()
