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
    

    @allure.step("Get current device orientation status")
    def get_device_orientation(self) -> str:
        """
        Business flow to retrieve the device orientation.
        """
        return MobileActions.get_orientation(self.driver)
    
    @allure.step("Verify device is responsive")
    def check_device_responsiveness(self):
        """
        Flow to ensure the device is alive and communicating with the driver.
        Returns system time and display resolution.
        """
        return MobileActions.get_device_metadata(self.driver)
    

    @allure.step("Get battery percentage")
    def get_battery_status(self) -> int:
        """
        Retrieves the battery level using the Action layer.
        """
        return MobileActions.get_battery_level(self.driver)

    @allure.step("Get Wi-Fi connection status")
    def get_wifi_status(self) -> bool:
        """
        Retrieves the Wi-Fi status using the Action layer.
        """
        return MobileActions.is_wifi_on(self.driver)