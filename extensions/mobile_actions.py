import allure
from appium.webdriver.webdriver import WebDriver
from appium.webdriver.webelement import WebElement
from selenium.webdriver.common.by import By 

class MobileActions:

    @staticmethod
    @allure.step("Click on element")
    def click(element: WebElement):
        element.click()

    @staticmethod
    @allure.step("Get elements count")
    def get_elements_count(driver: WebDriver, locator_type: By, locator_value: str) -> int:
        return len(driver.find_elements(locator_type, locator_value))

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