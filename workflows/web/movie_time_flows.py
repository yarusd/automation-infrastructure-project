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
    def get_expected_genre_category_count(self,expected_category_count:list) -> Locator:
        self.all_movies.all_movies_header.click()
        for movie in expected_category_count:
            pass
        return movie
    

    @allure.step("Enter keyword to search bar")
    def search_a_movie_name(self,text:str) -> None:
        UIActions.force_click(self.all_movies.all_movies_header)     
        UIActions.update_text(self.all_movies.movie_search_bar,text)
        UIActions.click(self.all_movies.search_button)

    @allure.step("Check keyword in search results")
    def check_search_text_in_search_results(self) -> Locator:
        search_results_list = self.all_movies.movie_title.all()
        for search in search_results_list:
            pass
        return search
    
    @allure.step("Choose sorting method")
    def choose_sorting_method(self, option:str) -> None:
        self.all_movies.all_movies_header.click()
        self.all_movies.sorting_selector.select_option(option)

    @allure.step("Get rating list")
    def get_rating_list(self) -> list:
        rating_list = self.all_movies.movie_rating.all_inner_texts()
        list = []
        for score in rating_list:
            if score == "Unrated":
                pass
            else:
                score = float(score.replace("★",""))
                list.append(score)
        return(list)

    @allure.step("Get title list")
    def get_title_list_text(self) -> list:
        title_list = self.all_movies.movie_title.all_inner_texts()
        return title_list

    @allure.step("Get year list") 
    def get_year_list(self) -> list:
        year_list = self.all_movies.movie_year.all_inner_texts()
        return year_list

    @allure.step("Get top movie")  
    def get_top_movie(self,list:list) -> str:
        top = max(list)
        return top

    @allure.step("Search by actor name and return results count")
    def search_by_actor_and_get_count(self, actor_name: str) -> int:
        self.all_movies.all_movies_header.click()
        UIActions.update_text(self.all_movies.movie_search_bar, actor_name)
        UIActions.click(self.all_movies.search_button)
        self.page.wait_for_timeout(1000)
        return self.all_movies.movie_title.count()  
    

    @allure.step("Search category name in search bar and return count")
    def search_category_in_search_bar_and_get_count(self, category_name: str) -> int:
        self.all_movies.all_movies_header.click()
        UIActions.update_text(self.all_movies.movie_search_bar, category_name)
        UIActions.click(self.all_movies.search_button)
        self.page.wait_for_timeout(1000)
        return self.all_movies.movie_title.count()

  

    

    
            

            
            
       

            
        # top_score = self.all_movies.movie_rating.first.inner_text()
        


        

    


  
  
    


            

        
      
        


