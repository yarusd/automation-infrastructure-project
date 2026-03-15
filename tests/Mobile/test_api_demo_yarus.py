import allure
from conftest import mobile_flows
from extensions.mobile_verifications import MobileVerify
from extensions.web_verifications import WebVerify
from workflows.Mobile.mobile_flow import MobileFlows
from workflows.Mobile.mobile_flows_yarus import MobileFlowsYarus


class TestMobileItemsYarus:

    @allure.title("Verify items count on Mobile App")
    @allure.description("This test ensures that exactly 11 items are displayed in the list")
    def test01_verify_list_count(self, mobile_flows:MobileFlows): 
        actual_count = mobile_flows.get_items_count()
        MobileVerify.values_equal(actual_count, 11)

    
    def test02_add_button_functionality(self, mobile_flows:MobileFlowsYarus):
        mobile_flows.go_to_default_animation_page()
        mobile_flows.add_a_new_button()
        added_buttons = mobile_flows.get_animation_buttons_count()
        MobileVerify.values_equal(added_buttons, 1)


    def test03_delete_button_functionality(self, mobile_flows: MobileFlowsYarus):
        mobile_flows.go_to_default_animation_page()
        mobile_flows.add_a_new_button() 
        #delete button
        mobile_flows.click_on_added_button()
        count_after_delete = mobile_flows.get_animation_buttons_count()
        MobileVerify.values_equal(count_after_delete, 0)
    