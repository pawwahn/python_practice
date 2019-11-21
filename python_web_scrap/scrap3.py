import urllib.request as req
from bs4 import BeautifulSoup

web_link = "https://news.google.com/?hl=en-IN&gl=IN&ceid=IN:en"

page = req.urlopen(web_link)

soup = BeautifulSoup(page)

print(soup.prettify())
news_obj = soup.findAll('a',class_='DY5T1d')
A,B,C=[],[],[]
# for row in news_obj:
#     if 'Modi' in row.find(text=True) or 'modi' in row.find(text=True):
#         print("----")
#         print(row.find(text=True))
#         A.append(row)
#     if 'against PM Modi' in row.find(text=True) or 'against PM Modi' in row.find(text=True):
#         print("---->>>>>")
#         print(row.find(text=True))
#         B.append(row)
#     if 'Housing' in row.find(text=True) or 'Housing' in row.find(text=True):
#         print("----<<<<<")
#         print(row.find(text=True))
#         C.append(row)
#print(A)


