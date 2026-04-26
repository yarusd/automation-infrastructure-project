import json
from typing import List, Tuple
import allure
from playwright.sync_api import APIRequestContext, APIResponse
from conftest import *
from data.api.movie_api_data import *
from extensions.api_actions import APIActions
import os
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv('API_KEY')

class MovieApiFlows:

    def __init__(self,request_context:APIRequestContext ,db_connection):
        self.api = APIActions(request_context)
        self.db = db_connection        # שומר אותו בתוך self

    @allure.step("Send get request")
    def send_a_get_request(self,url:str)-> APIResponse:
        return self.api.get(url)

    @allure.step("Send get request for user order history")
    def get_user_order_history(self, user_id: int,header_user_id:int , use_api_key: bool = False) -> APIResponse:
        url = f"{ORDER_URL}/{user_id}"
        headers = {
            "X-USER-ID": str(header_user_id) }
        if use_api_key:
            headers["x-api-key"] = API_KEY
        return self.api.get(url, headers=headers)
    
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
 
    @allure.step("Send PATCH request to update movie fields")
    def patch_movie_request(self, movie_id: int, payload: dict, use_api_key: bool = False) -> APIResponse:
        url = f"{MOVIES_URL}/{movie_id}"
        headers = {}
        if use_api_key:
            headers = {"x-api-key": API_KEY}
        return self.api.patch(url, payload=payload, headers=headers)


    @allure.step("Send DELETE request") 
    def delete_request(self, url: str, use_api_key: bool = False) -> APIResponse:
        headers = {}   
        if use_api_key:
            headers = {"x-api-key": API_KEY}   
        return self.api.delete(url, headers=headers)


    @allure.step("Send DELETE movie request") 
    def delete_movie_request(self, movie_id: int, use_api_key: bool = False) -> APIResponse:
        url = f"{MOVIES_URL}/{movie_id}"
        headers = {}   
        if use_api_key:
            headers = {"x-api-key": API_KEY}   
        return self.api.delete(url, headers=headers)
    
    @allure.step("Send DELETE request") 
    def delete_booked_order(self, order_id: str, use_api_key: bool = False) -> APIResponse:
        url = f"{ORDER_URL}/{order_id}"
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
    def search_for_random_keyword(self,query:dict) -> APIResponse:
        response = self.api.get(MOVIES_URL,params=query)
        return response
    
    @allure.step("Getting search results count")
    def get_api_search_count(self, params):
        response = self.search_for_random_keyword(params)
        return APIActions.count(response.json())
    

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
    
    @allure.step("Get json key value")
    def get_value_from_key(self ,response:APIResponse , key:str) -> str :
        res_data = response.json()
        value = res_data.get(key)
        print(f"key value is : {value}")
        return value    
    
    @allure.step("DB: Fetching all values from column")
    def get_db_column_values(self, column_name: str) -> List[Tuple]:        
        cursor = self.db.cursor()
        cursor.execute(f"SELECT {column_name} FROM Movies") 
        return cursor.fetchall()
    
    @allure.step("DB: Getting count for search result")
    def get_db_movies_count(self, column_name: str) -> int:
        results = self.get_db_column_values(column_name)
        return APIActions.count(results)
    
    @allure.step("DB: Filtering table by value")
    def db_filter_by(self, column_name: str, s_value: str) -> List[Tuple]:
        
        query = f"SELECT *FROM Movies WHERE {column_name} = ?"
        my_cursor = self.db.cursor()
        my_cursor.execute(query, (s_value,))
        return my_cursor.fetchall()

    @allure.step("DB: Getting count for search result")
    def get_db_movies_count_by_filter(self, column_name: str, s_value: str) -> int:
        results = self.db_filter_by(column_name, s_value)
        return APIActions.count(results)