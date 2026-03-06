import allure
import pytest
from data.web.movie_time_data import *
from extensions.web_verifications import WebVerify
from utils.common_ops import read_data_from_csv
from workflows.web.movie_time_flows import MovieFlows

CATEGORY_DATA_PATH = r"data\ddt\all_movie_category.csv"

class TestMovieCategoryDDT:

    @allure.title("Test - Verify Category Count by Name")
    @allure.description("This test verifies movie count for each genre using CSV data and Genre Name")
    @pytest.mark.parametrize("category_data", read_data_from_csv(CATEGORY_DATA_PATH))
    def test_verify_categories_count_ddt(self, movie_time_flows: MovieFlows, category_data):
        movie_time_flows.navigate_to_all_movies()
        actual_count = movie_time_flows.get_movie_count_by_genre_name(category_data["genre_name"])
        expected_count = int(category_data["expected_count"])
        WebVerify.values_are_equal(actual_count,expected_count,message=f"Count mismatch for genre: {category_data['genre_name']}")





