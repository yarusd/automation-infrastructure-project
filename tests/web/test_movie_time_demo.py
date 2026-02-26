import allure

from data.web.movie_time_data import *
from extensions.web_verifications import WebVerify
from workflows.web.movie_time_flows import MovieFlows

class TestMovieTimeDemoWeb:

    
    @allure.title("Movie Display Count Validation")
    @allure.description("Validates UI movie count vs header indicator")
    def test_verify_movie_icons_count(self,movie_time_flows:MovieFlows):
        actual_icons = movie_time_flows.get_actual_now_showing_icons()
        expected_icons = movie_time_flows.get_expected_now_showing_icons()
        WebVerify.values_are_equal(actual_icons,expected_icons,"Error - Values Not Equal")


    @allure.title("Guest Booking Error Check")
    @allure.description("Verifies error on booking without login")
    def test_verify_invalid_booking_in_guest_mode(self,movie_time_flows:MovieFlows):
        actual_booking_error_message = movie_time_flows.get_booking_process_in_guest_mode()
        WebVerify.contain_text(actual_booking_error_message,expected_booking_error_message,"Error - Message Not Equal")

    @allure.title("Verify Movie Details Redirection")
    @allure.description("Checks that clicking 'Details' leads to the correct movie description.")
    def test_verify_details_button_leads_to_description(self,movie_time_flows:MovieFlows):
        actual_movie_description = movie_time_flows.navigate_to_movies_description()
        WebVerify.strings_are_equal(actual_movie_description,expected_movie_description)