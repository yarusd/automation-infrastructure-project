import allure
from page_objects.mobile.api_demo_page import MobileItemsPage

class MobileFlows:
    def __init__(self, driver): # מקבל driver ולא page
        self.items_page = MobileItemsPage(driver)

    @allure.step("Get the total count of items on screen")
    def get_items_count(self) -> int:
        # בגלל שזה Appium, אנחנו סופרים את אורך הרשימה שחזרה
        return len(self.items_page.items_list)