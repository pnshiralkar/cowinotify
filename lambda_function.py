import time

from config import CHECK_INTERVAL
from check_availability import check, get_time_now


def lambda_handler(a, b):
    num_times = (60 * 1) // CHECK_INTERVAL
    num_times = num_times or 1
    for i in range(num_times):
        num_sms_sent = check()
        print(f"Checked at {get_time_now().strftime('%d-%m-%Y %I:%M:%S %p')} : Sent {num_sms_sent} SMS")
        if i != num_times - 1:
            time.sleep(CHECK_INTERVAL)

