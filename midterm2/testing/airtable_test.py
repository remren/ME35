import requests
import json

### ! DELETE WHEN PUSHING TO GIT ! ###
airtable_token = ''

fields = []

# BEST TUTORIAL! https://dev.to/matthewvielkind/using-python-and-airtable-3bb7
# /v0/{baseId}/{tableIdOrName}/{recordId}
url = "https://api.airtable.com/v0/appuCYgDyr8AZA6XH/tblGydkwtSmHpa5pY/recMvkcH9nUrHk1KK"
headers = {
           'Authorization':f'Bearer {airtable_token}',
           'Content-Type':'application/json'
          }
reply = requests.request("GET", url, headers=headers)
if reply.status_code == 200:
    reply = reply.json() # JSON array of info
    display(reply)
    # display(reply["fields"])
    # for x in reply['fields']['Notes']:
        # display(x)
    # id = [x['key'] for x in reply]
    # fields = [x['fields']['fields'] for x in reply]

display(reply['fields']['Color'])

update_data = {
                  "fields": {
                      "Color":"HELLO!!!!"
                  }
              }

reply = requests.request("PATCH", url, headers=headers, data=json.dumps(update_data))
display('ran it')