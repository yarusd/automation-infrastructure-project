import allure
from conftest import mobile_flows
from extensions.mobile_verifications import MobileVerify
from extensions.web_verifications import WebVerify
from workflows.Mobile.mobile_flow import MobileFlows


class TestMobileItems:

    @allure.title("Verify items count on Mobile App")
    @allure.description("This test ensures that exactly 11 items are displayed in the list")
    def test_01_verify_list_count(self, mobile_flows:MobileFlows): 
        actual_count = mobile_flows.get_items_count()
        MobileVerify.values_equal(actual_count, 11)
