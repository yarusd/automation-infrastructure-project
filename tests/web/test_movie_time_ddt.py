



import allure
import pytest

from data.web.movie_time_data import *
from extensions.ui_actions import UIActions
from extensions.web_verifications import WebVerify
from utils.common_ops import read_data_from_csv
from workflows.web.movie_time_flows import MovieFlows


LOGIN_DATA_PATH = r"data\ddt\login_data.csv"

class TestSauceDDT:

    
    #@allure.title("User Authentication DDT")
    #@allure.description("Validate login behavior using diverse data-driven inputs (Positive/Negative).")
    @pytest.mark.parametrize("Login_data",read_data_from_csv(LOGIN_DATA_PATH))
    def test_user_login_authentication_ddt(self,movie_time_flows:MovieFlows,Login_data):
        movie_time_flows.fill_registration_form_valid_input(Login_data["username"], Login_data["password"],Login_data["expected_status"])

        


        

        
        

