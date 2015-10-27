import os
import urllib
import sys

def main(argv):
	if not (len(argv) == 3):
		print 'Usage:  ' + argv[0] + '  [url file]  [target directory]'
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

if __name__ == '__main__':
	main(sys.argv)