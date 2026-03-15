from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.webdriver import WebDriver

class MobileItemsPage:
    def __init__(self, driver: WebDriver): 
        self.driver = driver 

    def get_items_list(self):
        # Using XPATH for better compatibility with Appium Studio
        items_locator = (MobileBy.XPATH, "//*[@id='text1']")
        return self.driver.find_elements(*items_locator)