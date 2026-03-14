from appium.webdriver.common.appiumby import AppiumBy

class MobileItemsPage:
    def __init__(self, driver):
        self.driver = driver # כאן זה driver ולא page
        
    @property
    def items_list(self):
        # ב-Appium אנחנו מחפשים אלמנטים דרך ה-driver
        return self.driver.find_elements(AppiumBy.ID, "text1")