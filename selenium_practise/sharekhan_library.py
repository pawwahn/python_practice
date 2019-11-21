import time
from selenium import webdriver

driver = webdriver.Chrome(executable_path="C:/chrome_file/chromedriver_win32/chromedriver")

class ShareKhanApp:

    def login_page(self):
        print("Trying to Login")
        driver.get("https://www.sharekhan.com/")

    @property
    def click_login(self):
        return driver.find_element_by_xpath(".//li[@class='login']/a[contains(text(),'Login/Trade')]")

    @property
    def trade_login(self):
        time.sleep(2)
        return driver.find_element_by_xpath("/*//form/md-input/span/input")

    @property
    def click_next_button_to_login(self):
        return driver.find_element_by_xpath("//*/loginpage//form/div[1]/button")

    @property
    def enter_mem_pwd(self):
        return driver.find_element_by_xpath("/*//form/md-input/span/input")

    @property
    def login_button_after_pwd(self):
        return driver.find_element_by_xpath("/*//loginpage//div[1]/button")

    @property
    def click_trade_now(self):
        return driver.find_element_by_xpath("*//span[contains(text(),'TRADE NOW')]")

    @property
    def search_share(self):
        return driver.find_element_by_xpath("//div/div[2]/md-input/span/input")

    @property
    def selected_share(self):
        return driver.find_element_by_xpath(".//*/li[1]//a/div/span[1]")

    @property
    def select_bracket_plus_tsl(self):
        return driver.find_element_by_xpath("//*/form//span[2]/md-radio/div")