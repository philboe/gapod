#!/bin/python3.5
#
# boeschphil@gmail.com
#
# grabs 'Astronomy Picture of the Day' from the apod homepage
# if apod is not a picture, grabs a random picture from the past year
# tries to set the picture as wallpaper


import os
import datetime 
import requests
import re
import logging
APODURLSTART='http://apod.nasa.gov/apod/ap'
APODURLEND='.html'
REGEX=re.compile(rb"image\/\d{4}\/\w*\.jpg")

def getRunningDesktopSession():
    desktopSession= os.environ.get('DESKTOP_SESSION')
    return desktopSession
    
def extractImageUrls(date):
    pattern=re.compile(r"image\/\d{4}\/\w*\.jpg")
    url=APODURLSTART+str(int(date)-1)+APODURLEND
    logging.warning("opening url"+url)
    website=requests.get(url)
    html=website.text
    imgNames=pattern.findall(html)
    return imgUrls

def downloadFile()

def getRandomPastDate():
    """returns a random date from the past year"""
    return

def getCurrentDate():
    """Returns current date as YYMMDD string"""
    currentDate=datetime.datetime.now().strftime('%y%m%d')
    return currentDate

if __name__ == '__main__':
    logging.warning('started')
    imageUrls
    print(names)

