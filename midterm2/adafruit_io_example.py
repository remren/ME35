# Credit: https://www.youtube.com/watch?v=tPRXgzxL100&t=806s

import Adafruit_IO
from Adafruit_IO import RequestError,Client,Feed
ADAFRUIT_IO_USERNAME='remren'
ADAFRUIT_IO_KEY='' # Empty for git push, put in your io key here normally
aio=Client(ADAFRUIT_IO_USERNAME,ADAFRUIT_IO_KEY)
try:
    test=aio.feeds('current-color')
except RequestError:
    test_feed=Feed(name='current-color')
    test_feed=aio.create_feed(test_feed)
aio.send_data(test.key,50)
