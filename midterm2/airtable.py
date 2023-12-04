import requests
import json

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

update_data = {
                  "fields": {
                      "Color": f"{largest_color}"
                  }
              }

reply = requests.request("PATCH", url, headers=headers, data=json.dumps(update_data))
display('Sent!')

reply = requests.request("GET", url, headers=headers)
if reply.status_code == 200:
    reply = reply.json() # JSON array of info
    display("Read!")
    display(reply)
    airtable_color = reply["fields"]["Color"]
    display(f"Color from AirTable: {airtable_color}")
