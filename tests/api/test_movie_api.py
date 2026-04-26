import allure
import pytest
from extensions.api_verifications import APIVerify
from workflows.api.movie_api_flows import MovieApiFlows
from workflows.web.movie_time_flows import MovieFlows
from data.api.api_ddt.data_hub import *
from data.api.movie_api_data import *



class TestMovieAPI:


# ===================== GET REQUESTS ======================= #


    @allure.title("Verify System Up")
    @allure.description("Verify system up and diaplay movies count")
    def test01_get_system_integrity_check(self, movie_flows: MovieApiFlows):
        response = movie_flows.send_a_get_request(HEALTH_URL)
        APIVerify.status_code(response ,EXP_SUCCESS_STAT)
        APIVerify.json_contains(response.json() , EXP_HEALTH_DATA)


    @allure.title("Verify Total Movies Count")
    @allure.description("Validates that the number of movies returned by the API matches the expected count.")
    def test02_verify_movies_list_count(self, movie_flows:MovieApiFlows):
        response = movie_flows.send_a_get_request(MOVIES_URL)
        APIVerify.status_code(response, EXP_SUCCESS_STAT)

        actual_movies_count = movie_flows.get_movies_count()
        APIVerify.verify_values_equals(actual_movies_count, EXPECTED_MOVIES_COUNT)

    @allure.title("DDT: Verify Keyword Search Functionality {test_name}")
    @allure.description("DDT :Validates searching for a  keyword returns results where keyword appears in at least one field in (cast, title, genre).")
    @pytest.mark.parametrize("payload, expected_status, expected_keyword ,test_name",FILTER_SCENARIOS)
    def test03_verify_search_engine_accuracy(self, movie_flows: MovieApiFlows,payload, expected_status, expected_keyword, test_name):
        search_results = movie_flows.search_for_random_keyword(payload)
        APIVerify.status_code(search_results, expected_status)
        APIVerify.soft_verify_search_integrity(search_results.json(), expected_keyword)
        APIVerify.assert_all()


    @allure.title("DDT : Combined Search: {test_name}")
    @allure.description("DDT : Verifies that filtering by multiple criteria (e.g., Title + Genre) returns correct movies or error messages.") 
    @pytest.mark.parametrize("payload, expected_status, expected_keyword, test_name", COMBINED_FILTER_SCENARIOS)
    def test04_verify_combined_search_logic(self, movie_flows: MovieApiFlows, payload, expected_status, expected_keyword, test_name):
        search_results = movie_flows.search_for_random_keyword(payload)
        APIVerify.status_code(search_results,expected_status)
        APIVerify.soft_verify_multiple_criteria(search_results.json(), expected_keyword)
        APIVerify.assert_all()

    @allure.title("DDT : Sorting Integrity: {test_name}")
    @allure.description("DDT : Validates that the API returns movies correctly sorted by Title, Year, or Rating according to the requested sort type.")
    @pytest.mark.parametrize("payload, status, key, sort_type, test_name", SORT_SCENARIOS)
    def test05_verify_sorting_integrity(self, movie_flows: MovieApiFlows, payload, status, key, sort_type, test_name):
        sort_results = movie_flows.search_for_random_keyword(payload)
        APIVerify.status_code(sort_results, status)    
        APIVerify.soft_verify_sorting(sort_results.json(), key, sort_type)
        APIVerify.assert_all()

    @allure.title("Verify API Stability - Multiple Consecutive Requests")
    @allure.description("Sends multiple concurrent/consecutive requests to ensure server resilience.")
    def test06_verify_api_stability_under_multiple_requests(self, movie_flows:MovieApiFlows):
        requests_list = movie_flows.send_multiple_requests(GET_REQUEST_AMOUNT)
        APIVerify.soft_verify_statuses(requests_list, EXP_SUCCESS_STAT)
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
    def test08_verify_equal_movies_from_web_and_api(self, movie_flows: MovieApiFlows, web_sync_context: MovieFlows):
        api_movies_list = movie_flows.get_movies_value(TITLE_KEY)
    
        web_sync_context.navigate_to_all_movies()
        web_movies_titles = web_sync_context.get_title_list_text()
    
        APIVerify.list_equals(api_movies_list, web_movies_titles, "Values not match")
        
    @allure.title("DDT :User Order History {test_name}")
    @allure.description("Validates ID matching between URL and X-USER-ID header to prevent security breaches.")
    @pytest.mark.parametrize("userId, headerId, status,test_name", USER_ORDER_HISTORY)
    def test09_verify_user_order_history_validation(self, movie_flows: MovieApiFlows,userId, headerId, status,test_name):
        response = movie_flows.get_user_order_history(userId, headerId)
        APIVerify.status_code(response, status)


    @allure.title("Verify Movies Gallery Uniqueness (ID & Title)")
    @allure.description("This test ensures that all movies in the gallery have unique IDs and unique Titles to prevent duplicates.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test10_verify_movies_gallery_uniquness(self, movie_flows: MovieApiFlows):
        movies_list = movie_flows.send_a_get_request(MOVIES_URL)
        APIVerify.verify_uniqueness(movies_list.json(), ID_KEY)
        APIVerify.verify_uniqueness(movies_list.json(),TITLE_KEY)
        APIVerify.assert_all()

    # ================== POST REQUESTS ===================== #

    @allure.title("DDT : register Validation: {test_name}")
    @allure.description("DDT : Validating register flows with positive and negative scenarios.")
    @pytest.mark.parametrize("payload, expected_status, expected_msg,test_name", REGISTER_SCENARIOUS)
    def test11_valid_register_scenarios(self, movie_flows: MovieApiFlows,payload, expected_status, expected_msg, test_name):
        register_request = movie_flows.send_post_request(REGISTER_URL,payload)
        print(register_request.json())
        APIVerify.status_code(register_request,expected_status)
        APIVerify.json_contains(register_request.json(), expected_msg)

    @allure.title("Duplicate Registration Verification")
    @allure.description("Verify that the system blocks duplicate registration with the same email.")
    def test12_verify_no_duplicate_registration(self, movie_flows:MovieApiFlows):
        register_1 = movie_flows.send_post_request(REGISTER_URL,NEW_REGISTER)
        APIVerify.status_code(register_1,EXP_CREATED_STAT)

        register_2 = movie_flows.send_post_request(REGISTER_URL,NEW_REGISTER)
        APIVerify.status_code(register_2 , EXP_DUPLICATE_STAT)
        APIVerify.json_contains(register_2.json(),EXP_DOUBLE_REGISTER_MSG)

    @allure.title("DDT : Login Validation: {test_name}")
    @allure.description("DDT : Validating login flows with positive and negative scenarios.")
    @pytest.mark.parametrize("payload, expected_status, expected_msg,test_name", LOGIN_SCENARIOUS)
    def test13_verify_login_scenarios(self, movie_flows: MovieApiFlows,payload, expected_status, expected_msg, test_name):
        login_request = movie_flows.send_post_request(LOGIN_URL, payload)
        print(login_request.json())
        APIVerify.status_code(login_request,expected_status)
        APIVerify.json_contains(login_request.json(),expected_msg)


    @allure.title("Verify Login Success after New User Registration")
    @allure.description("Verifies that a newly registered user can successfully log in with their credentials.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test14_verify_login_with_new_register(self, movie_flows: MovieApiFlows):
        # new register
        register_res = movie_flows.send_post_request(REGISTER_URL,NEW_REGISTER)
        APIVerify.status_code(register_res, EXP_CREATED_STAT)

        login_info = {"email": NEW_REGISTER["email"] , 
                         "password": NEW_REGISTER["password"]}
        
        login_res = movie_flows.send_post_request(LOGIN_URL, login_info)
        APIVerify.status_code(login_res,EXP_SUCCESS_STAT)
        

    @allure.title("DDT - Create Movie: {test_name}")
    @allure.description("Verifies movie add with valid and invalid payloads. Validates status codes and response data integrity.")
    @pytest.mark.parametrize("payload, expected_status, expected_msg,test_name", NEW_MOVIE_SCENARIOS)
    def test15_add_movie_to_catalog_scenarios(self, movie_flows: MovieApiFlows, payload, expected_status, expected_msg,test_name):
        post_response = movie_flows.send_post_request(MOVIES_URL,payload ,USE_API_KEY)
        APIVerify.status_code(post_response, expected_status)
        APIVerify.verify_required_fields_not_empty(post_response.json(), REQUIRED_FIELDS)


    @allure.title("Create Movie: Unauthorized Access Attempt")
    @allure.description("Security test verifying the API correctly blocks requests without a valid API Key")
    @allure.severity(allure.severity_level.CRITICAL)
    def test16_post_create_movie_unauthorized(self, movie_flows: MovieApiFlows):
        post_response = movie_flows.send_post_request(MOVIES_URL,NEW_MOVIE_DATA)
        APIVerify.status_code(post_response, EXP_UNAUTHORIZED_STAT)  


    @allure.title("DDT : Payment Validation: {test_name}")
    @allure.description("DDT : Validating direct payment flows with positive and negative scenarios.")
    @pytest.mark.parametrize("payload, expected_status, expected_msg,test_name", DIRECT_PAYMENT_SCENARIOS)
    def test17_direct_payment_validations(self, movie_flows: MovieApiFlows,payload, expected_status, expected_msg, test_name):
        order_request = movie_flows.send_post_request(DIRECT_CHECKOUT_URL,payload)
        APIVerify.status_code(order_request,expected_status)
        APIVerify.json_contains(order_request.json(), expected_msg)


    @allure.title("DDT : Ticket Reservation Scenarios: {test_name}")
    @allure.description("DDT: Verifying ticket reservations with various data sets (Valid and Invalid).")
    @pytest.mark.parametrize("payload, expected_status, expected_msg, test_name", BOOKING_SCENARIOS)
    def test18_reserve_tickets_validation_scenarios(self, movie_flows: MovieApiFlows, payload, expected_status, expected_msg, test_name):
        order_request = movie_flows.send_post_request(ORDER_URL, payload)
        APIVerify.status_code(order_request, expected_status)
        APIVerify.json_contains(order_request.json(), expected_msg)


    @allure.title("DDT : Payment for Reserved Order: {test_name}")
    @allure.description("DDT: Verifying the end-to-end flow of paying for a previously reserved order.")
    @pytest.mark.parametrize("payload, expected_status, expected_msg, test_name", PAY_RESERVATION)
    def test19_pay_for_reserved_order(self, movie_flows: MovieApiFlows, payload, expected_status, expected_msg, test_name):

        order_reservation = movie_flows.send_post_request(ORDER_URL, VALID_BOOKING)
        order_id = movie_flows.get_value_from_key(order_reservation, ORDER_KEY)
        payload[ORDER_KEY] = order_id
        pay_request = movie_flows.send_post_request(PAY_FOR_RESERV_URL, payload)
        
        APIVerify.status_code(pay_request, expected_status)
        APIVerify.json_contains(pay_request.json(), expected_msg)

    @allure.title("Prevent Duplicate Seat Reservations")
    @allure.description("Validates the system prevents booking the same seat for the same movie twice") 
    def test20_verify_no_duplication_in_reservations(self, movie_flows: MovieApiFlows):
        first_order = movie_flows.send_post_request(ORDER_URL, VALID_BOOKING)
        APIVerify.status_code(first_order,EXP_CREATED_STAT)

        second_order = movie_flows.send_post_request(ORDER_URL ,VALID_BOOKING)
        APIVerify.status_code(second_order,EXP_DUPLICATE_STAT)
        APIVerify.json_contains(second_order.json() , EXP_DOUBLE_BOOKING_MSG)

    #  ==================== PUT REQUESTS ===================== #

    @allure.title("DDT:  Update Movie Existing Information {test_name}")
    @allure.description("DDT : Verifies that an existing movie can be updated using a valid API Key") 
    @pytest.mark.parametrize("payload, expected_status, expected_msg,test_name",PUT_MOVIE_SCENARIOS)
    def test21_update_movie_with_authorizations(self, movie_flows: MovieApiFlows,payload, expected_status, expected_msg, test_name):
        movie_update = movie_flows.update_movie_request(PUT_MOVIE_ID, payload, USE_API_KEY)
        APIVerify.status_code(movie_update,expected_status)
        APIVerify.json_contains(movie_update.json(),expected_msg)


    @allure.title("Update Movie Without Authorization")
    @allure.description("Security verification: Ensures the system rejects movie updates when an API Key is missing..")
    @allure.severity(allure.severity_level.CRITICAL)    
    def test22_update_movie_without_authorizations(self, movie_flows: MovieApiFlows):
        movie_update = movie_flows.update_movie_request(PUT_MOVIE_ID, VALID_MOVIE)
        APIVerify.status_code(movie_update, EXP_UNAUTHORIZED_STAT)

    # ======================= PATCH REQUESTS ================== #

    @allure.title("DDT : Partial Update Movie Existing Information {test_name}")
    @allure.description("DDT: Verifies  Partial update using a valid API Key") 
    @pytest.mark.parametrize("payload, expected_status, expected_msg, test_name", PATCH_SCENARIOS)
    def test23_partial_movie_details_update(self, movie_flows: MovieApiFlows,payload, expected_status, expected_msg, test_name):

        patch_response = movie_flows.patch_movie_request(PATCH_MOVIE_ID, payload, USE_API_KEY)
        APIVerify.status_code(patch_response,expected_status)
        APIVerify.json_contains(patch_response.json(), expected_msg)


    @allure.title("Partial Update Movie Information Unauthorized")
    @allure.description("Verifies Partial update Block without API Key") 
    @allure.severity(allure.severity_level.CRITICAL)
    def test24_partial_movie_update_unauthorized(self, movie_flows : MovieApiFlows):
        patch_response = movie_flows.patch_movie_request(PATCH_MOVIE_ID, VALID_PATCH_DATA)
        APIVerify.status_code(patch_response,EXP_UNAUTHORIZED_STAT)
        APIVerify.json_contains(patch_response.json(), UNAUTHORIZED_MSG)


    # ================== DELETE REQUESTS ===================== #

    @allure.title("System Integrity: Full Database Reset Verification")
    @allure.description("Validates that the reset endpoint not only returns 200 ok and restores the database initial state of 60 movies.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test25_reset_api_db_and_verify_count(self, setup_clean_database,movie_flows: MovieApiFlows):
        reset_response = setup_clean_database
        APIVerify.status_code(reset_response, EXP_SUCCESS_STAT)

        actual_count = movie_flows.get_movies_count()
        APIVerify.verify_values_equals(actual_count, EXPECTED_MOVIES_COUNT)


    @allure.title("Security Check: Block Database Reset Without API Key")
    @allure.description("Validates that the API strictly prevents database resets without API Key.")
    @allure.severity(allure.severity_level.CRITICAL)    
    def test26_reset_api_db_unauthorized(self, movie_flows: MovieApiFlows):
        response = movie_flows.delete_request(DELETE_DATABASE)
        APIVerify.status_code(response, EXP_UNAUTHORIZED_STAT)
    

    @allure.title("DDT - Movie Validation: {test_name}")
    @allure.description("Verifies DELETE logic for various ID scenarios, including valid, missing, and invalid IDs.")
    @pytest.mark.parametrize("movie_id, expected_status, test_name",DELETE_MOVIE_SCENARIOS)
    def test_27_delete_movie_from_catalog(self, movie_flows: MovieApiFlows,movie_id, expected_status, test_name):
        response = movie_flows.delete_movie_request(movie_id,USE_API_KEY)
        APIVerify.status_code(response,expected_status)


    @allure.title("Security - Movie Delete: Unauthorized Access Attempt")
    @allure.description("Security test verifying that deleting a movie is blocked without a valid API Key.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test28_delete_movie_unauthorized(self, movie_flows: MovieApiFlows):
        response = movie_flows.delete_movie_request(DEL_MOVIE_ID)
        APIVerify.status_code(response, EXP_UNAUTHORIZED_STAT)


    @allure.title("DELETE - Verify Booked Order Deletion")
    @allure.description("E2E Flow: Create a new seat reservation and verify it can be successfully deleted using its unique Order ID.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test29_verify_booked_order_deletion(self, movie_flows: MovieApiFlows):
        # Book reservation
        book_order = movie_flows.send_post_request(ORDER_URL, VALID_BOOKING)
        order_id = movie_flows.get_value_from_key(book_order, ORDER_KEY)

        # Delete reservation
        delete_order = movie_flows.delete_booked_order(order_id)
        APIVerify.status_code(delete_order, EXP_SUCCESS_STAT)
        APIVerify.json_contains(delete_order.json(), EXP_ORDER_DEL_MSG)

    @allure.title("DELETE - Try to Delete Without Order ID")
    @allure.description("Negative test: Verifies that the system returns 404 when the Order ID is missing from the URL path.")
    def test30_verify_not_booking_without_order_id(self, movie_flows: MovieApiFlows):
        delete_booking = movie_flows.delete_booked_order("")
        APIVerify.status_code(delete_booking,EXP_NOT_FOUND_STAT)


    # ================== DATABASE TESTS ===================== #

    @allure.title("Verify Total Movie Count: API vs DB")
    @allure.description("Ensures the total number of movies in the database matches the API total count.")
    def test31_verify_total_movie_count(self, movie_flows: MovieApiFlows):
        api_movies_count = movie_flows.get_movies_count()
        db_movies_count = movie_flows.get_db_movies_count(TITLE_KEY)
        APIVerify.verify_values_equals(db_movies_count,api_movies_count)

    @allure.title("Verify Search Logic: API vs DB Cross-Check")
    @allure.description("Compares API search results count with a direct SQL WHERE query count.")
    def test32_verify_search_logic_in_db_and_api(self, movie_flows: MovieApiFlows):

        api_count = movie_flows.get_api_search_count(API_DB_SEARCH_DATA["api_params"])
        db_count = movie_flows.get_db_movies_count_by_filter(
            API_DB_SEARCH_DATA["db_column"], 
            API_DB_SEARCH_DATA["keyword"])
        APIVerify.verify_values_equals(api_count, db_count)



