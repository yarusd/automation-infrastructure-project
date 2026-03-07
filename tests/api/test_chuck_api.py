import json
import sqlite3
import allure
#database_path = "tests/api/joke_categories.db"
#my_db = sqlite3.connect(database_path)
from data.api.chuck_api_data import *
from extensions.api_verifications import APIVerify
from extensions.web_verifications import WebVerify
from workflows.api.chuck_api_flows import ChuckApiFlows
from utils.common_ops import get_db_categories

from workflows.web.chuck_web_flows import ChuckWebFlows


class TestChuckAPI:

    @allure.title("Verify Random Joke Retrieval via GET Request")
    @allure.description("Verifies that the API successfully returns a random joke with a 200 OK status code")
    def test01_Verify_random_joke_retrieval_via_GET_request(self,chuck_flows:ChuckApiFlows):
        APIVerify.status_code(chuck_flows.search_for_joke(JOKE),EXPECTED_STATUS_SUCCESS_CODE)

    @allure.title("Verify Joke Retrieval by Specific Category")
    @allure.description("Ensures that fetching a joke from a specific category (e.g., 'career') returns a valid response and success status code.")
    def test02_get_random_joke_by_category(self,chuck_flows:ChuckApiFlows):
        APIVerify.status_code(chuck_flows.search_for_joke(CAREER),EXPECTED_STATUS_SUCCESS_CODE)  

    @allure.title("Verify Retrieval of All Available Joke Categories")
    @allure.description("Validates that the endpoint for retrieving the full list of joke categories is functional and returns the expected success code.")
    def test03_get_list_of_categories(self, chuck_flows: ChuckApiFlows):    
        APIVerify.status_code(chuck_flows.get_categories(), EXPECTED_STATUS_SUCCESS_CODE)


    @allure.title("Verify Data Integrity: API Categories vs Database Records")
    @allure.description("Validates that the joke categories retrieved from the API match the records stored in the system database.")
    def test_04_verify_api_categories_against_db(self, chuck_flows, db_connection):
        api_list = chuck_flows.get_categories().json()
        db_list = get_db_categories(db_connection)
        APIVerify.list_equals(api_list, db_list, "API and DB categories Do Not Match")

    @allure.title("Verify Joke Search Returns 200")
    @allure.description("Sends a search request for a joke and verifies that the API returns a 200 status code.")
    def test01_verify_joke_search(self,chuck_flows:ChuckApiFlows):
        APIVerify.status_code( chuck_flows.search_for_joke(SEARCH_VALUE),EXPECTED_STATUS_SUCCESS_CODE)


    @allure.title("Verify Joke Value is Unique")
    @allure.description("Fetches two random jokes and verifies that their text values are unique.")
    def test02_verify_joke_id_is_uniqe(self, chuck_flows:ChuckApiFlows):
        first_id = chuck_flows.get_joke_value(ID)
        second_id = chuck_flows.get_joke_value(ID)
        APIVerify.soft_assert(first_id != second_id,f" {first_id} == {second_id}")
        APIVerify.assert_all()        

    @allure.title("Verify Joke ID is Unique")
    @allure.description("Fetches two random jokes and verifies that IDs are unique.")    
    def test03_verify_joke_value_is_uniqe(self, chuck_flows:ChuckApiFlows):
        value_1 = chuck_flows.get_joke_value(VALUE)
        value_2 = chuck_flows.get_joke_value(VALUE)
        APIVerify.soft_assert(value_1 != value_2,f"{value_1} == {value_2}")
        APIVerify.assert_all()        

    @allure.title("Validate First Keyword Has More Jokes Than Second - API")
    @allure.description("Asserts that the first keyword total joke count is greater than the second keyword.")
    def test_04_verify_who_has_more_jokes(self,chuck_flows:ChuckApiFlows):
        keyword_1_total = chuck_flows.get_joke_keyword_search_amount(SEARCH_KEYWORD_1)
        keyword_2_total = chuck_flows.get_joke_keyword_search_amount(SEARCH_KEYWORD_2)
        APIVerify.compare_values(keyword_1_total,keyword_2_total)

    @allure.title("Verify Random Joke Matches Web Joke")
    @allure.description("Verifies that a random joke from API matches the joke displayed on the web page.")
    def test05_verify_equal_joke_from_web_and_api(self,chuck_flows:ChuckApiFlows, chuck_web_flows:ChuckWebFlows):
        joke_data = chuck_flows.get_full_random_joke()
        api_joke_value = joke_data[VALUE]
        api_url = joke_data[URL]

        chuck_web_flows.navigate_to_web(api_url)
        web_joke_value = chuck_web_flows.get_web_joke_value()
        WebVerify.strings_are_equal(api_joke_value, web_joke_value, "Values not match")

  
    @allure.title("Verify Required Fields Are Not Null")
    @allure.description("Ensures that all required fields in a random joke response exist and are not null or empty.")
    def test06_Verify_required_fields_not_null(self,chuck_flows: ChuckApiFlows):
        joke_body = chuck_flows.get_full_random_joke()
        APIVerify.verify_required_fields_not_null(joke_body, REQUIRED_FIELDS)

    @allure.title("Send Multiple Random Jokes and Verify Status 200")
    @allure.description("Sends multiple random joke requests via API and verifies that each response returns status code 200 using soft assertions.")
    def test07_Verify_sending_multiply_requests_status_ok(self,chuck_flows: ChuckApiFlows):
        APIVerify.verify_responses_status_ok(chuck_flows.send_multiple_jokes(GET_REQUEST_COUNT), EXPECTED_STATUS_SUCCESS_CODE)
        APIVerify.assert_all()        


      
        
        
      