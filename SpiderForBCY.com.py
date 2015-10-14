import urllib2
import urllib
import socket
import re
import os
import time
import sys

def getAllWorkPageHTML(url):
    req = urllib2.Request(url, headers={ 'User-Agent': '' })
    html = urllib2.urlopen(req).read()
    return html

def getCurrentPageWorks(html):
    worksReg = re.compile('<a href="(.+?)" target="_blank" title=".*?">')
    works = re.findall(worksReg, html)

    for work in works:
        print 'Found work urls: ' + work

    return works

def getLikeCount(html):
    likeReg = re.compile(r'<div class="btn btn--pink btn--zan btn--base-border-radius js-zan" data-zan="(\d+?)">')
    like = re.findall(likeReg, html)

    for l in like:
        print 'Like: %s' % l

    return like[0]

def getTitle(html):
    titleReg = re.compile('<h1 class="js-post-title">(.+?)</h1>', re.S)
    title = re.findall(titleReg, html)

    for t in title:
        print 'Title: ' + t.decode('utf8')

    return title[0].decode('utf8')

def getDate(html):
    dateReg = re.compile('<span style="line-height: 24px;">.+?\d+?P\D*?(\d.+?) .+?\D*?</span>', re.S)
    date = re.findall(dateReg, html)

    for d in date:
        print 'Date: ' + d;

    return date[0];

def getWorkHTML(url):
    baseUrl = 'http://bcy.net'
    req = urllib2.Request(baseUrl + url, headers={'User-Agent': ''})
    html = urllib2.urlopen(req).read()

    return html

def getWorkPictures(html, directoryName):
    postContentReg = re.compile(r'<div class="post__content js-content-img-wrap js-fullimg js-maincontent mb20">.*?<div class="declaration fz14 mt30">', re.S)
    postContent = re.findall(postContentReg, html)[0]

    pictureUrlsReg = re.compile(r"src='(.+?)/\w+?'")
    pictureUrls = re.findall(pictureUrlsReg, postContent)

    for pictureUrl in pictureUrls:
        print 'Found picture url: ' + pictureUrl

        pictureNameReg = re.compile(r'/(\w*\.\w*)$')
        pictureName = re.findall(pictureNameReg, pictureUrl)[0]
        print 'Saving picture:  ' + pictureUrl + '  ---->  ' + directoryName + '/' + pictureName
        urllib.urlretrieve(pictureUrl, directoryName + '/' + pictureName)

def getWorkData(html):
    directoryName = makeWorkDirectory(html)
    if (cmp(directoryName, ' ') == 0):
        print 'Skiping current Work'
        return
    else:
        getWorkPictures(html, directoryName)

def makeWorkDirectory(html):
    title = ''
    try:
        title = getTitle(html).strip()
    except UnicodeEncodeError:
        print 'Get title fail, using time depend name instead.'
        title = '%s' % time.time()

    directoryName = getLikeCount(html).strip() + '-' + title + ' ' + getDate(html)
    if os.path.exists(directoryName):
        print 'Directory:  ' + directoryName + ' exists, skiping...'
        return directoryName
    else:
        print 'Making directory:  ' + directoryName
        try:
            os.mkdir(directoryName)
            pass
        except OSError, WindowsError:
            print 'Making directory failed'
            return ' '
        return directoryName

def main():
    pagesCount = 0
    logFileName = 'log.txt'
    logFile = open(logFileName, 'a')
    socket.setdefaulttimeout(10)

    while True:
        pagesCount += 1
        try:
                html = getAllWorkPageHTML('http://bcy.net/coser/allwork?&p=%s' % pagesCount)
                currentPageWorksUrls = getCurrentPageWorks(html)

                for workUrl in currentPageWorksUrls:
                    workHtml = getWorkHTML(workUrl)
                    getWorkData(workHtml)
        except:
                pass

    logFile.close()

if __name__ == "__main__":
    sys.exit(int(main() or 0))
