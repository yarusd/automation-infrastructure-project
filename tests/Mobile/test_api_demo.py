import allure
from data.mobile.api_demos import *
from extensions.mobile_verifications import MobileVerify
from workflows.Mobile.mobile_flow import MobileFlows


class TestMobileItems:

    @allure.title("Verify items count on Mobile App")
    @allure.description("This test ensures that exactly 11 items are displayed in the list")
    def test_01_verify_list_count(self, mobile_flows:MobileFlows): 
        actual_count = mobile_flows.get_items_count()
        MobileVerify.values_are_equal(actual_count, EXPECTED_CATEGORIES_COUNT)


    @allure.title("Verify Device Orientation")
    @allure.description("This test verifies that the device is in Portrait mode")
    def test_02_verify_orientation(self, mobile_flows: MobileFlows):
        orientation = mobile_flows.get_device_orientation()
        MobileVerify.verify_orientation(orientation)


    @allure.title("Device Battery Health Test")
    def test_03_verify_battery_level(self, mobile_flows: MobileFlows):
        battery = mobile_flows.get_battery_status()
        MobileVerify.verify_battery_status(battery)


    @allure.title("Device Heartbeat and Connection Test")
    @allure.description("Verifies connectivity by retrieving system time and display metadata")
    def test_04_device_heartbeat(self, mobile_flows: MobileFlows):
        time, size = mobile_flows.check_device_responsiveness()
        MobileVerify.verify_heartbeat(time, size)
    
    @allure.title("Verify Add Button Functionality")
    @allure.description("Verifies that clicking the 'Add Button' successfully increases the total button count by 1.")
    def test05_add_button_functionality(self, mobile_flows: MobileFlows):
        mobile_flows.go_to_default_animation_page()
        
        initial_count = mobile_flows.get_current_buttons_count() 
        mobile_flows.add_button_and_get_count()
        new_count = mobile_flows.get_current_buttons_count()

        MobileVerify.verify_button_added(initial_count,new_count)        

    @allure.title("Verify Delete Button Functionality")
    @allure.description("Verifies that the 'Remove Button' successfully decreases the total button count by 1.")
    def test06_delete_button_functionality(self, mobile_flows: MobileFlows):
        mobile_flows.restart_app() 
        mobile_flows.go_to_default_animation_page()

        count_before = mobile_flows.add_button_and_get_count()
        count_after = mobile_flows.remove_button_and_get_count()
        
        MobileVerify.verify_button_deleted(count_before, count_after)