import urllib
import urllib.request
import time
from bs4 import BeautifulSoup
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

stock_advice_page = "https://www.moneycontrol.com/markets/stock-advice/"

page = urllib.request.urlopen(stock_advice_page)

soup = BeautifulSoup(page, features="lxml")

# print(soup.prettify())
# print(soup.title)

expert_data_obj = soup.select('equity1')
# print(soup.select('div.equity1'))

for link in expert_data_obj.find_all("table"):
    print(link)










# print(expert_data_obj.find('table'))
#      # print(row)
#
# # tables = soup.findChildren('table')
# # print(tables)
# #
# # for table in tables[1:]:
# # #     print("------------------------->>>")
# # #     # print(table)
# # #     # print(table.findChildren(['th'])).find('div')
# # #     print(table.select('td')[1].get_text(strip=True))
# #     print()
#
#
