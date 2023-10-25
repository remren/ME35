import urequests as requests

url = "https://worldtimeapi.org/api/timezone/America/New_York"
reply = requests.get(url)
print(reply)