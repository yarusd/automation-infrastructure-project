import allure
from playwright.sync_api import Page
from data.web.movie_time_data import *
from extensions.ui_actions import UIActions
from extensions.web_verifications import WebVerify
from page_objects.web.movie_time_all_movie_page import MovieTimeAllMoviesPage
from page_objects.web.movie_time_home_page import MovieTimeHomePage
from page_objects.web.movie_time_login_page import MovieTimeLoginPage


class MovieFlows:
    def __init__(self,page:Page):
        self.page = page
        self.login = MovieTimeLoginPage(page)
        self.home = MovieTimeHomePage(page)
        self.all_movies = MovieTimeAllMoviesPage(page)

    @allure.step("Sign in:")
    def sign_in(self,user_name:str,password:str) -> None:
        UIActions.update_text(self.login.user_name_field,user_name)
        UIActions.update_text(self.login.password_field,password)
        UIActions.click(self.login.submit_button)

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