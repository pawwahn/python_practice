import urllib.request
import pandas as pd
from bs4 import BeautifulSoup

wiki = "https://en.wikipedia.org/wiki/List_of_state_and_union_territory_capitals_in_India"

page = urllib.request.urlopen(wiki)

soup = BeautifulSoup(page)

table_obj = soup.find('table', class_='wikitable sortable plainrowheaders')
#print(table_obj)
A=[]
B=[]
C=[]
D=[]
E=[]
for row in table_obj.findAll('tr'):
    #print(row)
    #print("--------------")
    cells = row.findAll('td')
    #print(cells)
    states = row.findAll('th')
    #print(states)
    if len(cells)==6:
        A.append(cells[0].find(text=True))
        B.append(states[0].find(text=True))
        C.append(cells[1].find(text=True))
        D.append(cells[2].find(text=True))
        E.append(cells[3].find(text=True))

df = pd.DataFrame(A,columns=['Number'])
df['State/UT'] = B
df['Administrative Capital'] = C
df['Legislative Capital'] = D
df['Judicial Capital'] = E
print(df)




