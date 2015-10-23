import urllib2
import urllib
import socket
import re
import os
import time
import sys

def getCurrentDateTankingHTML(url):
    req = urllib2.Request(url, headers={ 'User-Agent': '' })
    html = urllib2.urlopen(req).read()
    return html

def getAllCurrentDateRankingWorkUrls(html):
    worksReg = re.compile('<div class="work-thumbnail__ft center mt15 mb10">.+?<a href="(.+?)"', re.S)
    works = re.findall(worksReg, html)
    return works

def getNextDateRankingUrl(html):
    nextDateUrlReg = re.compile('<a class="date" href="(.+?)"><span class="vam"')
    urls = re.findall(nextDateUrlReg, html)

    if (len(urls) == 0):
        return ''
    return urls[0]

def main():
    baseUrl = 'http://bcy.net/coser/'
    currentDateRankingUrl = 'toppost100?type=lastday&date=20150918'
    logFileName = 'SpiderForBCY.com.Ranking.log'
    logFile = open(logFileName, 'a')
    urlsFileName = 'SpiderForBCY.com.Ranking.urls'
    urlsFile = open(urlsFileName, 'wb')
    allWorks = set()
    socket.setdefaulttimeout(10)

    print 'Starting Spider...'
    while True:
        try:
                debugString = 'Trying urls: ' + currentDateRankingUrl
                currentDateTankingHTML = getCurrentDateTankingHTML(baseUrl + currentDateRankingUrl)

                allCurrentDateRankingWorkUrls = getAllCurrentDateRankingWorkUrls(currentDateTankingHTML)
                
                print debugString + (' ---> Found %d works' % len(allCurrentDateRankingWorkUrls))
                logFile.write(debugString + '\n')
                
                allWorks |= set(allCurrentDateRankingWorkUrls)
                
                currentDateRankingUrl = getNextDateRankingUrl(currentDateTankingHTML)
                if (cmp(currentDateRankingUrl, '') == 0):
                    break
        except KeyboardInterrupt:
            print 'keyboard Interrupt, exiting...'
            break
        #except:
        #        pass

    print 'Found totally %d works' % len(allWorks)
    for workUrl in allWorks:
        urlsFile.write(workUrl + '\n')
    
    urlsFile.close()
    logFile.close()

if __name__ == "__main__":
    sys.exit(int(main() or 0))
