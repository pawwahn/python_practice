import requests
from bs4 import BeautifulSoup
from urllib import request

url = 'https://www.worldometers.info/world-population/population-by-country/'

req = requests.get(url=url)
soup = BeautifulSoup(req.content, 'lxml')

table = soup.find('tbody')

quotes = []
for row in table.findAll('tr'):
    #print(row.contents)
    quote = {}
    #quote['id'] = row.td.contents[0]
    quote['id'] = row.contents[1].text
    quote['country'] = row.contents[3].text
    quote['population'] = row.contents[5].text
    quote['yearly_change'] = row.contents[7].text
    quote['net_change'] = row.contents[9].text
    quotes.append(quote)
print(quotes)