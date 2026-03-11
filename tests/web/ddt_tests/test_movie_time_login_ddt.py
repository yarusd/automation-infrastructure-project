
import allure
import pytest
from data.web.movie_time_data import *
from extensions.web_verifications import WebVerify
from utils.common_ops import read_data_from_csv
from workflows.web.movie_time_flows import MovieFlows

LOGIN_DATA_PATH = r"data\ddt\login_data.csv"

class TestLogineDDT:

    
    @allure.title("User Authentication DDT")
    @allure.description("Validate login behavior using diverse data-driven inputs (Positive/Negative).")
    @pytest.mark.parametrize("login_data",read_data_from_csv(LOGIN_DATA_PATH))
    def test_user_login_authentication_ddt(self,movie_time_flows:MovieFlows,login_data):
        movie_time_flows.sign_in(login_data["username"], login_data["password"])
        WebVerify.verify_log_in(movie_time_flows.page, movie_time_flows.login ,login_data["expected_status"])                 
                              



        


        

        
        

