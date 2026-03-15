from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.common.by import By



class DefaultAnimationPage:
    def __init__(self, driver:WebDriver):
        self.driver = driver 
    
    add_button = (By.ID, "addNewButton")
    new_buttons = (By.XPATH, "//*[@id='gridContainer']/android.widget.Button")
        