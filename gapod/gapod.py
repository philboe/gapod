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
import random
import subprocess


FIRSTAPOD = '19950616'
APODURLSTART = 'http://apod.nasa.gov/apod/ap'
APODURLEND = '.html'
REGEX = re.compile(rb"image\/\d{4}\/\w*\.jpg")
WALLPAPERDIR = '/Pictures/Wallpapers/'


def getNewWallpaper():
    logging.info("get environmet variables for home and desktop session")
    desktopSession, home = getEnvironmentVars()
    wallpaperPath = home+WALLPAPERDIR
    logging.info("get current date")
    currentDate = getCurrentDate()
    logging.info("extracting possible image urls from apod site for currentDate="+currentDate)
    imgUrls = extractImageUrls(currentDate)
    logging.info("Find biigest file of %d images",len(imgUrls))
    filepath = getBiggestFile(imgUrls, wallpaperPath)
    logging.info("Downloaded file %s, try to set it as wallpaper",filepath )
    setNewBackground(filepath, desktopSession)


def setNewBackground(filepath, desktopSession):
    if 'gnome' in desktopSession:
        os.system("gsettings set org.gnome.desktop.background picture-uri file:"+filepath)
        os.system("gsettings set org.gnome.desktop.background picture-options stretched") 
    elif 'openbox'||'bspwm' in desktopSession:
        os.system("feh --bg-fill "+filepath)
    print(filepath, desktopSession)



def getEnvironmentVars():
    desktopSession = os.environ.get('DESKTOP_SESSION')
    home = os.environ.get('HOME')
    return desktopSession, home


def extractImageUrls(date):
    imgUrls = []
    logging.info(date)
    pattern = re.compile(r"image\/\d{4}\/\w*\.jpg")
    url = APODURLSTART+str(date)+APODURLEND
    logging.warning("opening url "+url)
    website = requests.get(url)
    html = website.text
    imgUrls = pattern.findall(html)
    logging.info("found images "+str(len(imgUrls)))
    if imgUrls:
        return imgUrls
    else:
        extractImageUrls(getRandomPastDate())


def getBiggestFile(imgUrls, wallpaperPath):
    """assuming that the biggest file has the highest resolution, we take the bigest file"""
    files = {}
    for imgUrl in imgUrls:
        response = requests.head(APODURLSTART[:-2]+imgUrl)
        files.update({imgUrl: response.headers.get('Content-Length')})
        logging.info(imgUrl[1]+" filesize is "+response.headers.get('Content-Length'))
    biggestFile = max(files, key=lambda k: files[k])
    logging.info("Biggest File is " + biggestFile[11:])
    logging.info("starting download of "+APODURLSTART[:-2]+biggestFile)
    image = requests.get(APODURLSTART[:-2]+biggestFile)
    logging.info(image.status_code)
    if image.status_code == 200:
        filepath = wallpaperPath+biggestFile[11:]
        logging.info("status ok, startng to write file at "+filepath)
        with open(filepath, 'wb') as newWallpaper:
            newWallpaper.write(image.content)
            logging.info("file written at "+filepath)
        del image
    return filepath


def getRandomPastDate(start=FIRSTAPOD):
    """returns a random date from FIRSTAPOD (16.06.1995) to today-2 """
    endTime = datetime.datetime.now()
    startTime = datetime.datetime.strptime(start, '%Y%m%d')
    randomPastDate = (startTime+datetime.timedelta(((endTime-startTime)*random.random()).days)).strftime('%y%m%d')
    return randomPastDate


def getCurrentDate():
    """Returns current date as YYMMDD string"""
    currentDate = datetime.datetime.now().strftime('%y%m%d')
    return currentDate

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info('started')
    getNewWallpaper()
