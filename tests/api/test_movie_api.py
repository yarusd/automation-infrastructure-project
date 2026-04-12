import allure
import pytest
from extensions.api_verifications import APIVerify
from workflows.api.movie_api_flows import MovieApiFlows
from workflows.web.movie_time_flows import MovieFlows
from data.api.api_ddt.patch_scenarios_data import *
from data.api.api_ddt.combined_filter_data import *
from data.api.api_ddt.filter_scenarios_data import *
from data.api.api_ddt.pay_for_reseved_data import *
from data.api.api_ddt.resrvation_booking_data import *
from data.api.api_ddt.sort_scenarios_data import *
from data.api.api_ddt.direct_payment_data import *
from data.api.api_ddt.full_update_data import *
from data.api.movie_api_data import *



class TestMovieAPI:

    @allure.title("Verify Movie API Availability")
    @allure.description("Checks if the Movie API endpoint is up and responding with a 200 OK status.")
    @allure.severity(allure.severity_level.BLOCKER)
    def test01_verify_api_availability(self, movie_flows:MovieApiFlows):
        request = movie_flows.send_a_get_request(MOVIES_URL)
        APIVerify.status_code(request,EXPECTED_STATUS_SUCCESS_CODE)

    @allure.title("Verify Total Movies Count")
    @allure.description("Validates that the number of movies returned by the API matches the expected count.")
    def test02_verify_movies_list_count(self, movie_flows:MovieApiFlows):
        actual_movies_count = movie_flows.get_movies_count()
        APIVerify.verify_values_equals(actual_movies_count,EXPECTED_MOVIES_COUNT)
        

    @allure.title("Verify Keyword Search Functionality {test_name}")
    @allure.description("Validates searching for a  keyword returns results where keyword appears in at least one field in (cast, title, genre).")
    @pytest.mark.parametrize("payload, expected_status, expected_keyword ,test_name",FILTER_SCENARIOS)
    def test03_verify_search_engine_accuracy(self, movie_flows: MovieApiFlows,payload, expected_status, expected_keyword, test_name):
        search_results = movie_flows.search_for_random_keyword(payload)
        APIVerify.status_code(search_results, expected_status)
        APIVerify.soft_verify_search_integrity(search_results.json(), expected_keyword)
        APIVerify.assert_all()

    @allure.title("Combined Search: {test_name}")
    @allure.description("Verifies that filtering by multiple criteria (e.g., Title + Genre) returns correct movies or error messages.") 
    @pytest.mark.parametrize("payload, expected_status, expected_keyword, test_name", COMBINED_FILTER_SCENARIOS)
    def test04_combined_search_logic(self, movie_flows: MovieApiFlows, payload, expected_status, expected_keyword, test_name):
        search_results = movie_flows.search_for_random_keyword(payload)
        APIVerify.status_code(search_results,expected_status)
        APIVerify.soft_verify_multiple_criteria(search_results.json(), expected_keyword)
        APIVerify.assert_all()

    @allure.title("Sorting Integrity: {test_name}")
    @allure.description("Validates that the API returns movies correctly sorted by Title, Year, or Rating according to the requested sort type.")
    @pytest.mark.parametrize("payload, status, key, sort_type, test_name", SORT_SCENARIOS)
    def test05_sorting_integrity(self, movie_flows, payload, status, key, sort_type, test_name):
        sort_results = movie_flows.search_for_random_keyword(payload)
        APIVerify.status_code(sort_results, status)    
        APIVerify.verify_sorting(sort_results.json(), key, sort_type)
        APIVerify.assert_all()

    @allure.title("Verify API Stability - Multiple Consecutive Requests")
    @allure.description("Sends multiple concurrent/consecutive requests to ensure server resilience.")
    def test06_verify_api_stability_under_multiple_requests(self, movie_flows:MovieApiFlows):
        requests_list = movie_flows.send_multiple_requests(GET_REQUEST_AMOUNT)
        APIVerify.soft_verify_statuses(requests_list, EXPECTED_STATUS_SUCCESS_CODE)
        APIVerify.assert_all()


    @allure.title("Verify Required Fields Are Not Null")
    @allure.description("Validates that all mandatory fields in the movie object are present and populated.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test07_verify_required_fields_not_null(self,movie_flows: MovieApiFlows):
        movies_list = movie_flows.get_full_movies_list()
        APIVerify.verify_required_fields_not_empty(movies_list, REQUIRED_FIELDS)
    

    @allure.title("Data Integrity: API vs Web Movie Titles Synchronization")
    @allure.description("Validates the list of movie titles in Backend API matches the Web UI.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test08_verify_equal_movies_from_web_and_api(self,movie_flows: MovieApiFlows, movie_time_flows:MovieFlows):

        api_movies_list = movie_flows.get_movies_value(TITLE_KEY)
        movie_time_flows.navigate_to_all_movies()
        web_movies_titles = movie_time_flows.get_title_list_text()
        APIVerify.list_equals(api_movies_list, web_movies_titles, "Values not match")


    @allure.title("System Integrity: Full Database Reset Verification")
    @allure.description("Validates that the reset endpoint not only returns 200 ok and restores the database initial state of 60 movies.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test09_reset_api_db_and_verify_count(self, setup_clean_database,movie_flows: MovieApiFlows):
        reset_response = setup_clean_database
        APIVerify.status_code(reset_response, EXPECTED_STATUS_SUCCESS_CODE)

        actual_count = movie_flows.get_movies_count()
        APIVerify.verify_values_equals(actual_count, EXPECTED_MOVIES_COUNT)


    @allure.title("Security Check: Block Database Reset Without API Key")
    @allure.description("Validates that the API strictly prevents database resets without API Key.")
    @allure.severity(allure.severity_level.CRITICAL)    
    def test10_reset_api_db_unauthorized(self, movie_flows: MovieApiFlows):
        response = movie_flows.delete_request(DELETE_DATABASE)
        APIVerify.status_code(response, EXPECTED_UNAUTHORIZED_STATUS_CODE)


    @allure.title("DDT Update Movie Existing Information {test_name}")
    @allure.description("Data-Driven Test: Verifies that an existing movie can be updated using a valid API Key") 
    @pytest.mark.parametrize("payload, expected_status, expected_msg,test_name",PUT_MOVIE_SCENARIOS)
    def test11_update_movie_with_authorizations(self, movie_flows: MovieApiFlows,payload, expected_status, expected_msg, test_name):
        movie_update = movie_flows.update_movie_request(PUT_MOVIE_ID, payload, USE_API_KEY)
        APIVerify.status_code(movie_update,expected_status)
        APIVerify.json_contains(movie_update.json(),expected_msg)


    @allure.title("Update Movie Without Authorization")
    @allure.description("Security verification: Ensures the system rejects movie updates when an API Key is missing..")
    @allure.severity(allure.severity_level.CRITICAL)    
    def test12_update_movie_without_authorizations(self, movie_flows: MovieApiFlows):
        movie_update = movie_flows.update_movie_request(PUT_MOVIE_ID, VALID_MOVIE)
        APIVerify.status_code(movie_update, EXPECTED_UNAUTHORIZED_STATUS_CODE)


    @allure.title("DDT Partial Update Movie Existing Information {test_name}")
    @allure.description("Data-Driven Test: Verifies  Partial update using a valid API Key") 
    @pytest.mark.parametrize("payload, expected_status, expected_msg, test_name", PATCH_SCENARIOS)
    def test13_partial_movie_details_update(self, movie_flows: MovieApiFlows,payload, expected_status, expected_msg, test_name):

        patch_response = movie_flows.patch_movie_request(PATCH_MOVIE_ID, payload, USE_API_KEY)
        APIVerify.status_code(patch_response,expected_status)
        APIVerify.json_contains(patch_response.json(), expected_msg)


    @allure.title("Partial Update Movie Information Unauthorized")
    @allure.description("Verifies Partial update Block without API Key") 
    @allure.severity(allure.severity_level.CRITICAL)
    def test14_partial_movie_update_unauthorized(self, movie_flows : MovieApiFlows):
        patch_response = movie_flows.patch_movie_request(PATCH_MOVIE_ID, VALID_PATCH_DATA)
        APIVerify.status_code(patch_response,EXPECTED_UNAUTHORIZED_STATUS_CODE)
        APIVerify.json_contains(patch_response.json(), UNAUTHORIZED_MSG)

    @allure.title("Payment Validation: {test_name}")
    @allure.description("Data-Driven Test: Validating direct payment flows with positive and negative scenarios.")
    @pytest.mark.parametrize("payload, expected_status, expected_msg,test_name", DIRECT_PAYMENT_SCENARIOS)
    def test15_direct_payment_validations(self, movie_flows: MovieApiFlows,payload, expected_status, expected_msg, test_name):
        order_request = movie_flows.send_post_request(DIRECT_CHECKOUT_URL,payload)
        APIVerify.status_code(order_request,expected_status)
        APIVerify.json_contains(order_request.json(), expected_msg)


    @allure.title("Ticket Reservation Scenarios: {test_name}")
    @allure.description("DDT: Verifying ticket reservations with various data sets (Valid and Invalid).")
    @pytest.mark.parametrize("payload, expected_status, expected_msg, test_name", BOOKING_SCENARIOS)
    def test16_reserve_tickets_validation_scenarios(self, movie_flows: MovieApiFlows, payload, expected_status, expected_msg, test_name):
        order_request = movie_flows.send_post_request(RESERV_URL, payload)
        APIVerify.status_code(order_request, expected_status)
        APIVerify.json_contains(order_request.json(), expected_msg)


    @allure.title("Payment for Reserved Order: {test_name}")
    @allure.description("DDT: Verifying the end-to-end flow of paying for a previously reserved order.")
    @pytest.mark.parametrize("payload, expected_status, expected_msg, test_name", PAY_RESERVATION)
    def test17_pay_for_reserved_order(self, movie_flows: MovieApiFlows, payload, expected_status, expected_msg, test_name):
        order_reservation = movie_flows.send_post_request(RESERV_URL, VALID_BOOKING)
        order_id = movie_flows.get_value_from_key(order_reservation, ORDER_KEY)
        
        payload[ORDER_KEY] = order_id
        pay_request = movie_flows.send_post_request(PAY_FOR_RESERV_URL, payload)
        
        APIVerify.status_code(pay_request, expected_status)
        APIVerify.json_contains(pay_request.json(), expected_msg)

    
