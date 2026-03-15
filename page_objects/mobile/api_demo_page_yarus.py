from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.common.by import By




class MobileItemsPageYarus:
    def __init__(self, driver:WebDriver):
        self.driver = driver 
        
    categories = (By.XPATH,"//*[@id='text1']")
    animation_category = (By.XPATH, "//*[@text='Animation']")
    default_animetion = (By.XPATH,"//*[@text='Default Layout Animations']")
    LIST_VIEW = (By.CLASS_NAME, "android.widget.ListView")
      
        

    # def get_items_list(self):
    #     return self.driver.find_elements(items[0],items[1])