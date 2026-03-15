from selenium.webdriver.common.by import By

from extensions.mobile_actions import MobileActions

class DefaultAnimationPage:
    
    def __init__(self, driver):
        self.driver = driver

    _ADD_BUTTON = (By.ID, "addNewButton")
    _NEW_BUTTONS = (By.XPATH, "//*[@id='gridContainer']/android.widget.Button")
    _FIRST_NEW_BUTTON = (By.XPATH, "(//*[@id='gridContainer']/android.widget.Button)[1]")


    def add_new_button(self):
        MobileActions.wait_and_click(self.driver, self._ADD_BUTTON)
    
    def remove_button(self):
        MobileActions.wait_and_click(self.driver, self._FIRST_NEW_BUTTON)

    def get_buttons_count(self) -> int:
        return MobileActions.get_elements_count_amount(self.driver, self._NEW_BUTTONS)