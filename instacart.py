import requests
import time
from sms_notifier import SMSNotifier

from pushover import init, Client


SMS_NOTIFIER_CONFIG_PATH = 'smsnotifier.conf'
RETRY_TIME_SECONDS = 60
url = "https://www.instacart.com/v3/containers/market-basket/next_gen/retailer_information/content/delivery"

NDT = b"All delivery windows are full"
SANITY_CHECK = b"initial_step"

headers = {
	'cookie':"ahoy_visitor=1b93d916-4ba0-4cec-b436-85879c6e713e; ajs_group_id=null; ajs_anonymous_id=%22dbfd02a9-f442-4fbf-9522-15f7fb42b21c%22; node_ssr_initial_bundle=true; _instacart_logged_in=1; __stripe_mid=f2a39530-a128-49d9-a8a5-d62d16798b66; ab.storage.userId.6f8d91cb-99e4-4ad7-ae83-652c2a2c845d=%7B%22g%22%3A%2233846564%22%2C%22c%22%3A1581462678406%2C%22l%22%3A1581462678406%7D; ab.storage.deviceId.6f8d91cb-99e4-4ad7-ae83-652c2a2c845d=%7B%22g%22%3A%2227b002ca-fbc0-10ed-1be1-b58fa4a9da89%22%2C%22c%22%3A1581462678410%2C%22l%22%3A1581462678410%7D; ajs_user_id=%2233846564%22; ahoy_track=true; amplitude_idundefinedinstacart.com=eyJvcHRPdXQiOmZhbHNlLCJzZXNzaW9uSWQiOm51bGwsImxhc3RFdmVudFRpbWUiOm51bGwsImV2ZW50SWQiOjAsImlkZW50aWZ5SWQiOjAsInNlcXVlbmNlTnVtYmVyIjowfQ==; ahoy_visit=d8feb083-2d1e-44dd-9193-7161a4d8e2b8; __stripe_sid=e19bed7c-841e-4ec1-a56d-42a8577ae6db; ubvt=73.119.6.2121586615927816477; build_sha=5abf6f0801c05ce9bf240557ce738b251d482fcb; ab.storage.sessionId.6f8d91cb-99e4-4ad7-ae83-652c2a2c845d=%7B%22g%22%3A%22f85b316a-89f8-8e01-e969-d9319300a3e7%22%2C%22e%22%3A1586614634104%2C%22c%22%3A1586612630853%2C%22l%22%3A1586612834104%7D; forterToken=d34058ed5a694608886314add5bc52fa_1586612833415_887_UAL9_9ck; amplitude_id_b87e0e586f364c2c189272540d489b01instacart.com=eyJkZXZpY2VJZCI6ImFhOGRiZGZhLTA4NmMtNDkzZC04ZDQ4LTE3YjE5MDMxM2I5ZFIiLCJ1c2VySWQiOiIzMzg0NjU2NCIsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTU4NjYxMjYzMTY2MiwibGFzdEV2ZW50VGltZSI6MTU4NjYxMjgzNTU1NywiZXZlbnRJZCI6MTMxMiwiaWRlbnRpZnlJZCI6OTMsInNlcXVlbmNlTnVtYmVyIjoxNDA1fQ==; _instacart_session=N1doOFFPM3JPSTc4Q3c0ZkFRM3Z5OUx4U05jL1RjZ3NuN2VpeW8rL0lQUzFrVTRCRHFrL3NFRFVsV3h5ekJGcE5VM3V0NzlIK0RNcmVad3FkM0MvMUh1WjVBVGNzSjF0eTFKUU96K1MrWmRwNFFmcHNEOU0wVEdoaDBnNUFlUzViQnV1NlIzRlJwSjkxcjZ5V1ZvUW5IQ2ZNNStzQSs3dHErSTVwdDRPZ2ZBMkN3RUtjQWdyYkI2elR1WlN2SFhyV2w1S2tia05WQTRsUHVWUm01LytYSWd1TG14NzhwYXFxUHNOZGVkemZka1k1a1BCakIvRFhOTVp6Yll6MTAvT3NiVHhMenNxSmJlc0lrekJJbitlNjRaeFAxejdmNlJIS2tpR3ZCLzFncGpESkJwRUtwZ21mN2dSc1pBMk5YVWEvOEFQdXRMYzU4b2cwWHlHb2NqU1ZGVXkyMXRCa2dMRWVGdnRFZnREMGhzPS0tZDNWYUhic0ZWTk5LMmdiL1g5cVRXZz09--3d9d921eb0083de2ab4c9d6a92e5bdf85ceddcf6",
	'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
}

def send_notification(number, carrier):
    sn = SMSNotifier(SMS_NOTIFIER_CONFIG_PATH)
    subject = 'Instacart'
    body = 'Delivery Times might be available.'
    sn.send_notification(number, carrier, subject, body)


def check_delivery_times():
	r = requests.get(url, headers=headers)

	if r.status_code == 200:
		if SANITY_CHECK in r.content:
			if NDT in r.content:
				print("No Delivery Times Available")
			else:
				print("Delivery Times might be Available")
				print(r.content)
				return True
	return False

if __name__=="__main__":
	avail = False
	while not avail:
		avail = check_delivery_times()
		if avail:
			#send_notification('5186496224','at&t')
			init("aqak974uu8m4cxo2dzveuqgx76w5bh")
			Client("ukskt1ptqmh95ctmjca65hyjjd6v2s").send_message("Deliveries Available!", title="Instacart Available")
			break
		time.sleep(RETRY_TIME_SECONDS)
