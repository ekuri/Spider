import urllib2
import urllib
import socket
import re
import os
import sys
import traceback


targetDirectory = 'test/bcy/'

def getWorkHTML(url):
    baseUrl = 'http://bcy.net'
    req = urllib2.Request(baseUrl + url, headers={'User-Agent': ''})
    html = urllib2.urlopen(req).read()

    return html

def getWorkPictures(originUrl, html):
    postContentReg = re.compile(r'<div class="post__content js-content-img-wrap js-fullimg js-maincontent mb20">.*?<div class="declaration fz14 mt30">', re.S)
    postContents = re.findall(postContentReg, html)

    if (len(postContents) == 0):
        lockedContentReg = re.compile(r'<div class="center lh1d5 fz16 l-postLocked">(.+?)</div>', re.S)
        lockedContent = re.findall(lockedContentReg, html)
        if (len(lockedContent) == 0):
            lockInfoReg = re.compile(r'<span class="l-detail-no-right-to-see__text">(.+?)</span>', re.S)
            lockInfo = re.findall(lockInfoReg, html)
        else:
            lockInfoReg = re.compile(r'<p class="red">(.+?)</p>')
            lockInfo = re.findall(lockInfoReg, lockedContent[0])
        print 'This work can not be accessed, info: '
        for info in lockInfo:
            print info.decode('utf8')
            
        raise IndexError
    
    for postContent in postContents:
        pictureUrlsReg = re.compile(r"src='(.+?)/\w+?'")
        pictureUrls = re.findall(pictureUrlsReg, postContent)
        print 'Found %d pictures' % len(pictureUrls)
        return pictureUrls
    

def getWorkPicturesUrls(url, html):
    return getWorkPictures(url, html)

def main():
    global targetDirectory
    socket.setdefaulttimeout(10)

    logFileName = targetDirectory + 'SpiderForBCY.com.url.log'
    finishedWorks = set()
    try:
        logFileReader = open(logFileName, 'r')
        finishedWorks = set(logFileReader.readlines())
        logFileReader.close()
    except IOError, error:
        pass
    urlFileName = targetDirectory + 'SpiderForBCY.com.Ranking.urls'
    urlFileReader = open(urlFileName, 'r')

    allWorks = urlFileReader.readlines()
    urlFileReader.close()

    urlFileWriter = open(urlFileName, 'wb')
    unfinishedWorks = set()
    print 'Having finished urls count: %d' % len(finishedWorks)
    print 'Parsing unfinished url...'
    for work in allWorks:
        if work in finishedWorks:
            continue
        unfinishedWorks.add(work)

    for work in unfinishedWorks:
        urlFileWriter.write(work)
        
    urlFileWriter.close()
    print 'Rewriting %d urls back to %s' % (len(unfinishedWorks), urlFileName)
    
    logFileWriter = open(logFileName, 'a')
    outputFileName = targetDirectory + 'SpiderForBCY.com.get.imageurls.from.workurls.src'
    outputFile = open(outputFileName, 'a')
    errorFileName = targetDirectory + 'SpiderForBCY.com.get.imageurls.from.workurls.error'
    errorFile = open(errorFileName, 'wb')
    for work in unfinishedWorks:
        try:
            print 'Trying url: ' + work,

            workHtml = getWorkHTML(work)
            pictureUrls = getWorkPicturesUrls(work, workHtml)
            outputFile.write('Url:' + work)
            for url in pictureUrls:
                outputFile.write(url + '\n')
            logFileWriter.write(work)
        except KeyboardInterrupt:
            print 'KeyboardInterrupt, exiting...'
            break
        except:
            print 'Error in processing, traceback: '
            print traceback.format_exc()
            errorFile.write(work)
            continue
    logFileWriter.close()
    outputFile.close()
    errorFile.close()

if __name__ == "__main__":
    sys.exit(int(main() or 0))
