import re
from urllib2 import urlopen
from urllib2 import Request,request_host
#from urllib.request import urlopen, Request
import urllib2
import urllib3.request
url = "http://www.chennai.tn.nic.in/emergency.htm"

#response = urllib2.request_host.urlopen(url)

response = urllib2.request_host.urlopen(url)

html = response.read()

htmlStr = html.decode()

pdata = findall("\d{2,20}", htmlStr)

for i in pdata:
    print i