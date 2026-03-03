import json
import allure
from playwright.sync_api import APIRequestContext, APIResponse
from data.api.chuck_api_data import *
from extensions.api_actions import APIActions

class ChuckApiFlows:

    def __init__(self,request_context:APIRequestContext):
        self.api = APIActions(request_context)

    @allure.step("Search for joke with keyword")
    def search_for_joke(self,query:str)->APIResponse:
        params = {"query":query}
        return self.api.get(FREE_SEARCH_RESOURCE,params)
    
    @allure.step("Get a random joke")
    def get_a_joke(self)->APIResponse:
        return self.api.get(RANDOM_RESOURCE)
    
    @allure.step("Get full random joke JSON")
    def get_full_random_joke(self) -> APIResponse:
        response = self.api.get(RANDOM_RESOURCE)
        return response.json()

    @allure.step("Get joke field part from a random joke") 
    def get_joke_value(self, value: str) -> APIResponse:
        joke = self.get_a_joke()
        joke_value = joke.json()[value]
        return joke_value
    
    @allure.step("Get total number of jokes for keyword")
    def get_joke_keyword_search_amount(self,keyword:str) -> int:
        keyword_joke = self.search_for_joke(keyword)
        return keyword_joke.json()["total"]
    

    @allure.step("Send multiply get a joke request")
    def send_multiple_jokes(self,end:int) ->list:
        responses = []
        for i in range(end):
            response = self.get_a_joke()
            responses.append(response)
        return responses
                
   
    
 




  
       

    

