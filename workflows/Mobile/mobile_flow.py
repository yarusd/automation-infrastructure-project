import allure
from extensions.mobile_actions import MobileActions
from page_objects.mobile.default_animation_page import DefaultAnimationPage
from page_objects.mobile.api_demo_page import MobileItemsPage
from appium.webdriver.webdriver import WebDriver

class MobileFlows:
    def __init__(self, driver:WebDriver): 
        self.driver = driver 
        self.items_page = MobileItemsPage(driver)
        self.default_animation = DefaultAnimationPage(driver)


    @allure.step("Get the total count of items on screen")
    def get_items_count(self) -> int:
        return len(self.items_page.get_items_list())
    

    @allure.step("Get ListView count from page source")
    def get_list_view_count_from_source(self) -> int:
        return MobileActions.get_page_source(self.driver, "ListView")
    

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
    

    @allure.step("Step: Navigate and count items")
    def get_items_count(self) -> int:
        return self.items_page.get_categories_count()
    
    @allure.step("Get current buttons count")
    def get_current_buttons_count(self) -> int:
        return self.default_animation.get_buttons_count()

    @allure.step("Step: Go to Animations")
    def go_to_default_animation_page(self) -> None:
        self.items_page.navigate_to_default_animation()

    @allure.step("Step: Add button and return total count")
    def add_button_and_get_count(self) -> int:
        self.default_animation.add_new_button()
        return self.default_animation.get_buttons_count()
    
    @allure.step("Remove button")
    def remove_button_and_get_count(self) -> int:
        self.default_animation.remove_button()
        return self.default_animation.get_buttons_count()

    def restart_app(self) -> None:
       # סגירה ופתיחה מחדש - פקודות ייעודיות ל-SeeTest
        self.driver.execute_script('seetest:client.applicationClose("com.example.android.apis")')
        # פתיחה מחדש - הוספנו את ה-Activity והורדנו מרכאות מה-false
        self.driver.execute_script('seetest:client.launch("com.example.android.apis/.ApiDemos", false, false)')
