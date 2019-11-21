import requests
from bs4 import BeautifulSoup
import re

page = requests.get('https://www.jiosaavn.com/song/padi-padi-leche/Izg-bh9DXkY')
#print(page) # if response is 200, the result is true

soup = BeautifulSoup(page.text,'html.parser')

#print(soup) # gives all the content of the page with html tags

# get the content of class_ with the class name: content-cell num
artist_name_list = soup.find(class_='content-cell num')
print(artist_name_list)




