import urllib
import socket
import re
import os
import time

def getHTML(url):
    page = urllib.urlopen(url)
    html = page.read()

    error404Reg = re.compile(r'(.*?wrong404.*?)')
    error404 = re.findall(error404Reg, html)

    if (len(error404) > 0):
        print "URL not exist: " + url
        raise ValueError

    return html

def getPicturesGroupName(html):
    reg = r'<div class="metaRight">.+?<h2><a href=".*?">(.+?)</a></h2>'
    picturesGroupNameReg = re.compile(reg, re.S)
    picturesGroupName = re.findall(picturesGroupNameReg, html)

    print 'Found Pictures Group:  ' + picturesGroupName[0]

    return picturesGroupName[0]

def makePictureFolder(pictureGroupName):
    pictureGroupName = pictureGroupName.strip()

    if os.path.exists(pictureGroupName):
        print 'Directory:  ' + pictureGroupName + ' exists, skiping...'
    else:
        print 'Making directory:  ' + pictureGroupName
        os.mkdir(pictureGroupName)

def getAllPicturesUrl(html):
    picturesContentReg = re.compile(r'<div class="postContent">.+?</div>', re.S)
    pictureContent = re.findall(picturesContentReg, html)[0]

    allPicturesUrlReg = re.compile(r'src="(.+?)"', re.S)
    allPicturesUrl = re.findall(allPicturesUrlReg, pictureContent)

    for pictureUrl in allPicturesUrl:
        print 'Found picture Url:  ' + pictureUrl

    return allPicturesUrl

def getAllPictures(allPicturesUrl, pictureGroupName):
    count = 0;
    for pictureUrl in allPicturesUrl:
        suffixReg = re.compile(r'(\.\w*)$')
        suffix = re.findall(suffixReg, pictureUrl)[0]

        print 'Saving picture:  ' + pictureUrl + '  ---->  %s' % count + suffix
        urllib.urlretrieve(pictureUrl, pictureGroupName + '/' + '%s' % count + suffix)
        count += 1

def singleRun(htmlUrl):
    html = getHTML(htmlUrl)
    pictureGroupName = getPicturesGroupName(html)

    makePictureFolder(pictureGroupName)
    allPicturesUrl = getAllPicturesUrl(html)
        
    getAllPictures(allPicturesUrl, pictureGroupName)


socket.setdefaulttimeout(10)
pageCount = 5159
logFileName = 'log.txt'
logFile = open(logFileName, 'a')

while True:
    try:
        pageCount += 1
        while True:
            htmlUrl = 'http://www.meizitu.com/a/%s.html' % pageCount
            print 'Trying URL:  ' + htmlUrl
            logFile.writelines('Trying URL:  ' + htmlUrl + '\n')
        
            singleRun(htmlUrl)
        
            pageCount += 1
            print 'Finished URL:  ' + htmlUrl
            logFile.write('Finished URL:  ' + htmlUrl + '\n')
    except KeyboardInterrupt:
        print 'keyboard Interrupt, exiting...'
        break
    except ValueError:
        logFile.write('Not Found URL:  ' + htmlUrl + '\n')
        time.sleep(0.5)
        continue
    except:
        pageCount -= 1
        time.sleep(0.5)
        continue

logFile.close()
