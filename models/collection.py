class Collection():
    tableName = 'collections'
    def __init__(self, name, site, url, status):
        self.id = None
        self.name = name
        self.favor = None
        self.create_date = None
        self.author_name = None
        self.site = site
        self.url = url
        self.status = status

    @classmethod
    def createDBTableString(cls):
        return '''create table if not exists %s (
                id integer primary key auto_increment,
                name text,
                favor integer,
                create_date date,
                author_name text,
                site text not null,
                url text not null,
                status char(10) not null
            )''' % cls.tableName

    def insertIntoDB(self, cursor):
        return cursor.execute('''insert into ''' + self.tableName + '''
                (name, favor, create_date, author_name, site, url, status)
                values (%s, %s, %s, %s, %s, %s, %s)''',
                (self.name, self.favor, self.create_date, self.author_name, self.site, self.url, self.status))
