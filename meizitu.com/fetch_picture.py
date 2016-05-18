import urllib2
import re
import time
import sys
import os
import hashlib
sys.path.append('.')
from database.database import Database

if (len(sys.argv) != 2):
    print 'should get base path'
    quit()
base_path = sys.argv[1]

cursor = Database.cursor()
cursor.execute('select id, url from pictures where status = "%s"' % 'new')
row = cursor.fetchone()
socket_timeout = 5
while (row):
    try:
        print row[1]
        picture_data = urllib2.urlopen(url = row[1], timeout = socket_timeout).read()
        sha1sum = hashlib.sha1(picture_data).hexdigest()
        filename = sha1sum + '.' + row[1].split('.')[-1]
        print filename
        picture_file = open(base_path + '/' + filename, 'wb')
        picture_file.write(picture_data)
        update_cursor = Database.cursor()
        update_cursor.execute('update pictures set status = "%s", filename = "%s" where id = %d' % ('done', filename, row[0]))
        Database.commit()
        update_cursor.close()

        row = cursor.fetchone()
    except KeyboardInterrupt:
        break
    except BaseException, e:
        print e
        time.sleep(1)
        pass

cursor.close()
