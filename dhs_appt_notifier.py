import json
import time
import argparse

import http.client
import urllib.parse

from sms_notifier.sms_notifier import SMSNotifier
from pathlib import Path
from datetime import datetime

DHS_HOST = 'ttp.cbp.dhs.gov'
DT_FORMAT = '%Y-%m-%dT%H:%M'
SMS_NOTIFIER_CONFIG_PATH = Path.home().joinpath('.smsnotifier.conf')
RETRY_TIME_SECONDS = 600


def check_appointment(location_id, end_year, end_month):
    available = False
    dt = ""
    connection = http.client.HTTPSConnection(DHS_HOST)
    schedule_params = {
        'orderBy': 'soonest',
        'locationId': location_id,
        'limit': 1,
        'minimum': 1
    }
    uri = f'/schedulerapi/slots?{urllib.parse.urlencode(schedule_params)}'
    connection.request("GET", uri)
    response = connection.getresponse()
    if response.status == 200:
        d = json.loads(response.read())
        ts = datetime.strptime(d[0]['startTimestamp'], DT_FORMAT)
        if ts.year <= end_year and ts.month <= end_month:
            dt = datetime.strftime(ts, '%A %B %d @ %H:%M')
            available = True
    return available, dt


def send_notification(number, carrier, data):
    sn = SMSNotifier(SMS_NOTIFIER_CONFIG_PATH)
    subject = 'DHSNotifier'
    body = f'Appointment Available on: {data}'
    sn.send_notification(number, carrier, subject, body)


def init_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("location_id", type=int, help='The location ID of a DHS interview site (e.g. 5441 - Boston)')
    parser.add_argument("cutoff_year", type=int, help='The latest year a desired appointment is available.')
    parser.add_argument("cutoff_month", type=int, help='The latest month a desired appointment is available.')
    parser.add_argument("sms_phone_number", type=str, help='A phone number to send the notification to.')
    parser.add_argument("sms_phone_carrier", type=str, help='The phone carrier belonging to the phone number.')
    return parser.parse_args()


if __name__ == "__main__":
    args = init_args()
    while True:
        appointment_available, appointment_datetime = check_appointment(args.location_id, args.cutoff_year,
                                                                        args.cutoff_month)
        if appointment_available:
            send_notification(args.sms_phone_number, args.sms_phone_carrier,
                              appointment_datetime)
            break
        time.sleep(RETRY_TIME_SECONDS)
