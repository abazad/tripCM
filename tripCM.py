import os, re, sys
import urllib2

#thanks to slacknux > https://github.com/slacknux for some suggestments
 
def main ():

    if (len (sys.argv) < 2):
 
                print "Usage : python tripCM.py URL mode \n"
                "URL : Cyanogenmod ROM URL \n"
                "mode : stable/RC/snapshot/nightly"

                sys.exit()
 
                URL = sys.argv[1]
                mode = sys.argv[2]
                link = "%s&type=%s" % (URL, mode)
                download(link)
 
 
def download (URL):

    response = urllib2.urlopen(URL)
    output = re.search('url=(.*?\.zip)', response.read()).group(1)

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