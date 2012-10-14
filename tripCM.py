import urllib2
from bs4 import BeautifulSoup
import re

## PARSING HTML FILE ##
request = urllib2.Request("replace with your cellphone URL")
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
