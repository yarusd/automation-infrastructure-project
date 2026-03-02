import json
from urllib import response

import allure

from conftest import request_context
from data.api.chuck_api_data import *
from extensions.api_verifications import APIVerify
from workflows.api.chuck_api_flows import ChuckApiFlows


class TestChuckAPI:

    @allure.title("Verify Random Joke Retrieval via GET Request")
    @allure.description("Verifies that the API successfully returns a random joke with a 200 OK status code")
    def test01_Verify_random_joke_retrieval_via_GET_request(self,chuck_flows:ChuckApiFlows):
        APIVerify.status_code(chuck_flows.search_for_joke(joke),EXPECTED_STATUS_SUCCESS_CODE)

    @allure.title("Verify Joke Retrieval by Specific Category")
    @allure.description("Ensures that fetching a joke from a specific category (e.g., 'career') returns a valid response and success status code.")
    def test02_get_random_joke_by_category(self,chuck_flows:ChuckApiFlows):
        APIVerify.status_code(chuck_flows.search_for_joke(career),EXPECTED_STATUS_SUCCESS_CODE)  

    @allure.title("Verify Retrieval of All Available Joke Categories")
    @allure.description("Validates that the endpoint for retrieving the full list of joke categories is functional and returns the expected success code.")
    def test03_get_list_of_categories(self, chuck_flows: ChuckApiFlows):    
        APIVerify.status_code(chuck_flows.get_categories(), EXPECTED_STATUS_SUCCESS_CODE)


    def test_04_joke_url(self,chuck_flows: ChuckApiFlows):
        response = (json.dumps(chuck_flows.search_for_joke(joke),indent=2))
        print(json.dumps(chuck_flows.search_for_joke("joke").json(), indent=2))

