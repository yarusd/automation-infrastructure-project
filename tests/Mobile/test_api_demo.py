import allure
from extensions.web_verifications import WebVerify

class TestMobileItems:

    @allure.title("Verify items count on Mobile App")
    @allure.description("This test ensures that exactly 12 items are displayed in the list")
    def test_01_verify_list_count(self, mobile_flows): # mobile_flows מגיע מה-conftest
        actual_count = mobile_flows.get_items_count()
        WebVerify.values_equal(actual_count, 12)