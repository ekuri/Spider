import urllib2
import re
import time
import sys
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
    pictures_reg = re.compile('''<img alt=".+?" src="(.+?)" /><br />''')
    pictures = re.findall(pictures_reg, html)
    return pictures

cursor.execute('select * from collections where status = "%s" and site = "%s"' % ('new', 'meizitu.com'))
row = cursor.fetchone()

socket_timeout = 5
while (row):
    try:
        print row[4]
        html = get_html(row[4], socket_timeout)
        pictures = get_pictures(html)
        insert_cursor = Database.cursor()
        for pic in pictures:
            if (insert_cursor.execute('select * from pictures where url = "%s"' % pic) > 0):
                continue
            insert_cursor.execute(''' insert into pictures
                (url, status, collection_id)
                values (%s, %s, %s)
                ''', (pic, 'new', row[0])
            )
        Database.commit()
        insert_cursor.execute('update collections set status = "%s" where id = %d' % ('done', row[0]))
        Database.commit()
        row = cursor.fetchone()
    except KeyboardInterrupt:
        break
    except BaseException, e:
        print e
        time.sleep(1)
        pass

cursor.close()
