import allure
from extensions.mobile_actions import MobileActions
from appium.webdriver.webdriver import WebDriver
from page_objects.mobile.api_demo_default_animation_page import DefaultAnimationPage
from page_objects.mobile.api_demo_page_yarus import MobileItemsPageYarus

class MobileFlowsYarus:
    def __init__(self, driver:WebDriver): 
        self.driver = driver 
        self.mobile_page = MobileItemsPageYarus(driver)
        self.default_animation = DefaultAnimationPage(driver)


    # @allure.step("Get the total count of items on screen")
    # def get_items_count(self) -> int:
    #     return len(self.mobile_page.categories)
    
    @allure.step("Get the total count of items on screen")
    def get_items_count(self) -> int:
    # קוראים ל-MobileActions כדי שיבצע find_elements אמיתי
        return MobileActions.get_elements_count(self.driver, self.mobile_page.categories)
    

    # @allure.step("Get ListView count from page source")
    # def get_list_view_count_from_source(self) -> int:
    #     return MobileActions.get_elements_count(self.driver, "ListView")
    
    @allure.step("Get ListView count from page source")
    def get_list_view_count_from_source(self) -> int:
        # אנחנו פשוט קוראים ללוקייטור שהגדרנו בדף
        return MobileActions.get_elements_count(self.driver, self.mobile_page.LIST_VIEW)
    
    @allure.step("Navigate to Default Layout Animation page")
    def go_to_default_animation_page(self) -> None :
        MobileActions.click(self.driver, self.mobile_page.animation_category)
        MobileActions.click(self.driver, self.mobile_page.default_animetion)
    
    @allure.step("Add a button")
    def add_a_new_button(self) -> None:
        MobileActions.click(self.driver, self.default_animation.add_button)

    @allure.step("Click on added button")
    def click_on_added_button(self) -> None:
        MobileActions.click(self.driver, self.default_animation.new_buttons)

    @allure.step("Get buttons count")
    def get_animation_buttons_count(self) -> int :
        buttons_count = MobileActions.get_elements_count(self.driver, self.default_animation.new_buttons)
        return buttons_count
    

# @pytest.fixture(scope="class")
# def mobile_setup():
#         dc = {}
#         dc['udid'] = 'RF8N63P9Z9R'
#         dc['appPackage'] = 'com.example.android.apis'
#         dc['appActivity'] = '.ApiDemos'
#         dc['platformName'] = 'android'
#         driver = webdriver.Remote('http://localhost:4724/wd/hub',dc)
#         driver.implicitly_wait(10)
#         yield driver
#         driver.quit()

# @pytest.fixture(scope="function")
# def mobile_flows(mobile_setup):
#     # Injecting the driver instance into the business logic layer
#     return MobileFlowsYarus(mobile_setup)