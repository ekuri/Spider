import urllib2
import re
import time
import sys
import traceback
sys.path.append('.')
from database.database import Database

# init database
cursor = Database.cursor()
cursor.execute('''create table if not exists pictures (
        id integer primary key auto_increment,
        url text not null,
        status char(10) not null,
        collection_id integer not null,
        filename text,
        foreign key (collection_id) references collections(id)
    )'''
)

Database.commit()

def get_html(url_target, socket_timeout):
    data = urllib2.urlopen(url = url_target, timeout = socket_timeout)
    return data.read()

def get_pictures(html):
    pictures_content_reg = re.compile('<div class="postContent">.+?</div>', re.S)
    picture_content = re.findall(pictures_content_reg, html)
    if (len(picture_content) != 1):
        raise Exception('No post content found')
    pictures_reg = re.compile('src="(.+?)"')
    pictures = re.findall(pictures_reg, picture_content[0])
    return pictures

cursor.execute('select * from collections where status = "%s" and site = "%s"' % ('new', 'meizitu.com'))
row = cursor.fetchone()

socket_timeout = 5
while (row):
    try:
        insert_cursor = Database.cursor()
        insert_cursor.execute('update collections set status = "%s" where id = %d' % ('waiting', row[0]))
        Database.commit()
        print row[4]
        html = get_html(row[4], socket_timeout)
        pictures = get_pictures(html)
        for pic in pictures:
            if (insert_cursor.execute('select * from pictures where url = "%s"' % pic) > 0):
                print '    Url already exists: ' + pic
                continue
            print pic
            insert_cursor.execute(''' insert into pictures
                (url, status, collection_id)
                values (%s, %s, %s)
                ''', (pic, 'new', row[0])
            )
        Database.commit()
        insert_cursor.execute('update collections set status = "%s" where id = %d' % ('done', row[0]))
        Database.commit()
        insert_cursor.close()
        cursor.execute('select * from collections where status = "%s" and site = "%s"' % ('new', 'meizitu.com'))
        row = cursor.fetchone()
    except KeyboardInterrupt:
        break
    except BaseException, e:
        traceback.print_exc()
        time.sleep(1)
        pass

cursor.close()
