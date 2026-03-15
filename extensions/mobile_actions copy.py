import allure
from appium.webdriver.webdriver import WebDriver
from appium.webdriver.webelement import WebElement
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MobileActions:


    @staticmethod
    @allure.step("Get Elements count")
    def get_elements_count(driver:WebDriver, locator):
        elements = driver.find_elements(*locator) 
        return len(elements)

    @staticmethod
    def click(driver:WebDriver, locator):
    # ה-* לפני ה-locator מפרק את ה-Tuple ל-By.XPATH ולערך שלו
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()
        
    # @staticmethod
    # @allure.step("Get elements count using len")
    # def get_elements_count(driver: WebDriver, locator_type: By, locator_value: str) -> int:
    #     return len(driver.find_elements(locator_type, locator_value))


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