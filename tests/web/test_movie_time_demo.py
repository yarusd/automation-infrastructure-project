import allure
from data.web.movie_time_data import *
from extensions.web_verifications import WebVerify
from workflows.web.movie_time_flows import MovieFlows
from smart_assertions import  verify_expectations

class TestMovieTimeDemoWeb:

    @allure.title("Test - all movies page")
    @allure.description("This test verify movies count  is valid")
    def test_verify_all_movies_count(self,movie_time_flows:MovieFlows):
        movie_time_flows.print_movies()
        assert movie_time_flows.get_total_movies_count() == EXPECTED_TOTAL_MOVIES

    @allure.title("Test - Movies category count") 
    @allure.description("This test will verify if count of category is valid")   
    def test01_verify_movies_count_for_each_genre(self,movie_time_flows:MovieFlows):
        actual_movie_count = movie_time_flows.count_each_movie_genre_category()
        expected_movie_count = movie_time_flows.get_expected_genre_category_count(EXPECTED_GENRE_MOVIE_COUNT)
        WebVerify.soft_int(actual_movie_count,expected_movie_count)
        verify_expectations() 

    @allure.title("Test- Valid search bar function")
    @allure.description("This test verify search bar results")
    def test02_verify_search_bar_results(self,movie_time_flows:MovieFlows):
        movie_time_flows.search_a_movie_name(SEARCH_KEYWORD)
        WebVerify.contain_text(movie_time_flows.check_search_text_in_search_results(),SEARCH_KEYWORD)

    @allure.title("Test - Valid rating sorting selector")   
    @allure.description("This test verify top rating shown after sorting by rating")
    def test03_verify_top_rating_display(self, movie_time_flows:MovieFlows):
        movie_time_flows.choose_sorting_method(SORT_BY_RATING)
        actual_top_rating =movie_time_flows.get_top_movie(movie_time_flows.get_rating_list())
        WebVerify.strings_are_equal(actual_top_rating,TOP_SCORE)
    
    @allure.title("Test - Valid title sorting selector ")
    @allure.description("This test verify sorting by title")
    def test04_verify_title_sorting_display(self, movie_time_flows: MovieFlows):
        movie_time_flows.choose_sorting_method(SORT_BY_TITLE)
        WebVerify.list_is_sorted_by_first_word(movie_time_flows.get_title_list_text())

    @allure.title("Test - Valid year sorting selector")
    @allure.description("This test verify sorting by year")
    def test05_verify_year_sorting_display(self, movie_time_flows: MovieFlows):
        movie_time_flows.choose_sorting_method(SORT_BY_YEAR)
        WebVerify.strings_are_equal(movie_time_flows.get_top_movie(movie_time_flows.get_year_list()),RECENT_YEAR)

    @allure.title("Test - Search by actor name")
    @allure.description("This test verify searching for an actor returns the correct number of movies")
    def test06_verify_actor_search_count(self, movie_time_flows: MovieFlows):
        actual_count = movie_time_flows.search_by_actor_and_get_count(ACTOR_NAME)
        WebVerify.soft_int(actual_count, EXPECTED_ACTOR_SEARCH_COUNT, f"No results")
        verify_expectations()

    @allure.title("Test - Search Category via Search Bar")
    def test07_verify_category_search_via_bar(self, movie_time_flows: MovieFlows):
        actual = movie_time_flows.search_category_in_search_bar_and_get_count(SEARCH_CATEGORY)
        WebVerify.soft_int(actual, EXPECTED_CATEGORY_SEARCH_COUNT, f"No results")
        verify_expectations()



    


        


    