import requests
import json
import time
from pushover import init, Client
PUSHOVER_CLIENT_ID = ""
PUSHOVER_API_TOKEN  = ""
URL = "https://api-patient.lumahealth.io/api/scheduler/availabilities?appointmentType=6011f3c4fa2b92009a1c0f43&date=%3E2021-04-05T00%3A00%3A00-04%3A00&date=%3C2021-04-15T23%3A59%3A59-04%3A00&facility=6011f3c1fa2b92009a1c0e24%2C601a236ff7f880001333e993%2C601a236ff7f880001333e993%2C6011f3c1fa2b92009a1c0e2a%2C6011f3c1fa2b92009a1c0e26&includeNullApptTypes=true&limit=100&page=1&patientForm=606aa2ea98a79a0012d274d4&populate=true&provider=601a24ac98d5e900120d2582%2C6011f3c2fa2b92009a1c0e69%2C6011f3c2fa2b92009a1c0e6d%2C6011f3c2fa2b92009a1c0e6b&sort=date&sortBy=asc&status=available"

headers = {
'x-access-token': ''
}

EMPTY = {'page': 1, 'size': 0, 'response': [], 'facilities': [], 'providers': [], 'appointmentTypes': []}

if __name__ == "__main__":
    init(PUSHOVER_CLIENT_ID)
    client = Client(PUSHOVER_API_TOKEN)
    while 1:
        r = requests.get(URL,headers=headers)
        if r.status_code == 200:
            response = r.json()
            if response == EMPTY:                
                time.sleep(5)
            else:
                print(r.content)
                client.send_message(f"Vaccine At Wonderland Available: {json.dumps(response)}", title="VaccineTime!")
        else:
            print("Error %d" % r.status_code)
            break
        time.sleep(5)
