import datetime

import requests

from sms import send_sms

INTERVAL = 60 * 2
PIN_CODES = ['415110']
SUBSCRIBED_PHONE_NUMBERS = ['+919075577238']


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
            if session['available_capacity'] > -1:   # TODO: change to 0
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
    for pc in PIN_CODES:
        available, message = check_availability(pc, date)
        if available:
            for phone in SUBSCRIBED_PHONE_NUMBERS:
                send_sms(phone, message)


check()
