import urllib2,re,hashlib
from bs4 import BeautifulSoup

## THIS FUNCTION HAS NOT BEEN TESTED, IT MAY DOESN'T WORK ##

def md5_check (file, blocks_size = 2**20):

    """
	the best way to check the entire file and make sure
	that you free the memory on each iteration,is dividing it 
	in various digest blocks, next feeding them
    to MD5 consecutively using update().

    """

    md5 = hashlib.md5()
    while True:

        #reading blocks size
    	data = file.read(blocks_size)

    	if not data:
    		break

        md5.update(data)

        return md5.digest()


## PARSING HTML FILE ##
request = urllib2.Request("http://download.cyanogenmod.com/?device=p970")
response = urllib2.urlopen(request)
soup = BeautifulSoup(response)
output = soup.find('a', href=re.compile('^http://get.cm/get'))['href']
##     -----         ##

## DOWNLOADING FILE ##

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
