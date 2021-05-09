import time

from config import CHECK_INTERVAL
from check_availability import check, get_time_now


def main():
    while True:
        num_sms_sent = check()
        print(f"Checked at {get_time_now().strftime('%d-%m-%Y %I:%M %p')} : Sent {num_sms_sent} SMS")
        time.sleep(CHECK_INTERVAL)


if __name__ == '__main__':
    main()
