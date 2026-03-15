from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.webdriver import WebDriver


items = (MobileBy.ID,"text1")


class MobileItemsPage:
    def __init__(self, driver:WebDriver):
        self.driver = driver 
        
    def get_items_list(self):
        return self.driver.find_elements(items[0],items[1])