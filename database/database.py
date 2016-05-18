import MySQLdb

class Database():
    user = 'root'
    passwd = 'qweasdzxc'
    db = 'spider'
    dbConnection = MySQLdb.connect(user=user, passwd=passwd, db=db, charset='utf8')

    @classmethod
    def execute(cls, query):
        cursor = cls.dbConnection.cursor()
        return cursor.execute(query)

    @classmethod
    def cursor(cls):
        return cls.dbConnection.cursor()

    @classmethod
    def commit(cls):
        return cls.dbConnection.commit()

    @classmethod
    def close(cls):
        cls.dbConnection.close()
