
import urllib
import urllib.request
import time
from bs4 import BeautifulSoup
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

wiki = "https://www.moneycontrol.com/stocks/advice/display_more.php"

page = urllib.request.urlopen(wiki)

soup = BeautifulSoup(page, features="lxml")

print(soup.prettify())
print(soup.title)
# print(soup.title.string)
news_obj = soup.findAll('div',class_='listingn')
print(news_obj)
