#!/usr/bin/python

#tripCM by gabriele-salvatori & slacknux

import getopt
import re
import sys
import time
import urllib2


def download(codename, tp):
	link = "http://download.cyanogenmod.com/?device=%s&type=%s" % (codename, tp)
	response = urllib2.urlopen(link)
	response = response.read()
	
    	try:
		directLink = re.search('url=(.*?\.zip)', response).group(1)
	except:
		print "1. Wrong codename and/or type\n2. Type not available for your device\n"
		sys.exit()

	fileName = directLink.split("/")[-1]
    	u = urllib2.urlopen(directLink)
    	meta = u.info()
    	fileSize = int(meta.getheaders("Content-Length")[0])
	f = open(fileName, 'wb')
    	print "[*]Downloading: %s" % fileName

    	downloadSize = 0
    	timeSpent = 0
    	speed = 0
    	step = time.time()

    	while True:
      		start = time.time()
      		chunk = u.read(8192)

      		if not chunk:
			time.sleep(1)
			print "\033[0K\t\tDownload completed\n"
			break

      		now = time.time()

      		if now-step>=2:
			timeSpent = now - start
		        speed=((len(chunk) / 1024) / timeSpent)
		        step = now

		downloadSize += len(chunk)
		f.write(chunk)
		remaining = (((fileSize-downloadSize)/len(chunk))*timeSpent)
      
		if remaining >= 60 and remaining<3600:
			remaining="%d min" % (remaining/60)
		elif remaining<60:
	  		remaining="%d s" % remaining
      		else:
          		remaining="%d h" % (remaining/3600)

      		percent = int(downloadSize*100/fileSize)
      		status = "\033[0J " + "\t\t%.2f MB of %.2f MB\t%d%%\t%d kB/s   %s" % (downloadSize/1048576.0, fileSize/1048576.0, percent, speed, remaining)
      		status += "\033[1A"
      		print status
	f.close()


def devList():
	u = urllib2.urlopen("http://download.cyanogenmod.com/")
	response = u.read()

	#extract device name and codename
	devicesList = re.findall('title="(.*?)".*?GetCM.navigateDevice\(\'(.*?)\'\)', response)
	#sort by device name
	devicesList.sort(key=lambda tup:tup[0])

	print "\033[4mCodename\033[0m"
	for item in devicesList:
		ntab = "\t"
		if len(item[1]) < 8:
			ntab="\t\t"
		print "%s%s%s" % (item[1], ntab, item[0])


def usage():
	print "Usage:\n\t./tripCM.py -c <codename> -t <type>\n"
	print "Description:\n\t-c, --codename\t\tdevice codename\n\t-t, --type\t\tstable, RC, snapshot, nightly\n\t-l, --list\t\tdevices list (to know your device codename)\n\t-h, --help\t\twhat you're reading now\n"
	print "Example:\n\t./tripCM.py -c crespo -t stable\n"


def main():
	print "                                   *     "
	print "          )                 (    (  `    "
	print "       ( /( (   (           )\   )\))(   "
	print "       )\()))(  )\  `  )  (((_) ((_)()\  "
	print "      (_))/(()\((_) /(/(  )\___ (_()((_) "
	print "      | |_  ((_)(_)((_)_\((/ __||  \/  | "
	print "      |  _|| '_|| || '_ \)| (__ | |\/| | "
	print "       \__||_|  |_|| .__/  \___||_|  |_| "
	print "                   |_|                   "
	print "       by gabriele-salvatori & slacknux\n"

	try:
		opts, args = getopt.getopt(sys.argv[1:], "c:t:lh", ["codename", "type", "list", "help"])
	except getopt.GetoptError as err:
		usage()
		print str(err)
		sys.exit()
	
	if not opts:
		usage()
		sys.exit()
	
	codename = ""
	tp = ""

	for o, a in opts:
		if o in ("-h", "--help"):
			usage()
			sys.exit()
		elif o in ("-l", "--list"):
			devList()
			sys.exit()
		elif o in ("-c", "--codename"):
			codename = a
		elif o in ("-t", "--type"):
			tp = a
		else:
			usage()
			sys.exit()
	download(codename, tp)


if __name__ == "__main__":
	main()

