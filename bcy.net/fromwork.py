import urllib2
import socket
import re

def getWorkHTML(url):
    baseUrl = 'http://bcy.net'
    req = urllib2.Request(baseUrl + url, headers={'User-Agent': ''})
    html = urllib2.urlopen(req).read()

    return html

def getWorkPicturesUrls(html):
    pictureUrlsReg = re.compile(r"src='(.+?)/\w650'")
    pictureUrls = re.findall(pictureUrlsReg, html)
    print 'Found %d pictures' % len(pictureUrls)
    return pictureUrls

def run(database):
    socket.setdefaulttimeout(10)
    cursor = database.selectWithTagAndStatus("work", "new")
    for row in cursor:
        try:
            work = row[0]
            print 'Trying url: ' + work,

            workHtml = getWorkHTML(work)
            pictureUrls = getWorkPicturesUrls(workHtml)
            for url in pictureUrls:
                database.insert(url, "picture", "new")
            
            database.updateStatus(work, "done")
        except KeyboardInterrupt:
            print 'KeyboardInterrupt, exiting...'
            break
