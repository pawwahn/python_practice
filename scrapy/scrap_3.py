import requests
from bs4 import BeautifulSoup

page = requests.get('https://www.jiosaavn.com/song/padi-padi-leche/Izg-bh9DXkY')

soup = BeautifulSoup(page.text,'html.parser')
#print(soup)

artist_name = soup.find(class_='menu-items')
#print(artist_name)
artist_name_list_items = artist_name.find_all('h2')

#get the content from the tags
for artist_name in artist_name_list_items:
    print(artist_name.contents[0])