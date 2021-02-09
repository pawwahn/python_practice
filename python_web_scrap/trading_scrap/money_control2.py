import moneycontrolPy.mcp as mcp

api = mcp.API()
api.DRIVER_PATH = 'path_to_your_chromedriver_file/chromedriver'

url_user = "https://mmb.moneycontrol.com/arvind151-user-profile-617276696e64313531.html"
url_post = "https://mmb.moneycontrol.com/forum-topics/stocks/hero-motocorp/thread-message-81248383-83073237.html"
url_stock = 'https://mmb.moneycontrol.com/forum-topics/stocks/ab-money-246165.html'

"""
You could change the urls if you want to search 
for a specific user/post/stock from the moneycontol forum.
"""

user_info = api.get_user_info(url_user)                 #To extract the user information
post_info = api.get_post_info(url_post)                 #To extract the post information
stock_info = api.get_stock_info(url_stock)              #To extract the stock information
top_boarders = api.get_top_boarders()                   #To extract the top boarders
hot_stocks = api.get_stock_in_the_news()