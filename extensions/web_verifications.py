import re

from playwright.sync_api import Locator, expect
import pytest
from smart_assertions import soft_assert, verify_expectations
import allure

from extensions.ui_actions import UIActions
from page_objects.web.movie_time_login_page import MovieTimeLoginPage

class WebVerify:
  
    @staticmethod    
    @allure.step("Verify that the element has text")
    def text(element: Locator, expected_text: str):
        """
        Verifies that the text of the element matches the expected text.
        """
        expect(element).to_have_text(expected_text)

    @staticmethod
    @allure.step("Verify login flow:")
    def verify_log_in(page,login:MovieTimeLoginPage,expected_status:str)->str:
       if expected_status == "True":
            WebVerify.visible(login.actual_log_in_header)
            UIActions.click(login.log_out_button)
       else:
            WebVerify.visible(login.error_message)
            page.reload()

    @staticmethod
    @allure.step("Verify String")
    def strings_are_equal(actual:str,expected:str,message:str=None):
        assert actual == expected,message or "EROOR - not matched"

  
    @staticmethod
    @allure.step("Verify Values")
    def values_are_equal(actual:float,expected:float,message=None):
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
    @allure.step("Verifies that the number of elements matching the locator is equal to the expected count")
    def count(element: Locator, count: str):
        """
        Verifies that the number of elements matching the locator is equal to the expected count.
        """
        expect(element).to_have_count(int(count))


    @staticmethod
    @allure.step("Verify search results for {search_type}")
    def verify_search_results(keyword: str, elements: Locator, expected_count: str, search_type: str):
        elements_list = elements.all_inner_texts()
        actual_count = len(elements_list)
        expected_count_int = int(expected_count)

        assert actual_count == expected_count_int, \
            f"DDT Failure: Search by {search_type} for '{keyword}' expected {expected_count_int} results, but found {actual_count}."

        if search_type == 'movie_name':
            result = all(keyword.lower() in item.lower() for item in elements_list)
            assert result, f"Text mismatch: The movie name '{keyword}' was not found in all returned titles: {elements_list}"
        

        
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


    @staticmethod
    @allure.step("Verify element is in list and count is correct")
    def verify_in_list(keyword: str, elements: Locator, expected_count: str):
        elements_list = elements.all_inner_texts()

        assert len(elements_list) == int(expected_count), \
            f"List - {len(elements_list)} count does not match expected count {int(expected_count)}"

        #Perform this test as well, only if the len of the list is as expected
        result = all(keyword.lower() in item.lower() for item in elements_list)
        assert result ,f"{keyword} was not found in all list items - {elements_list}"
        


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

    @staticmethod
    @allure.step("Verify all elements contain: {expected_text}")
    def all_elements_contain_text(locator: Locator, expected_text: str):
        # המתן שהאלמנטים יהיו גלויים
        locator.first.wait_for(state="visible")
        
        titles = locator.all_text_contents()
        for title in titles:
            assert expected_text.lower() in title.lower(), \
                f"Expected '{expected_text}' to be in '{title}'"


    @staticmethod
    @allure.step("Verify Condition is True")
    def is_true(condition: bool, message: str = None):
        assert condition, message or "ERROR - Condition is not True"

        