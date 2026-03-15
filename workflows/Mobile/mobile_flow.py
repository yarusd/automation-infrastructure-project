import allure
from extensions.mobile_actions import MobileActions
from page_objects.mobile.api_demo_page import MobileItemsPage
from appium.webdriver.webdriver import WebDriver

class MobileFlows:
    def __init__(self, driver:WebDriver): 
        self.driver = driver 
        self.items_page = MobileItemsPage(driver)


    @allure.step("Get the total count of items on screen")
    def get_items_count(self) -> int:
        return len(self.items_page.get_items_list())
    

    @allure.step("Get ListView count from page source")
    def get_list_view_count_from_source(self) -> int:
        return MobileActions.get_text_count_in_source(self.driver, "ListView")