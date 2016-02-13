import sqlite3

class Database():
	db = None
	
	def __init__(self, filename):
		self.db = sqlite3.connect(filename)
		self.db.execute('create table if not exists url (target TEXT PRIMARY KEY NOT NULL, tag TEXT NOT NULL, status TEXT NOT NULL)')
		self.db.commit()
	
	def __del__(self):
		self.db.close()
	
	def insert(self, url, tag, status):
		self.db.execute("insert or ignore into url (target, tag, status) values ('" + url + "', '" + tag + "', '" + status + "')")
		self.db.commit()
		
	def selectWithTag(self, tag):
		return self.db.execute("select * from url where tag = '" + tag + "'")
		
	def selectWithUrl(self, url):
		return self.db.execute("select * from url where target = '" + url + "'")
		
	def selectWithTagAndStatus(self, tag, status):
		return self.db.execute("select * from url where tag = '" + tag + "' and status = '" + status + "'")
		
	def updateStatus(self, url, status):
		self.db.execute("update url set status = '" + status + "' where target = '" + url + "'")
		self.db.commit()
		