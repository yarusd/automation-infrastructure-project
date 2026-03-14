import allure
import pytest
from data.web.movie_time_data import *
from extensions.web_verifications import WebVerify
from workflows.web.movie_time_flows import MovieFlows

class TestMovieTimeHomepage:

    
    @allure.title("Homepage Movie Display Count Validation")
    @allure.description("Validates UI movie count vs header indicator")
    def test01_verify_now_showing_icons_count(self,movie_time_flows:MovieFlows):
        actual_icons_count = movie_time_flows.get_actual_now_showing_icons_count()
        expected_icons_count = movie_time_flows.get_expected_now_showing_icons__count()
        WebVerify.values_are_equal(actual_icons_count,expected_icons_count,"Error - Values Not Equal")

   
    @allure.title("Guest Mood Invalid Booking Message")
    @allure.description("Verifies error message on booking without login")
    def test02_verify_invalid_booking_in_guest_mode(self,movie_time_flows:MovieFlows,navigate_to_homepage):
        actual_booking_error_message = movie_time_flows.get_error_booking_process_message()
        WebVerify.contain_text(actual_booking_error_message,EXPECTED_BOOKING_ERROR_MESSAGE)

    allure.title("Verify Movie Details Redirection")
    allure.description("Verifies that clicking 'Details' leads to the correct movie description.")
    def test03_verify_details_button_leads_to_description(self,movie_time_flows:MovieFlows,navigate_to_homepage):
        movie_time_flows.click_on_details_button()
        actual_movie_description = movie_time_flows.get_movie_description()
        WebVerify.strings_are_equal(actual_movie_description,EXPECTED_MOVIE_DESCRIPTION,"Error - Movie description mismatch")


    @allure.title("Verify Theme Toggle Switches to Light Mode (AI Vision)")
    @allure.description("Verifies that clicking the 'Theme Toggle' button displays the light mode view.(with AI)")
    @pytest.mark.xfail(reason="Bug: AI fails to detect light mode transition / Site rendering issue")
    def test04_verify_theme_toggle_leads_to_light_mode_with_vision(self, movie_time_flows: MovieFlows,navigate_to_homepage):
        movie_time_flows.click_on_Theme_Toggle()
        is_light_mode = movie_time_flows.verify_theme_with_vision(expected_mode="light mode")
        WebVerify.is_true(is_light_mode, "Error - AI detected that the site is NOT in light mode")

    
    @allure.title("Verify 'Already have an account' Navigation")
    @allure.description("Validate that clicking the login link on the Register page correctly redirects the user to the Login page.")
    def test05_verify_navigation_to_login_page(self,movie_time_flows: MovieFlows):
        movie_time_flows.go_to_login_page_from_register()
        WebVerify.visible(movie_time_flows.login.login_header)
    

    @allure.title("Verify 'Register here' button Navigation")
    @allure.description("Validate clicking the Register here button on login page redirects the user to the register page.")
    def test006_verify_navigation_to_register_page(self,movie_time_flows: MovieFlows):
        movie_time_flows.go_to_login_page_from_register()
        WebVerify.visible(movie_time_flows.register.register_header)

    
    
    @allure.title("Verify homepage movies slider functional")
    @allure.description("Verify movie details is changed by clicking left and right arrows")
    def test06_verify_movie_slider_navigation(self,movie_time_flows: MovieFlows,navigate_to_homepage):
        movie_title = movie_time_flows.home.movie_on_slider
        current_movie_title = movie_time_flows.get_text(movie_title)

        movie_time_flows.click_on_next_slider()
        next_movie_title = movie_time_flows.get_text(movie_title)

        movie_time_flows.click_on_previous_slider()
        previous_movie_title = movie_time_flows.get_text(movie_title)
        WebVerify.slider_navigation(current_movie_title,next_movie_title,previous_movie_title)
        



