import os
import sys

def main(argv):
    if not (len(argv) == 2):
        print 'Usage:  ' + argv[0] + '  [filename]'
        return
        
    if not os.path.isfile(argv[1]):
        print 'Not a file'
        return
        
    print 'Converting to local...'
    targetFileReader = open(argv[1], 'r')
    fileLines = targetFileReader.readlines()
    targetFileReader.close()

    targetFileWriter = open(argv[1], 'wb')
    for line in fileLines:
        print 'Writing: ' + line.strip()
        targetFileWriter.write(line.strip() + '\n')

if __name__ == '__main__':
    main(sys.argv)