import requests
import json
from pushover import Client 
import time
import sys

PUSHOVER_API_TOKEN = ""
PUSHOVER_CLIENT_ID = ""

DATE_LST = [
    "12/17/2020",
    "12/18/2020"
]

def check_date_avail(start_date,end_date):
    header = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
    "cookie": "",
    "channelname": "WEB",
    "grid": "",
    "appname": "MCL_WEB",
    "x-distil-ajax": "",
    
  
    }
    payload = { 
        "request":{
            "header":{
                "lineOfBusiness":"RETAIL",
                "appName":"CVS_APP",
                "apiKey":"",
                "channelName":"WEB",
                "deviceToken":"",
                "deviceType":"DESKTOP",
                "responseFormat":"JSON",
                "securityType":"apiKey",
                "source":"CVS_WEB",
                "type":"retleg"
            },
            "startDate":start_date,
            "endDate":end_date,
            "visitCode":"48",
            "clinicId":"2732"
        }
    }
    r = requests.post("https://www.cvs.com/RETAGPV3/scheduler/V3/getAvailableSlots",headers=header,json=payload)
    
    if(r.status_code == 200):
        data = r.json()
        print(data)
        if(data['response']['header']['statusDesc'] != 'Success'):
            return False,""
        if(data['response']['details'][0]['availableSlots'] != []):
            return True,json.dumps(data['response']['details'][0])

        if(data['response']['details'][1]['availableSlots'] != []):
            return True,json.dumps(data['response']['details'][1])    

        if(data['response']['details'][2]['availableSlots'] != []):
            return True,json.dumps(data['response']['details'][2])              
        return False,""
    else:
        print("Error - %d" % r.status_code)
        return False,""
      
if __name__ == "__main__":
    client = Client(PUSHOVER_CLIENT_ID, api_token=PUSHOVER_API_TOKEN)
    while 1:
        status,data = check_date_avail("12/17/2020","12/17/2020")      
        if(status == True):
            client.send_message(data, title="CVS Appt Available!")
            print("Appt Available!")
            print(data)
            sys.exit(0)
        time.sleep(10)
        