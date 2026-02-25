import re

from playwright.sync_api import Locator, expect
from smart_assertions import soft_assert, verify_expectations
import allure

class WebVerify:
  
    @staticmethod    
    @allure.step("Verify that the element has text")
    def text(element: Locator, expected_text: str):
        """
        Verifies that the text of the element matches the expected text.
        """
        expect(element).to_have_text(expected_text)

    @staticmethod
    @allure.step("Verify String")
    def strings_are_equal(actual:str,expected:str,message:str =None):
        assert actual == expected,message


    @staticmethod
    @allure.step("Verify that the element is visible")
    def visible(element: Locator):
        """
        Verifies that the element is visible.
        """
        expect(element).to_be_visible()
    
    @staticmethod
    @allure.step("Verify that the element is not visible")
    def not_visible(element: Locator):
        """
        Verifies that the element is not visible.
        """
        expect(element).not_to_be_visible()
    
    @staticmethod
    @allure.step("Verifies that the number of elements matching the locator is equal to the expected count")
    def count(element: Locator, count: int):
        """
        Verifies that the number of elements matching the locator is equal to the expected count.
        """
        expect(element).to_have_count(count)

    @staticmethod
    @allure.step("Verify that the element contains the expected text")
    def contain_text(element: Locator, expected_text: str):
         """
        Verifies that the text of the element contains the expected text,
        ignoring differences in uppercase/lowercase.
        """
        # regex case-insensitive
         expect(element).to_contain_text(re.compile(expected_text, re.IGNORECASE))

    @staticmethod
    @allure.step("Verify that a list of strings contains the expected text")
    def contain_text_list(elements: list[str], expected_text: str):
        """
        Verifies that at least one string in the list contains the expected text,
        ignoring differences in uppercase/lowercase.
        If the list is empty, the assertion fails.
        """
        combined_text = " ".join(elements)  # מחברים את כל התוצאות למחרוזת אחת
        if not re.search(expected_text, combined_text, re.IGNORECASE):
            raise AssertionError(f"Expected '{expected_text}' to be in '{combined_text}'")
    
    @staticmethod
    @allure.step("Verify that the element has the expected value")
    def value(element: Locator, expected_value: str):
        """
        Verifies that the value of the element matches the expected value.
        """
        expect(element).to_have_value(expected_value)
    
    @staticmethod
    @allure.step("Verify that list is sorted by first word (A-Z)")
    def list_is_sorted_by_first_word(values: list[str]):
        """
        בודק שהרשימה ממוינת לפי המילה הראשונה בלבד (A-Z), התעלמות מה-Case
        """
        first_words = [v.split()[0].lower() for v in values]
        assert first_words == sorted(first_words), f"Titles are not sorted by first word. {first_words}"


    # Soft Assertions    
    @staticmethod
    @allure.step("Soft assertion to check if the element has the expected text")
    def soft_text(element: Locator, expected_text: str, message: str):
        """
        Soft assertion to check if the element has the expected text.
        Test execution will continue even if this assertion fails.
        """
        actual_text = element.inner_text()
        soft_assert(actual_text == expected_text, message)

    @staticmethod
    @allure.step("Soft assertion to check if two integers are equal")
    def soft_int(actual: int, expected: int, message:str= None):
        """
        Soft assertion to compare two integers.
        Test execution will continue even if this assertion fails.
        """
        soft_assert(actual == expected, message)

    @staticmethod
    @allure.step("Soft assertion to check if the element is visible")
    def soft_is_visible(element: Locator, message: str):
        """
        Soft assertion to check if the element is visible.
        Test execution will continue even if this assertion fails.
        """
        soft_assert(element.is_visible(), message)

    @staticmethod
    @allure.step("Raises all collected assertion errors at once")
    def soft_all():
        """Raises all collected assertion errors at once."""
        verify_expectations()



        