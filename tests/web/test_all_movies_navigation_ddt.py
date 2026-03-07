import allure
import pytest

from data.web.movie_time_data import *
from extensions.web_verifications import WebVerify
from utils.common_ops import read_data_from_csv
from workflows.web.movie_time_flows import MovieFlows


NAVIGATION_DATA_PATH = r"data\ddt\navigation_data.csv"

class TestAllMoviesNavigationDDT:

    @allure.title("Test - Navigation Menu Header Verification")
    @allure.description("This test verify navigation menu links")
    @pytest.mark.parametrize("nav_data", read_data_from_csv(NAVIGATION_DATA_PATH))
    def test_verify_navigation_menu_headers(self, movie_time_flows: MovieFlows, nav_data):
        actual_header = movie_time_flows.click_and_get_actual_page_header(nav_data["header_name"])
        expected_header = nav_data["expected_header"]
        WebVerify.strings_are_equal(actual_header.upper(), expected_header.upper())


