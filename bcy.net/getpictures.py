import urllib2
import urllib
import socket
import re
import traceback

targetDirectory = 'get/bcy/'

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

        pictureNameReg = re.compile(r'/(\w+\.?\w+)$')
        pictureName = re.findall(pictureNameReg, pictureUrl)[0]

        while True:
            print 'Saving picture:  ' + pictureUrl + '  ---->  ' + directoryName + '/' + pictureName
            try:
                urllib.urlretrieve(pictureUrl, directoryName + '/' + pictureName)
                break
            except socket.timeout, error:
                print 'Get socket.timeout exception: ',
                print error


def run(database, targetDirectory):
    socket.setdefaulttimeout(10)
    cursor = database.selectWithTagAndStatus("picture", "new")
    
    for row in cursor:
        url = row[0]
        filename = "-"
        tokens = url.split('/')
        filename = filename.join(tokens[4:])
        print "Getting: " + url + " To: " + targetDirectory + filename
        try:
            urllib.urlretrieve(url, targetDirectory + filename)
            database.updateStatus(url, "done")
        except KeyboardInterrupt:
            print 'KeyboardInterrupt, exiting...'
            break
        except:
            traceback.print_exc()
            pass