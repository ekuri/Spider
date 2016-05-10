class Pictures():
    tableName = 'pictures'
    def __init__(self, url, status):
        self.url = url
        self.status = status

    def createDBTable(self, database):
        database.execute('create table if not exists ' + tableName + ' (\
            url TEXT PRIMARY KEY NOT NULL,\
            status char(10) NOT NULL)')

    def insertIntoDB(self, database):
        database.execute('insert or ignore into ' + tableName + ' (url, status) values (\"' + self.url + '\", \"' + self.status + '\")')
        database.commit()

    def selectWithStatus(self, database, status):
        return database.execute('select * from ' + tableName + ' where status = \"' + status)

    def update(self, database):
        database.execute('update ' + tableName + ' set status = \"' + self.status + '\" where url = \"' + self.url + '\"')
        database.commit()
