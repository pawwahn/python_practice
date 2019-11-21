import time
#from selenium_practise.sharekhan_library import *
#from selenium_practise.sharekhan_library import ShareKhanApp as App

#pytohn_practise

from pytohn_practise.selenium_practise.sharekhan_library import *
from .sharekhan_library import ShareKhanApp as App

SHARE_NAME = 'ITC'
#####################################################
#NORMAL = None
#BRACKET = None
#BRACKET_TSL = App().select_bracket_plus_tsl
####################################################
TRADE_TYPE = 'BRACKET+TSL'

class Trade:



    def main_function(self):
        self.call_login_page()
        self.click_login_button()
        self.input_trade_login()
        self.click_next_button()
        self.input_membership_password()
        self.login_after_password()
        self.trade_now()
        self.find_share_to_trade()
        self.select_bracket_plus_tsl()

    def call_login_page(self):
        App().login_page()

    def click_login_button(self):
        App().click_login.click()

    def input_trade_login(self):
        time.sleep(2)
        App().trade_login.click()
        App().trade_login.send_keys("NANDAGOPAL1992")

    def click_next_button(self):
        App().click_next_button_to_login.click()

    def input_membership_password(self):
        time.sleep(2)
        App().enter_mem_pwd.click()
        App().enter_mem_pwd.send_keys("Python*05")

    def login_after_password(self):
        time.sleep(2)
        App().login_button_after_pwd.click()

    def trade_now(self):
        time.sleep(2)
        App().click_trade_now.click()

    def find_share_to_trade(self):
        time.sleep(2)
        App().search_share.click()
        App().search_share.send_keys(SHARE_NAME)
        time.sleep(3)
        App().selected_share.click()

    def select_bracket_plus_tsl(self):
        time.sleep(2)
        App().select_bracket_plus_tsl.click()

if __name__=='__main__':
    Trade().main_function()
