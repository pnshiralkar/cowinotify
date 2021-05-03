import datetime
import time

import requests

from sms import send_sms

INTERVAL = 60 * 1
RESEND_SMS_INTERVAL = 60 * 3

PINCODES_PHONE_NUMBERS = {
    '000000': ['+911234567890']
}

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
            if session['available_capacity'] > -1:  # TODO: change to 0
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
    date = datetime.datetime.now().strftime("%d-%m-%Y")
    for pc in PINCODES_PHONE_NUMBERS:
        available, message = check_availability(pc, date)
        if available:
            should_send = False
            if pc not in cache:
                should_send = True
            else:
                delta = datetime.datetime.now() - cache[pc]['time']
                if cache[pc]['message'] != message or delta.seconds >= RESEND_SMS_INTERVAL:
                    print(cache[pc]['message'] != message, delta.seconds >= RESEND_SMS_INTERVAL)
                    should_send = True

            if should_send:
                cache[pc] = {
                    'message': message,
                    'time': datetime.datetime.now()
                }
                for phone in PINCODES_PHONE_NUMBERS[pc]:
                    send_sms(phone, message, mock=True)


def main():
    while True:
        check()
        time.sleep(INTERVAL)


if __name__ == '__main__':
    main()
