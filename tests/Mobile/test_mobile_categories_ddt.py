import allure
import pytest
from data.web.movie_time_data import *
from extensions.mobile_verifications import MobileVerify
from utils.common_ops import read_data_from_csv
from workflows.mobile.mobile_flow import MobileFlows

CATEGORIES_DATA_PATH = r"data\mobile\mobile_categories_data.csv"

class TestMobileCategoriesDDT:

    @allure.title("Test - Verify each category Count by Name")
    @allure.description("This test verifies category count for each category using CSV data and Name")
    @pytest.mark.parametrize("categories_data", read_data_from_csv(CATEGORIES_DATA_PATH))
    def test_verify_each_category_count_ddt(self, mobile_flows:MobileFlows, categories_data):

        actual_count = mobile_flows.click_and_count_list(categories_data["category_name"])
        expected_count = categories_data["expected_count"]
        mobile_flows.go_back()

        MobileVerify.values_are_equal(actual_count,expected_count,
                                   f"Count mismatch for genre: {categories_data['category_name']}")


