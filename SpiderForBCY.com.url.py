import urllib2
import urllib
import socket
import re
import os
import time
import sys

def getLikeCount(html):
    likeReg = re.compile(r'<div class="btn btn--pink btn--zan btn--base-border-radius js-zan" data-zan="(\d+?)">')
    like = re.findall(likeReg, html)

    return like[0]

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

        while True:
            print 'Saving picture:  ' + pictureUrl + '  ---->  ' + directoryName + '/' + pictureName
            try:
                urllib.urlretrieve(pictureUrl, directoryName + '/' + pictureName)
                break
            except socket.timeout, error:
                print 'Get socket.timeout exception: ' + error

def getWorkData(url, html):
    directoryName = makeWorkDirectory(url, html)
    getWorkPictures(html, directoryName)

def makeWorkDirectory(url, html):
    directoryName = getLikeCount(html)
    urlReg = re.compile('/(.+?)/(.+?)/(.+?)/(.+)')
    urlTokens = (re.findall(urlReg, url))[0]
    for urlToken in urlTokens:
        directoryName = directoryName + '-' + urlToken

    if os.path.exists(directoryName):
        print 'Directory:  ' + directoryName + ' exists, skiping...'
        return directoryName
    else:
        print 'Making directory:  ' + directoryName
        try:
            os.mkdir(directoryName)
        except OSError, error:
            print 'Making directory failed'
            raise error
        return directoryName

def main():
    pagesCount = 0
    logFileName = 'SpiderForBCY.com.url.log'
    logFile = open(logFileName, 'a')
    logFileReader = open(logFileName, 'r')
    urlFileName = 'SpiderForBCY.com.Ranking.urls'
    urlFile = open(urlFileName, 'r')
    socket.setdefaulttimeout(10)

    allWorks = urlFile.readlines()
    urlFile.close()
    
    finishedWorks = set(logFileReader.readlines())
    print 'having finished urls count: %d' % len(finishedWorks)

    try:
        for work in allWorks:
            print 'Trying url: ' + work
            if work in finishedWorks:
                print 'This url has been finished'
                continue
            workHtml = getWorkHTML(work)
            getWorkData(work, workHtml)
            logFile.write(work)
    except KeyboardInterrupt:
        print 'KeyboardInterrupt, exiting...'

    logFile.close()

if __name__ == "__main__":
    sys.exit(int(main() or 0))
