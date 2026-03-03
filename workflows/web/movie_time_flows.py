import allure
from playwright.sync_api import Locator, Page
from data.web.movie_time_data import *
from extensions.ui_actions import UIActions
from extensions.web_verifications import WebVerify
from page_objects.web.movie_time_Register_page import MovieTimeRegisterPage
from page_objects.web.movie_time_all_movie_page import MovieTimeAllMoviesPage
from page_objects.web.movie_time_home_page import MovieTimeHomePage
from page_objects.web.movie_time_login_page import MovieTimeLoginPage
from page_objects.web.movie_time_navigation_menu_page import MovieTimeNavigationMenu


class MovieFlows:
    def __init__(self,page:Page):
        self.page = page
        self.login = MovieTimeLoginPage(page)
        self.home = MovieTimeHomePage(page)
        self.all_movies = MovieTimeAllMoviesPage(page)
        self.navigation = MovieTimeNavigationMenu(page)
        self.register = MovieTimeRegisterPage(page)
    

    @allure.step("Navigate to all Movies:")
    def navigate_to_all_movies(self) -> None:
        UIActions.force_click(self.all_movies.all_movies_header)

    @allure.step("Navigate to all section")
    def navigate_to_all_category(self) -> None:
        UIActions.force_click(self.all_movies.movie_genre_button.first)


    @allure.step("Enter keyword to search bar")
    def search_a_movie_name(self,keyword:str) -> None:
        UIActions.force_click(self.all_movies.all_movies_header)     
        UIActions.update_text(self.all_movies.movie_search_bar,keyword)
        UIActions.click(self.all_movies.search_button)


    @allure.step("Choose sorting method")
    def choose_sorting_method(self, option:str) -> None:
         self.all_movies.sorting_selector.select_option(option)
   
   
    @allure.step("Get rating list")
    def get_rating_list(self) -> list:
        rating_list = UIActions.get_text_list(self.all_movies.movie_rating)
        scores = []
        for score in rating_list:
            if score != "Unrated":
                score = float(score.replace("★",""))
                scores.append(score)
        return(scores)

    @allure.step("Get title list")
    def get_title_list_text(self) -> list:
        title_list = UIActions.get_text_list(self.all_movies.movie_title)
        return title_list


    @allure.step("Get year list") 
    def get_year_list(self) -> list:
        year_list = UIActions.get_text_list(self.all_movies.movie_year)
        return year_list

    @allure.step("Get top movie")  
    def get_top_movie(self,movie_list:list) -> str:
        return movie_list[0]

    @allure.step("Filter by genre name and count movies")
    def get_movie_count_by_genre_name(self, genre_name: str) -> int:
        target_genre = self.all_movies.movie_genre_button.filter(has_text=genre_name)
        UIActions.force_click(target_genre)
        return UIActions.count(self.all_movies.movie_title)
    
    @allure.step("Get Navigation header text")
    def get_page_header(self, button_name: str) -> str:
        if button_name.lower() == 'theme':
            target = self.navigation.theme_switch_button
        else:
            target = self.navigation.menu_links.filter(has_text=button_name).first
        
        UIActions.click(target)
        return UIActions.get_text(self.navigation.page_header)
     

    

    
            

            



        

    


  
  
    


            

        
      
        


