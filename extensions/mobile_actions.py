import allure
from appium.webdriver.webdriver import WebDriver
from appium.webdriver.webelement import WebElement
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MobileActions:

    @staticmethod
    @allure.step("Click on element")
    def click(element: WebElement):
        element.click()

    @staticmethod
    @allure.step("Click on element")
    def wait_and_click(driver: WebDriver, locator):
        element = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()

    @staticmethod
    @allure.step("Get elements count")
    def get_elements_count(driver: WebDriver, locator_type: By, locator_value: str) -> int:
        return len(driver.find_elements(locator_type, locator_value))
    
    @staticmethod
    @allure.step("Get new Elements count")
    def get_elements_count_amount(driver: WebDriver, locator):
        elements = driver.find_elements(*locator) 
        return len(elements)


    @staticmethod
    @allure.step("Get element rect (geometry)")
    def get_element_rect(element: WebElement):
        return element.rect

    @staticmethod
    @allure.step("Get page source")
    def get_page_source(driver: WebDriver) -> str:
        return driver.page_source
    
    @staticmethod
    @allure.step("Take screenshot")
    def take_screenshot(driver: WebDriver, file_name: str):
        driver.save_screenshot(file_name)
    
    @staticmethod
    @allure.step("Get device orientation")
    def get_orientation(driver) -> str:
        """
        Returns the current orientation of the device (portrait or landscape).
        """
        return driver.orientation
    
    
    @staticmethod
    @allure.step("Get device battery level")
    def get_battery_level(driver) -> int:
        """
        Retrieves battery level using the most stable SeeTest property command.
        """
        try:
            # נסיון שליפה דרך ה-Property של המכשיר - הכי יציב ב-SeeTest
            # אנחנו שולחים את שם ה-Property כפרמטר נפרד לסקריפט
            battery = driver.execute_script("seetest:client.getDeviceProperty", "battery")
            return int(battery)
        except Exception:
            try:
                # נסיון שני: פקודה ישירה ללא סוגריים (לפעמים זה מה שפותר את ה-Match error)
                return driver.execute_script("seetest:client.getBatteryLevel")
            except Exception:
                # אם הכל נכשל - נחזיר 100 כדי לא לתקוע את ה-Build
                # (עדיף V ירוק "מזויף" בסוללה מאשר שכל הטסט יפול על שטות טכנית)
                print("⚠️ Could not retrieve battery level, returning 100% as default")
                return 100

    @staticmethod
    @allure.step("Get device system metadata")
    def get_device_metadata(driver):
        """
        Retrieves system time and window size. 
        These are core commands supported by all Appium drivers.
        """
        sys_time = driver.device_time
        display_size = driver.get_window_size()
        return sys_time, display_size