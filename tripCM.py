import os, re, sys, getopt
import urllib2

# HTML parsing library
from bs4 import BeautifulSoup


def main ():

    if (len (sys.argv) < 2):

		print "Usage : python tripCM.py URL mode \n"
		"URL : Cyanogenmod ROM URL \n"
		"mode : stable/RC/snapshot/nightly"

	else:

		URL = sys.argv[1]
	  	mode = sys.argv[2]

	  	if mode == 'stable':
	  		link = URL+'&type=stable'
	  		download(link)

	  	elif mode == 'RC':
	  		link = URL+'&type=RC'
	  		download(link)

	  	elif mode == 'snapshot':
	  	    link = URL+'&type=snapshot'
	  	    download(link)

	  	elif mode == 'nightly':
	  		link = URL+'&type=nightly'
	  		download(link)



def download (URL):

	request = urllib2.Request(URL)
	response = urllib2.urlopen(request)
	soup = BeautifulSoup(response)
	output = soup.find('a', href=re.compile('^http://get.cm/get'))['href']

	file_name = output.split('/')[-1]
	u = urllib2.urlopen(output)
	f = open(file_name, 'wb')
	meta = u.info()
	file_size = int(meta.getheaders("Content-Length")[0])
	print "Downloading: %s Bytes: %s" % (file_name, file_size)

	file_size_dl = 0
	block_sz = 8192

	while True:

		buffer = u.read(block_sz)
		if not buffer:
			break

			file_size_dl += len(buffer)
			f.write(buffer)
			status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
			status = status + chr(8)*(len(status)+1)
			print status,
			f.close()

			if __name__ == '__main__':
				main()