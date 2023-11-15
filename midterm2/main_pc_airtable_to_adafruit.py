# Credit: https://www.youtube.com/watch?v=tPRXgzxL100&t=806s
# Utilizes the same mqtt on the backend.

import Adafruit_IO
from Adafruit_IO import RequestError,Client,Feed

ADAFRUIT_IO_USERNAME='remren'
ADAFRUIT_IO_KEY='aio_KREH423KtBAWVsm6LTNhaeplYxUQ'

aio=Client(ADAFRUIT_IO_USERNAME,ADAFRUIT_IO_KEY)

def send_color(color):
    try:
        test=aio.feeds('current-color')
    except RequestError:
        test_feed=Feed(name='current-color')
        test_feed=aio.create_feed(test_feed)
    aio.send_data(test.key, color)

import requests
import json
import time

### ! DELETE WHEN PUSHING TO GIT ! ###
airtable_token = 'patpIAzceXZY5dEX7.f943211123e4b6f6745be734de43c2d80defd584d92470533a260eda306431a9'

fields = []

# BEST TUTORIAL! https://dev.to/matthewvielkind/using-python-and-airtable-3bb7
# /v0/{baseId}/{tableIdOrName}/{recordId}
url = "https://api.airtable.com/v0/appuCYgDyr8AZA6XH/tblGydkwtSmHpa5pY/recMvkcH9nUrHk1KK"
headers = {
           'Authorization':f'Bearer {airtable_token}',
           'Content-Type':'application/json'
          }

i = 0
while True:
    print(f"running:{i}")
    reply = requests.request("GET", url, headers=headers)
    if reply.status_code == 200:
        reply = reply.json() # JSON array of info
        airtable_color = reply["fields"]["Color"]
        send_color(airtable_color)
    i += 1
    time.sleep(5)
