#!/bin/python3.5
#
# boeschphil@gmail.com
#
# grabs 'Astronomy Picture of the Day' from the apod homepage
# if apod is not a picture, grabs a random picture from the past year
# tries to set the picture as wallpaper


import os
import datetime 

def getRunningDesktopSession:
    desktopSession=if os.environ.get('DESKTOP_SESSION') else 'none'
    return desktopSession
    
   

def getRandomPastDate:
    """returns a random date from the past year"""
    return

def getCurrentDate:
    """Returns current date as YYMMDD string"""
    currentDate=datetime.datetime.now().strftime('%y%m%d')
    return currentDate


