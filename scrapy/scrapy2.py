html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">second para </p>
"""

from bs4 import BeautifulSoup

soup = BeautifulSoup(html_doc,'html.parser')
#print soup
#print soup.html

#print soup.p['class']
#print soup.body.p['class']
#print soup.body.p.child
#print soup.a
#print soup.a['2']
x =  soup.find_all('a') 
#print soup.find(id='title')                            # gives error as der is no id='title'

#print soup.find_all('a')
"""
for line in soup.find_all('a'):
    print line,"---> ",line.get('href')
    #print "---> ",line.get('class')
"""
print (soup.get_text("\n", " "))                             # soup.get_text(separator, strip, types)
print ("++++++++++++++++++++++++++++++++++")
print (soup.get_text(";", '\n'))
print ("-------------------------------")
print (soup.get_text())


