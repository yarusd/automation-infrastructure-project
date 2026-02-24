import allure
from data.web.movie_time_data import *
from extensions.web_verifications import WebVerify
from workflows.web.movie_time_flows import MovieFlows
from smart_assertions import soft_assert, verify_expectations

class TestMovieTimeDemoWeb:

    @allure.title("Test - all movies page")
    @allure.description("This test verify movies count  is valid")
    def test_verify_all_movies_count(self,movie_time_flows:MovieFlows):
        movie_time_flows.print_movies()
        assert movie_time_flows.get_total_movies_count() == EXPECTED_TOTAL_MOVIES

    @allure.title("Test - Movies category count") 
    @allure.description("This test will verify if count of category is valid")   
    def test_verify_movies_count_for_each_genre(self,movie_time_flows:MovieFlows):
        movie_count = movie_time_flows.count_each_movie_genre_category()
        expected_movie_count = movie_time_flows.get_expected_genre_category_count(EXPECTED_GENRE_MOVIE_COUNT)
        soft_assert(movie_count == expected_movie_count)
        verify_expectations()

    @allure.title("Test- Search bar")
    @allure.description("This test verify search bar results")
    def test_verify_search_bar_results(self,movie_time_flows:MovieFlows):
        movie_time_flows.search_a_movie_name(EXPECTED_SEARCH_KEYWORD)
        WebVerify.contain_text(movie_time_flows.check_search_text_in_search_results(),EXPECTED_SEARCH_KEYWORD)
        

        


    