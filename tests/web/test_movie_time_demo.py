import allure

from data.web.movie_time_data import *
from extensions.web_verifications import WebVerify
from workflows.web.movie_time_flows import MovieFlows

class TestMovieTimeDemoWeb:

    
    @allure.title("Homepage Movie Display Count Validation")
    @allure.description("Validates UI movie count vs header indicator")
    def test01_verify_now_showing_icons_count(self,movie_time_flows:MovieFlows):
        actual_icons_count = movie_time_flows.get_actual_now_showing_icons_count()
        expected_icons_count = movie_time_flows.get_expected_now_showing_icons__count()
        WebVerify.values_are_equal(actual_icons_count,expected_icons_count,"Error - Values Not Equal")


    @allure.title("Guest Mood Invalid Booking Message")
    @allure.description("Verifies error message on booking without login")
    def test02_verify_invalid_booking_in_guest_mode(self,movie_time_flows:MovieFlows):
        actual_booking_error_message = movie_time_flows.get_error_booking_process_message()
        WebVerify.contain_text(actual_booking_error_message,expected_booking_error_message)

    allure.title("Verify Movie Details Redirection")
    allure.description("Verifies that clicking 'Details' leads to the correct movie description.")
    def test03_verify_details_button_leads_to_description(self,movie_time_flows:MovieFlows):
        movie_time_flows.click_on_details_button()
        actual_movie_description = movie_time_flows.get_movie_description()
        WebVerify.strings_are_equal(actual_movie_description,expected_movie_description,"Error - Movie description mismatch")