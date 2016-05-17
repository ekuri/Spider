class Picture():
    tableName = 'pictures'
    def __init__(self, url, status, collection_id):
        self.id = None
        self.url = url
        self.status = status
        self.filename = None
        self.collection_id = collection_id

    @classmethod
    def createDBTableString(cls):
        return '''create table if not exists %s (
            id integer primary key auto_increment,
            url text not null,
            status char(10) not null,
            filename text,
            collection_id integer not null,
            foreign key (collection_id) references collections(id)
            )''' % cls.tableName

    def insertIntoDB(self, cursor):
        return cursor.execute('''insert into ''' + self.tableName +
            '''(url, status, filename, collection_id)
            values (%s, %s, %s, %s)''',
            (self.url, self.status, self.filename, self.collection_id))

    @classmethod
    def selectWithStatus(cls, cursor, status):
        return cursor.execute('''select * from ''' + cls.tableName +
        ''' where status = '%s'
            ''' % (status))

    def updateIntoDB(self):
        return '''update %s set status = %s, filename = %s where id = %s
            ''' % self.tableName, self.status, self.filename, self.id
