import re

import allure
from playwright.sync_api import Page
from data.web.movie_time_data import *
from extensions.ui_actions import UIActions
from extensions.web_verifications import WebVerify
from page_objects.web.movie_time_all_movie_page import MovieTimeAllMoviesPage
from page_objects.web.movie_time_home_page import MovieTimeHomePage
from page_objects.web.movie_time_login_page import MovieTimeLoginPage
from page_objects.web.movie_time_movie_page import MovieTimeMoviePage
from page_objects.web.movie_time_navigation_manu_page import MovieTimeNavigationMenu
from utils.common_ops import extract_digits_from_text
from google import genai
from google.genai import types


class MovieFlows:
    def __init__(self,page:Page):
        self.page = page
        self.login = MovieTimeLoginPage(page)
        self.home = MovieTimeHomePage(page)
        self.all_movies = MovieTimeAllMoviesPage(page)
        self.movie_page = MovieTimeMoviePage(page)
        self.navigation_manu = MovieTimeNavigationMenu(page)

    @allure.step("Sign in:")
    def get_actual_now_showing_icons_count(self)->int:
        return  self.home.actual_now_showing_icon.count()
    
    def get_expected_now_showing_icons__count(self)->int:
        return extract_digits_from_text(UIActions.get_text(self.home.expected_now_showing_icon))
    
    def get_error_booking_process_message(self)->str:
        UIActions.click(self.home.book_now_button)
        return self.home.actual_booking_movie_error_message

    def click_on_details_button(self) -> None:
        UIActions.click(self.home.details_button)

    def get_movie_description(self) -> str:
        return UIActions.get_text(self.movie_page.movie_description)


    def sign_in(self,user_name:str,password:str)->None:
        UIActions.click(self.home.log_in_icon)
        UIActions.update_text(self.login.email_address_field,user_name)
        UIActions.update_text(self.login.password_field,password)
        UIActions.click(self.login.log_in_button)


    @allure.step("Navigte to:")
    def navigate_to(self,url:str)->None:
        UIActions.navigate_to(self.page,url)
   
    @allure.step("Get Home Header")
    def get_home_header(self)->str:
        return UIActions.get_text(self.home.header)
    
    @allure.step("login with ddt:")
    def verify_ddt_flow(self,expected_status)->None: 
        if expected_status == "success":
            WebVerify.text(self.home.header,EXPECTED_HOME_HEADER)
        else:
            WebVerify.contain_text(self.login.error_message,LOGIN_ERROR_MESSAGE)

    
    @allure.step("Click on Theme Toggle Button")
    def click_on_Theme_Toggle(self) -> None:
        UIActions.click(self.navigation_manu.switch_mode_button)


    @allure.step("Verify theme mode with vision")
    def verify_theme_with_vision(self, expected_mode: str) -> bool:
        self.page.wait_for_timeout(1000)
        client = genai.Client(api_key=GEMENI_API_KEY)
        screenshot_bytes = self.page.screenshot(type="png")
        prompt = (
            "Examine the screenshot. Is the main background color of the website white or very light? "
            "Respond with 'Yes' or 'No' only."
        )
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                prompt,
                types.Part.from_bytes(
                    data=screenshot_bytes,
                    mime_type="image/png"
                )
            ]
        )
        result = response.text.strip().lower()
        print(f"\nThe result from AI: {result}")
        return "yes" in result