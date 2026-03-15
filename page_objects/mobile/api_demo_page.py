from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.common.by import By
from extensions.mobile_actions import MobileActions

class MobileItemsPage:
    def __init__(self, driver: WebDriver): 
        self.driver = driver 

    CATEGORIES = (By.XPATH, "//*[@id='text1']")
    ANIMATION_CAT = (By.XPATH, "//*[@text='Animation']")
    DEFAULT_ANIM = (By.XPATH, "//*[@text='Default Layout Animations']")
    LIST_VIEW = (By.CLASS_NAME, "android.widget.ListView")

    def get_items_list(self):
        items_locator = (MobileBy.XPATH, "//*[@id='text1']")
        return self.driver.find_elements(*items_locator)
    
    def get_categories_count(self) -> int:
        return MobileActions.get_elements_count_amount(self.driver, self.CATEGORIES)
    
    def navigate_to_default_animation(self):
        MobileActions.wait_and_click(self.driver, self.ANIMATION_CAT)
        MobileActions.wait_and_click(self.driver, self.DEFAULT_ANIM)