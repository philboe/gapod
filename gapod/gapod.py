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
from gi.repository import Notify

FIRSTAPOD = '19950616'
APODURLSTART = 'http://apod.nasa.gov/apod/ap'
APODURLEND = '.html'
WALLPAPERDIR = '/Pictures/Wallpapers/'


def getNewWallpaper():

    logging.info("get environmet variables for home and desktop session")
    desktopSession, home = getEnvironmentVars()
    wallpaperPath = home+WALLPAPERDIR
    logging.info("get current date")
    currentDate = getCurrentDate()
    logging.info("extracting possible image urls from apod site for currentDate="+currentDate)
    imgUrls, html = extractImageUrlsAndHtml(currentDate)
    logging.info("Find biigest file of %d images", len(imgUrls))
    apodText = getApodText(html)
    filepath = getBiggestFile(imgUrls, wallpaperPath)
    apodText = getApodText(html)
    save_apodText(wallpaperPath,apodText)
    logging.info("Downloaded file %s, try to set it as wallpaper", filepath)
    setNewBackground(filepath, desktopSession)
    sendNotification(apodText)




def setNewBackground(filepath, desktopSession):
    """sets Wallpaper acording to desktop session"""
    logging.info('your WM is ' + desktopSession)
    if 'gnome' or 'ubuntu' in desktopSession:
        os.system("gsettings set org.gnome.desktop.background picture-uri file:"+filepath)
        os.system("gsettings set org.gnome.desktop.background picture-options stretched")
    if 'openbox' or 'bspwm' in desktopSession:
        os.system("feh --bg-fill "+filepath)
    if 'sway' in desktopSession:
        logging.info(' setting wallpaper in swaywm')
        os.system("swaymsg output \"*\" background " + filepath+' fill')


def getEnvironmentVars():
    """get environment vaiables from os"""
    desktopSession = os.environ.get('DESKTOP_SESSION')
    home = os.environ.get('HOME')
    return desktopSession, home


def extractImageUrlsAndHtml(date):
    """searches for valid picture (jpg) urls"""
    imgUrls = []
    logging.info(date)
    pattern = re.compile(r"image\/\d{4}\/\w*\.jpg")
    url = APODURLSTART+str(date)+APODURLEND
    logging.info("opening url "+url)
    website = requests.get(url)
    html = website.text
    imgUrls = pattern.findall(html)
    logging.info("found images "+str(len(imgUrls)))
    if imgUrls:
        return imgUrls, html
    else:
        extractImageUrlsAndHtml(getRandomPastDate())


def getBiggestFile(imgUrls, wallpaperPath):
    """assuming that the biggest file has the highest resolution, we take the bigest file"""
    files = {}
    for imgUrl in imgUrls:
        response = requests.head(APODURLSTART[:-2]+imgUrl)
        files.update({imgUrl: response.headers.get('Content-Length')})
        logging.info(imgUrl+" filesize is "+response.headers.get('Content-Length'))
    biggestFile = max(files, key=lambda k: int(files[k]))
    filepath = wallpaperPath+biggestFile[11:]
    logging.info("Biggest File is " + biggestFile[11:])
    if not os.path.isfile(filepath):
        logging.info("starting download of "+APODURLSTART[:-2]+biggestFile)
        image = requests.get(APODURLSTART[:-2]+biggestFile)
        if image.status_code == 200:
            logging.info("status ok, startng to write file at "+filepath)
            with open(filepath, 'wb') as newWallpaper:
                newWallpaper.write(image.content)
                logging.info("file written at "+filepath)
            del image
    else:
        logging.info('file already exists at '+filepath)
    return filepath


def getApodText(html):
    """Searches and returns for the Title of the current picture"""
    pattern = re.compile(r"<b>\s(.+)\s\<\/b\>\s\<br>")
    apodText = pattern.findall(html)
    logging.info('short description of todays picture is ' + apodText[0])
    return apodText[0]


def save_apodText(filepath, apodText):
    logging.info('saving description for later use')
    with open(filepath+'current.txt','w') as descFile:
        descFile.write(apodText+'\n')


def sendNotification(apodText):
    """ if available, tries to send notification with libnotify gobject binding"""
    Notify.init("GAPOD")
    notification = Notify.Notification.new('Astronomy Picture of the Day', apodText)
    notification.set_timeout(Notify.EXPIRES_NEVER)
    notification.show()


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
