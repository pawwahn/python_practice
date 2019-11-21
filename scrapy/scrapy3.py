import requests
from bs4 import BeautifulSoup

url = "https://eportal.htcindia.com/home/"
r = requests.get(url)

soup =BeautifulSoup(r.content)
links = soup.find_all("a")

#for link in links:
    #print link.get("href")
#     if 'http' in link.get("href"):
#         print "<a href='%s'>%s</a>" %(link.get("href"),link.text)

# g_data = soup.find_all("div",{"class": "clearfix"})
# print g_data

j = soup.html.body.section
print (j)
    