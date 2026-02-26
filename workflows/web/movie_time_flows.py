import re

import allure
from playwright.sync_api import Page
from data.web.movie_time_data import *
from extensions.ui_actions import UIActions
from extensions.web_verifications import WebVerify
from page_objects.web.movie_time_all_movie_page import MovieTimeAllMoviesPage
from page_objects.web.movie_time_home_page import MovieTimeHomePage
from page_objects.web.movie_time_login_page import MovieTimeLoginPage
from utils.common_ops import extract_digits_from_text


class MovieFlows:
    def __init__(self,page:Page):
        self.page = page
        self.login = MovieTimeLoginPage(page)
        self.home = MovieTimeHomePage(page)
        self.all_movies = MovieTimeAllMoviesPage(page)

    @allure.step("Sign in:")
    def get_actual_now_showing_icons(self)->int:
        return  self.home.actual_now_showing_icon.count()
    
    def get_expected_now_showing_icons(self)->int:
        return extract_digits_from_text(UIActions.get_text(self.home.expected_now_showing_icon))
    
    def get_booking_process_in_guest_mode(self)->str:
        UIActions.click(self.home.book_now_button)
        #return self.home.actual_booking_movie_error_message
        return self.home.actual_booking_movie_error_message

    def navigate_to_movies_description(self):
        UIActions.click(self.home.details_button)
        return self.home.movie_description.inner_text()


    def fill_registration_form_valid_input(self,user_name,password,expected_status)->str:
        UIActions.click(self.home.log_in_icon)
        UIActions.update_text(self.login.email_address_field,user_name)
        UIActions.update_text(self.login.password_field,password)
        UIActions.click(self.login.log_in_button)
        if expected_status == "True":
            WebVerify.visible(self.login.actual_log_in_header)
            UIActions.click(self.login.log_out_button)
        else:
            WebVerify.visible(self.login.error_message)
            self.page.reload()


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