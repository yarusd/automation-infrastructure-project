import allure
import pytest
from data.web.movie_time_data import *
from extensions.web_verifications import WebVerify
from utils.common_ops import read_data_from_csv
from workflows.web.movie_time_flows import MovieFlows


ALL_MOVIES_DATA_PATH = r"data\ddt\search_data.csv"

class TestAllMoviesSearchDDT:

    @allure.title("Test - Verify SEARCH with DDT")
    @allure.step("This test verify SEARCH results")
    @pytest.mark.parametrize("movies",read_data_from_csv(ALL_MOVIES_DATA_PATH))
    def test_verify_search_bar_results_ddt(self,movie_time_flows: MovieFlows,movies,navigate_to_all_movies_page):

        movie_time_flows.search_a_movie_name(movies["keyword"])
        WebVerify.verify_search_results(
            keyword = movies["keyword"],
            elements = movie_time_flows.all_movies.movie_title,
            expected_count = movies["expected_total_search_results"],
            search_type = movies["search_type"] )
