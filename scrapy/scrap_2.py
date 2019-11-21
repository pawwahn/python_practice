import requests
from bs4 import BeautifulSoup

page = requests.get('https://www.jiosaavn.com/song/padi-padi-leche/Izg-bh9DXkY')

soup = BeautifulSoup(page.text,'html.parser')
#print(soup)

# get all <p> tag data
a_tag_data = soup.find_all('p')
print(a_tag_data)

# remove duplicate data from all the <p>
print("-------------->")
print(set(a_tag_data))