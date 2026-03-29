import allure
import pytest
from data.api.movie_api_data import *
from extensions.api_verifications import APIVerify
from workflows.api.movie_api_flows import MovieApiFlows
from workflows.web.movie_time_flows import MovieFlows




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
        

    @allure.title("Verify Random Keyword Search Functionality")
    @allure.description("Validates searching for a random keyword returns results where keyword appears in at least one field.")
    def test03_verify_free_search_accuracy(self, movie_flows:MovieApiFlows):
        search_results = movie_flows.search_for_random_keyword(RANDOM_KEYWORD)
        APIVerify.soft_verify_keyword_anywhere_in_results(search_results, RANDOM_KEYWORD)
        APIVerify.assert_all()

    @allure.title("Verify Specific Metadata Filtering")
    @allure.description("Checks if movies returned by a specific search (e.g., Genre or Year) as requested criteria.")
    def test04_verify_filtered_search_results(self, movie_flows: MovieApiFlows):
        search_results = movie_flows.search_for_specific_results(DICT_KEYWORD)
        APIVerify.verify_all_movies_match_criteria(search_results,DICT_KEYWORD)
        APIVerify.assert_all()


    @allure.title("Verify API Stability - Multiple Consecutive Requests")
    @allure.description("Sending multiple of requests to ensure the server remains stable and returns successful status codes.")
    def test05_verify_api_stability_under_multiple_requests(self, movie_flows:MovieApiFlows):
        requests_list = movie_flows.send_multiple_requests(GET_REQUEST_AMOUNT)
        APIVerify.soft_verify_statuses(requests_list, EXPECTED_STATUS_SUCCESS_CODE)
        APIVerify.assert_all()


    @allure.title("Verify Required Fields Are Not Null")
    @allure.description("Ensures that all required fields in a movies response exist and are not null or empty.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test06_Verify_required_fields_not_null(self,movie_flows: MovieApiFlows):
        movies_list = movie_flows.get_full_movies_list()
        APIVerify.verify_required_fields_not_empty(movies_list, REQUIRED_FIELDS)
    
    @allure.title("Data Integrity: API vs Web Movie Titles Synchronization")
    @allure.description("Validates the list of movie titles in Backend API matches the Web UI.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test07_verify_equal_movies_from_web_and_api(self,movie_flows: MovieApiFlows, movie_time_flows:MovieFlows):
        api_movies_list = movie_flows.get_movies_value(TITLE_KEY)

        movie_time_flows.navigate_to_all_movies()
        web_movies_titles = movie_time_flows.get_title_list_text()
        APIVerify.list_equals(api_movies_list, web_movies_titles, "Values not match")


    @allure.title("System Integrity: Full Database Reset Verification")
    @allure.description("Validates that the reset endpoint not only returns 200 ok and restores the database initial state of 60 movies.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test08_reset_api_db_and_verify_count(self, setup_clean_database,movie_flows: MovieApiFlows):
        reset_response = setup_clean_database
        APIVerify.status_code(reset_response, EXPECTED_STATUS_SUCCESS_CODE)

        actual_count = movie_flows.get_movies_count()
        APIVerify.verify_values_equals(actual_count, EXPECTED_MOVIES_COUNT)


    @allure.title("Security Check: Block Database Reset Without API Key")
    @allure.description("Validates that the API strictly prevents database resets without API Key.")
    @allure.severity(allure.severity_level.CRITICAL)    
    def test09_reset_api_db_unauthorized(self, movie_flows: MovieApiFlows):
        response = movie_flows.delete_request(DELETE_DATABASE)
        APIVerify.status_code(response, EXPECTED_UNAUTORIZED_STATUS_CODE)

    @allure.title("Update Movie Existing Information")
    @allure.description("Verifies that an existing movie can be updated using a valid API Key") 
    @allure.severity(allure.severity_level.CRITICAL)    
    def test10__update_movie_with_authorizations(self, movie_flows: MovieApiFlows):
        movie_update = movie_flows.update_movie_request(PUT_MOVIE_ID, PUT_MOVIE_DATA, USE_API_KEY)
        APIVerify.json_contains(movie_update.json(),PUT_MOVIE_SUCCESS_MSG)


    @allure.title("Update Movie Without Authorization")
    @allure.description("Security check to ensure the server rejects update requests when an API Key is missing.")
    def test11_update_movie_without_authorizations(self, movie_flows: MovieApiFlows):
        movie_update = movie_flows.update_movie_request(PUT_MOVIE_ID, PUT_MOVIE_DATA)
        APIVerify.status_code(movie_update, EXPECTED_UNAUTORIZED_STATUS_CODE)


    @allure.title("Book Tickets Scenarios : {status_txt}")
    @allure.description("DDT: Verifying ticket booking with various data sets (Valid and Invalid).")
    @pytest.mark.parametrize("payload, expected_status,expected_msg,status_txt", BOOKING_SCENARIOS)
    def test12_book_tickets_validation_scenarios(self, movie_flows: MovieApiFlows,payload, expected_status,expected_msg,status_txt):
        order_request = movie_flows.send_post_request(ORDERS_URL,payload)
        APIVerify.status_code(order_request,expected_status)
        APIVerify.json_contains(order_request.json(), expected_msg)

