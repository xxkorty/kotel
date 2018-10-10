import datetime

import pytz


def shop_is_open(tz='Europe/Prague'):
    tz = pytz.timezone(tz)
    time_now = datetime.datetime.now(tz).time()

    #here we could apply any timezone according shop geo location
    time_day = datetime.time(9, 45, tzinfo=tz)
    time_night = datetime.time(20, 30, tzinfo=tz)
    
    is_open = False
    
    if time_now >= time_day and time_now <= time_night:
        is_open = True
        print ("day")
        return is_open
    else:
      print("night") 

shop_is_open()
