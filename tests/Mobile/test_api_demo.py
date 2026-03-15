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