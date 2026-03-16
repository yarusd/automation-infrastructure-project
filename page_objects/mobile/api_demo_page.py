from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from extensions.mobile_actions import MobileActions

class MobileItemsPage:
    def __init__(self, driver: WebDriver): 
        self.driver = driver 

    ITEMS = (By.XPATH, "//*[@id='text1']")
    CATEGORIES = (By.XPATH, "//*[@id='text1']")
    ANIMATION_CAT = (By.XPATH, "//*[@text='Animation']")
    DEFAULT_ANIM = (By.XPATH, "//*[@text='Default Layout Animations']")
    LIST_VIEW = (By.CLASS_NAME, "android.widget.ListView")

    def get_items_list(self,items):
        items_locator = (items)
        WebDriverWait(self.driver, 10).until(
        EC.visibility_of_any_elements_located(items_locator)
        )
        return self.driver.find_elements(*items_locator)

    def click_category_by_text(self, name):
        dynamic_xpath = (By.XPATH, f"//*[@text='{name}']")
        self.driver.find_element(*dynamic_xpath).click()
        
    def get_categories_count(self) -> int:
        return MobileActions.get_elements_count_amount(self.driver, self.CATEGORIES)
    
    def navigate_to_default_animation(self):
        MobileActions.wait_and_click(self.driver, self.ANIMATION_CAT)
        MobileActions.wait_and_click(self.driver, self.DEFAULT_ANIM)