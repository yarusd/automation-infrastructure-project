import allure
from data.web.movie_time_data import *
from extensions.web_verifications import WebVerify
from workflows.web.movie_time_flows import MovieFlows

class TestMovieTimeAllMoviesPage:
        
    
    @allure.title("Test - Valid rating sorting selector")   
    @allure.description("This test verify top rating shown after sorting by rating")
    def test01_verify_top_rating_display_selector(self, movie_time_flows:MovieFlows, navigate_to_all_movies_page):
        movie_time_flows.choose_sorting_method(SORT_BY_RATING)
        actual_top_rating =movie_time_flows.get_top_movie(movie_time_flows.get_rating_list())
        WebVerify.strings_are_equal(actual_top_rating,TOP_SCORE)
    

    @allure.title("Test - Valid title sorting selector ")
    @allure.description("This test verify sorting by title")
    def test02_verify_title_sorting_display_selector(self, movie_time_flows: MovieFlows,navigate_to_all_movies_page):
        movie_time_flows.choose_sorting_method(SORT_BY_TITLE)
        WebVerify.list_is_sorted_by_first_word(movie_time_flows.get_title_list_text())

    @allure.title("Test - Valid year sorting selector")
    @allure.description("This test verify sorting by year")
    def test03_verify_year_sorting_display_selector(self, movie_time_flows: MovieFlows,navigate_to_all_movies_page):
        movie_time_flows.choose_sorting_method(SORT_BY_YEAR)
        actual_first_movie = movie_time_flows.get_top_movie(movie_time_flows.get_year_list())
        WebVerify.strings_are_equal(actual_first_movie,RECENT_YEAR)

    




    


        


    