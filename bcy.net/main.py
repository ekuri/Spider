import sys
import database
import fromranking
import fromwork
import getpictures

if (len(sys.argv) != 2):
	print 'error: should give the database filename'
	quit()

db = database.Database(sys.argv[1])

#fromranking.run(db, "http://bcy.net/coser/", "toppost100?type=week&date=20150918")
#fromwork.run(db)
#getpictures.run(db, "./data/")
