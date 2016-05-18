import urllib2
import re
import time
import sys
sys.path.append('.')
from database.database import Database

# init database
cursor = Database.cursor()
cursor.execute('''create table if not exists collections (
        id integer primary key auto_increment,
        name text not null,
        charset char(10) not null,
        site text not null,
        url text not null,
        status char(10) not null,
        favor integer,
        create_date date,
        author_name text
    )'''
)

Database.commit()
cursor.close()

# init spider
base_url = 'http://meizitu.com/a/'
initial_url = 'list_1_1.html'
socket_timeout = 5
charset = 'gb2312'
site = 'meizitu.com'

def get_html(url_target, socket_timeout):
    data = urllib2.urlopen(url = url_target, timeout = socket_timeout)
    return data.read()

def get_collections(html):
    collections_reg = re.compile('<a target=\'_blank\' href="(.+?)".+?alt="(.+?)"></a>')
    collections = re.findall(collections_reg, html)
    return collections

def get_next_page(html):
    next_page_reg = re.compile("<li><a href='(.+?)'>\xcf\xc2\xd2\xbb\xd2\xb3</a></li>")
    next_page = re.findall(next_page_reg, html)
    if (len(next_page) > 0):
        print 'Next page: ' + next_page[0]
        return next_page[0]
    return ''

while len(initial_url) > 0:
    try:
        html = get_html(base_url + initial_url, socket_timeout)
        collections = get_collections(html)
        cursor = Database.cursor()
        for url, name in collections:
            cursor.execute(''' select * from collections where url = '%s'
                ''' % url
            )
            if cursor.fetchone():
                continue
            cursor.execute(''' insert into collections
                (name, charset, site, url, status)
                values (%s, %s, %s, %s, %s)
                ''', (name.encode('base64'), charset, site, url, 'new')
            )
        cursor.close()
        Database.commit()
        initial_url = get_next_page(html)
    except KeyboardInterrupt:
        break
    except BaseException, e:
        print e
        time.sleep(1)
        pass
