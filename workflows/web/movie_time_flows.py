import allure
from playwright.sync_api import Locator, Page
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

    @allure.step("Print movies list")
    def print_movies(self) -> None:
        self.all_movies.all_movies_header.click()
        movie_list = self.all_movies.movie_title.all_inner_texts()
        print("\nMovies list:")
        for i, movie in enumerate(movie_list):
            print(f"{i+1} - {movie}")
    
    @allure.step("Get total movies count")
    def get_total_movies_count(self) -> int:
        return UIActions.count(self.all_movies.movie_title)
    
    @allure.step("Click and count each movie category films")
    def count_each_movie_genre_category(self) ->int:
        self.all_movies.all_movies_header.click()
        movies_genre = self.all_movies.movie_genre_button.all()
        for genre in movies_genre:
            UIActions.click(genre)
        return UIActions.count(self.all_movies.movie_title)

    @allure.step("Get expected categoy count")
    def get_expected_genre_category_count(self,expected_category_count:list):
        self.all_movies.all_movies_header.click()
        for movie in expected_category_count:
            pass
        return movie
    
    @allure.step("Enter keyword to search bar")
    def search_a_movie_name(self,text:str) -> None:
        self.all_movies.all_movies_header.click()     
        UIActions.update_text(self.all_movies.movie_search_bar,text)
        UIActions.click(self.all_movies.search_button)

    @allure.step("Check keyword in search results")
    def check_search_text_in_search_results(self) -> Locator:
        search_results_list = self.all_movies.movie_title.all()
        for search in search_results_list:
            pass
        return search
         
      
        




      
        





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
            WebVerify.contain_text(self.login.error_message)