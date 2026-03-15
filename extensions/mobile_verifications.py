import allure
from appium.webdriver.webelement import WebElement

class MobileVerify:

    @staticmethod
    @allure.step("Verify values are equal")
    def values_equal(actual, expected, message: str = None):
        """
        General comparison between two values (numbers or strings).
        """
        assert actual == expected, message or f"Expected '{expected}', but got '{actual}'"

    @staticmethod
    @allure.step("Verify element is displayed")
    def is_displayed(element: WebElement, message: str = "Element should be visible"):
        """
        Verifies that the given element is displayed on the screen.
        """
        assert element.is_displayed(), message

    @staticmethod
    @allure.step("Verify element text")
    def text(element: WebElement, expected_text: str):
        """
        Verifies that the element's text matches the expected string exactly.
        """
        actual_text = element.text
        assert actual_text == expected_text, f"Expected text '{expected_text}', but got '{actual_text}'"

    @staticmethod
    @allure.step("Verify list count")
    def list_count(elements_list: list, expected_count: int):
        """
        Verifies that the number of items in a list matches the expected count.
        """
        actual_count = len(elements_list)
        assert actual_count == expected_count, f"Expected {expected_count} items, but found {actual_count}"

    @staticmethod
    @allure.step("Verify element contains text")
    def contains_text(element: WebElement, expected_substring: str):
        """
        Verifies that the element's text contains the expected substring (case-insensitive).
        """
        actual_text = element.text
        assert expected_substring.lower() in actual_text.lower(), \
             f"Expected '{expected_substring}' to be part of '{actual_text}'"