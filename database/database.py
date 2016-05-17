import MySQLdb

class Database():
    user = 'root'
    passwd = 'qweasdzxc'
    db = 'spider'
    dbConnection = MySQLdb.connect(user=user, passwd=passwd, db=db)

    @classmethod
    def execute(cls, query):
        cursor = cls.dbConnection.cursor()
        return cursor.execute(query)

    @classmethod
    def cursor(cls):
        return cls.dbConnection.cursor()
