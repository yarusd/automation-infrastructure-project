import json
import sqlite3
import allure
database_path = "tests/api/joke_categories.db"
my_db = sqlite3.connect(database_path)

from conftest import request_context
from data.api.chuck_api_data import *
from extensions.api_verifications import APIVerify
from workflows.api.chuck_api_flows import ChuckApiFlows
from utils.common_ops import get_db_categories



class TestChuckAPI:

    #@allure.title("Verify Random Joke Retrieval via GET Request")
    #@allure.description("Verifies that the API successfully returns a random joke with a 200 OK status code")
    def test01_Verify_random_joke_retrieval_via_GET_request(self,chuck_flows:ChuckApiFlows):
        APIVerify.status_code(chuck_flows.search_for_joke(joke),EXPECTED_STATUS_SUCCESS_CODE)

    #@allure.title("Verify Joke Retrieval by Specific Category")
    #@allure.description("Ensures that fetching a joke from a specific category (e.g., 'career') returns a valid response and success status code.")
    def test02_get_random_joke_by_category(self,chuck_flows:ChuckApiFlows):
        APIVerify.status_code(chuck_flows.search_for_joke(career),EXPECTED_STATUS_SUCCESS_CODE)  

    #@allure.title("Verify Retrieval of All Available Joke Categories")
    #@allure.description("Validates that the endpoint for retrieving the full list of joke categories is functional and returns the expected success code.")
    def test03_get_list_of_categories(self, chuck_flows: ChuckApiFlows):    
        APIVerify.status_code(chuck_flows.get_categories(), EXPECTED_STATUS_SUCCESS_CODE)


    #@allure.title("Verify Data Integrity: API Categories vs Database Records")
    #@allure.description("Validates that the joke categories retrieved from the API match the records stored in the system database.")
    def test_04_verify_api_categories_against_db(self, chuck_flows, db_connection):
        api_list = chuck_flows.get_categories().json()
        db_list = get_db_categories(db_connection)
        APIVerify.list_equals(api_list, db_list, "API and DB categories Do Not Match")


