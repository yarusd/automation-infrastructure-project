import json
import allure
from playwright.sync_api import APIRequestContext, APIResponse
from data.api.movie_api_data import *
from extensions.api_actions import APIActions
import os
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv('API_KEY')

class MovieApiFlows:

    def __init__(self,request_context:APIRequestContext):
        self.api = APIActions(request_context)


    @allure.step("Send get request")
    def send_a_get_request(self,url:str)-> APIResponse:
        return self.api.get(url)

    @allure.step("Send post request to create movie")
    def send_post_request(self, url: str, payload: dict, use_api_key: bool = False) -> APIResponse:
        headers = {}   
        if use_api_key:
            headers = {"x-api-key": API_KEY}
        return self.api.post(url, payload=payload, headers=headers)
    
    @allure.step("Send put request")
    def update_movie_request(self, movie_id:int, payload: dict, use_api_key: bool = False) -> APIResponse:
        url = f"{MOVIES_URL}/{movie_id}"
        headers = {}   
        if use_api_key:
            headers = {"x-api-key": API_KEY}   
        return self.api.put(url,payload=payload, headers=headers)
 

    @allure.step("Send DELETE request") 
    def delete_request(self, url: str, use_api_key: bool = False) -> APIResponse:
        headers = {}   
        if use_api_key:
            headers = {"x-api-key": API_KEY}   
        return self.api.delete(url, headers=headers)
    


    @allure.step("Get full movie list")
    def get_full_movies_list(self) -> APIResponse:
        response = self.api.get(MOVIES_URL)
        return response.json()
    
    def get_movies_count(self) -> int:
        movies_count = APIActions.count(self.get_full_movies_list())
        return movies_count
    
    @allure.step("Free search with random keyword")
    def search_for_random_keyword(self,query:str) -> APIResponse:
        params = {"q":query}
        response = self.api.get(MOVIES_URL,params)
        search_response = response.json()
        return search_response
    
    @allure.step("Search for specific results")
    def search_for_specific_results(self,query:dict) -> APIResponse:
        response = self.api.get(MOVIES_URL,params=query)
        search_response = response.json()
        return search_response
    

    @allure.step("Send multiple get a joke request")
    def send_multiple_requests(self,amount:int) -> list:
        responses = []
        for i in range(amount):
            response = self.send_a_get_request(MOVIES_URL)
            responses.append(response)
        return responses


    @allure.step("Get movie field part from movie list") 
    def get_movies_value(self, value: str) -> APIResponse:
        values_list = []
        movies = self.get_full_movies_list()
        for _ in movies:
            new_value = _[value]
            values_list.append(new_value)
        return values_list
    
    # @allure.step("Update movie info")
    # def update_movie_info(self,id:str) -> APIResponse:
    #     params = {"q":id}
    #     response = self.api.get(MOVIES_URL,params)
    #     update_ = response.json()
    #     return search_response
    
    

