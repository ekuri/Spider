import urllib2
import socket
import re

def getCurrentDateTankingHTML(url):
    req = urllib2.Request(url, headers={ 'User-Agent': '' })
    html = urllib2.urlopen(req).read()
    return html

def getAllCurrentDateRankingWorkUrls(html):
    worksReg = re.compile('"(/coser/detail/.+?)"')
    works = re.findall(worksReg, html)
    return works

def getNextDateRankingUrl(html):
    nextDateUrlReg = re.compile('<a class="date" href="(.+?)"><span class="vam"')
    urls = re.findall(nextDateUrlReg, html)

    if (len(urls) == 0):
        return ''
    return urls[0]

def run(database, baseUrl, currentDateRankingUrl):
    socket.setdefaulttimeout(10)

    print 'Starting Spider for BCY...'
    while True:
        try:
                database.insert(currentDateRankingUrl, "date", "current")
                print 'Trying urls: ' + baseUrl + currentDateRankingUrl
                currentDateTankingHTML = getCurrentDateTankingHTML(baseUrl + currentDateRankingUrl)
                allCurrentDateRankingWorkUrls = getAllCurrentDateRankingWorkUrls(currentDateTankingHTML)
                print '---> Found %d works' % len(allCurrentDateRankingWorkUrls)
                for work in allCurrentDateRankingWorkUrls:
                    #print "found work: " + work
                    database.insert(work, "work", "new")
                database.updateStatus(currentDateRankingUrl, "done")
                
                currentDateRankingUrl = getNextDateRankingUrl(currentDateTankingHTML)
                if (cmp(currentDateRankingUrl, '') == 0):
                    break
        except KeyboardInterrupt:
            print 'keyboard Interrupt, exiting...'
            break
