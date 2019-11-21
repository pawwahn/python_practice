html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""
from bs4 import BeautifulSoup
#page = '/home/likewise-open/HTCINDIA/pavankumark/Desktop/workspace/python_project/scrapy/html_page.html'
#soup = BeautifulSoup(page, 'html.parser')
soup = BeautifulSoup(html_doc, 'html.parser')
#print html_doc,"----------\n"

#print(soup.prettify())
#print soup.html
print (soup.title)
print (soup.html.title)
print (soup.html.title.name)
print (soup.html.title.string)
print (soup.title.parent.name)
print (soup.title.parent.parent.name)
#print soup.title.parent['class']
print (soup.p)
print (soup.p.b)
print (soup.p.b.name)
print (soup.p.b.string)
print (soup.p['class'])