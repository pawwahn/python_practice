
import urllib
import urllib.request
import time
from bs4 import BeautifulSoup

wiki = "https://en.wikipedia.org/wiki/List_of_state_and_union_territory_capitals_in_India"

page = urllib.request.urlopen(wiki)

soup = BeautifulSoup(page)

print(soup.prettify())
print(soup.title)
print(soup.title.string)
print(soup.a)
all_links = soup.find_all('a')
for link in all_links:
    print(link.get("href"))