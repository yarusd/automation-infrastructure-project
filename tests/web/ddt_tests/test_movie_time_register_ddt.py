
import allure
import pytest
from data.web.movie_time_data import *
from extensions.web_verifications import WebVerify
from utils.common_ops import read_data_from_csv
from workflows.web.movie_time_flows import MovieFlows

REGISTER_DATA_PATH = r"data\ddt\register_data.csv"

class TestRegisterDDT:

    
    @allure.title("User Authentication DDT")
    @allure.description("Validate Registeration behavior using diverse data-driven inputs (Positive/Negative).")
    @pytest.mark.parametrize("register_data",read_data_from_csv(REGISTER_DATA_PATH))
    def test_user_register_authentication_ddt(self,movie_time_flows:MovieFlows,register_data):
        movie_time_flows.fill_register_form(register_data["full_name"], 
                                            register_data["email"],
                                            register_data["password"],
                                            register_data["confirm_password"])
        WebVerify.verify_auth_result(movie_time_flows, register_data["expected_status"])                              



        


        

        
        

