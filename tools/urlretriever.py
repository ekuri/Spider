import os
import urllib
import sys

def main(argv):
	if not (len(argv) == 3):
		print 'Usage:  ' + argv[0] + '  [src file]  [target directory]'
		return
	
	if not os.path.isfile(argv[1]):
		print 'Not a file, exiting...'
		return
	
	targetDirectory = argv[2]
	if not os.path.isdir(targetDirectory):
		print 'Making directory: ' + targetDirectory
		try:
			os.mkdir(targetDirectory)
		except:
			print 'Error in making directory, exiting...'
			return
	
	print 'Starting url retrieve...'
	srcfile = open(argv[1], 'r')
	
	allElements = srcfile.readlines()
	srcfile.close()
	
	logfile = open()
	for 

if __name__ == '__main__':
	main(sys.argv)