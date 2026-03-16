import allure
from appium.webdriver.webelement import WebElement

class MobileVerify:

    @staticmethod
    @allure.step("Verify values are equal")
    @allure.step("Verify Values are equal")
    def values_are_equal(actual ,expected ,message=None):
        assert float(actual) == float(expected),message or "Expected equal strings but both were different"

    @staticmethod
    @allure.step("Verify button was added. Initial count: {initial_count}, New count: {new_count}")
    def verify_button_added(initial_count: int, new_count: int):
        assert new_count == initial_count + 1, f"Expected {initial_count + 1} buttons, but found {new_count}"

    
    @staticmethod
    @allure.step("Verify button was deleted. Initial count: {initial_count}, New count: {new_count}")
    def verify_button_deleted(initial_count: int, new_count: int):
        assert new_count == initial_count - 1, f"Expected {initial_count - 1} buttons, but found {new_count}"

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
        

    @staticmethod
    @allure.step("Verify device orientation")
    def verify_orientation(actual):
        # Log orientation status
        print(f"\n📱 Device Orientation: {actual.capitalize()}")
        
        # Validate orientation is portrait
        assert actual == "portrait",f"Device is in Landscape mode"


    @staticmethod
    @allure.step("Verify device battery level")
    def verify_battery_status(battery_level):
        # Log battery status to console
        print(f"\n🔋 Current Battery Level: {battery_level}%")
        
        # Ensure battery is sufficient for testing (above 20%)
        MobileVerify.is_true(battery_level > 20, f"Battery level too low: {battery_level}%")

    @staticmethod
    @allure.step("Verify condition is true")
    def is_true(condition: bool, message: str = "Assertion failed: expected True but got False"):
        """
        General boolean assertion to verify that a condition is met.
        """
        assert condition, message


    @staticmethod
    @allure.step("Verify device heartbeat data")
    def verify_heartbeat(time, size):
        # Log metadata to console
        print(f"\n⌚ Device Time: {time}")
        print(f"📏 Resolution: {size['width']}x{size['height']}")

        # Soft Assert: Collect all failures before asserting
        errors = []
        if not time: 
            errors.append("System time is empty")
        if size['width'] <= 0 or size['height'] <= 0: 
            errors.append(f"Invalid resolution: {size['width']}x{size['height']}")

        # Final validation
        assert not errors, f"Heartbeat verification failed: {', '.join(errors)}"