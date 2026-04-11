import pytest
MOVIE_API_URL ="https://movie-time-api.onrender.com/api/"
USE_API_KEY =True

# EXPECTED STATUS
EXPECTED_STATUS_SUCCESS_CODE = 200
EXPECTED_CREATED_STATUS_CODE = 201
EXPECTED_BAD_REQUEST_STATUS = 400
EXPECTED_UNAUTHORIZED_STATUS_CODE = 401
EXPECTED_FORBIDDEN_STATUS = 403
EXPECTED_NOT_FOUND_STATUS = 404

# URL ENDPOINTS:
TITLE_KEY = "title"
MOVIES_URL = "movies"
ORDERS_URL = "orders"
DIRECT_CHECKOUT_URL= "payments/checkout"
DELETE_DATABASE = "test/reset"

RANDOM_KEYWORD = "man"
COMBINED_SEARCH = "genre=action&genre=romance"
EXPECTED_COMBINED_RESULTS = {"genre" : "action"} or {"genre" : "romance"}
GET_REQUEST_AMOUNT = 20
EXPECTED_MOVIES_COUNT = 60
REQUIRED_FIELDS = ["id", "title", "genre","duration"]
ORDER_CONFIRMED_MSG = {'status': 'confirmed'}
PUT_MOVIE_ID = 1


COMBINED_FILTER_SCENARIOS = [
    # POSITIVE SCENARIOS:
    ({"title": "superman", "genre": "action"}, 200, "superman", "T4.1 - Title and Genre match"),
    ({"cast": "Chris Evans", "genre": "romance"}, 200, "chris", "T4.2 - Cast and Genre match"),
    ({"q": "flow", "year": "2024"}, 200, "flow", "T4.3 - Q + Year match"),
    
    # 4. Negative: Mismatch 
    ({"title": "superman", "genre": "Romance"}, 400, "No movies found", "T4.4 - No results for Romance in Superman"),
    ({"q": "flow", "year": "2025"}, 400, "No movies found", "T4.5 - No results for 2025 in Flow"),
    ({"cast": "tom cruise", "genre": "romance"}, 400, "No movies found", "T.6 - cast exists but genre mismatch"),

    # 4. Genre + Sort 
    ({"genre": "Action", "sort": "rating"}, 400, "cannot combine", "T4.7 - Genre + Sort: Forbidden"),
    ({"genre": "Action", "year": ""}, 400, "cannot be empty", "T4.8 - valid Genre + empty year"),
    ({"title": "!@#", "cast": "tom cruies"}, 400, "Invalid", "T4.9 - special chars + valid cast")

]



BOOKING_SCENARIOS = [
    ({"userId": 1, "movieId": 25, "quantity": 1}, 201, {"status": "confirmed"}, "Valid: Min Boundary (1)"),
    ({"userId": 1, "movieId": 25, "quantity": 8}, 201, {"status": "confirmed"}, "Valid: Max Boundary (8)"),
    ({"userId": 1, "movieId": 25, "quantity": 4}, 201, {"status": "confirmed"}, "Valid: Middle Range (4)"),

    ({"userId": 999, "movieId": 25, "quantity": 1}, 401, {"error": "Unauthorized"}, "Error: User Not Found"),
    ({"userId": 1, "movieId": 9999, "quantity": 1}, 404, {"error": "Not Found"}, "Error: Movie Not Found"),
    ({"userId": 0, "movieId": 25, "quantity": 1}, 401, {"error": "Unauthorized"}, "Error: User Not Found"),

    ({"userId": 1, "movieId": 25, "quantity": 0}, 400, {"error": "Bad Request"}, "Validation: Quantity Zero"),
    ({"userId": 1, "movieId": 25, "quantity": 20}, 400, {"error": "Bad Request"}, "Validation: Quantity Too High (20)"),
    ({"userId": 1, "movieId": 25, "quantity": "jdhhf"}, 400, {"error": "Bad Request"}, "Validation: Quantity as String"),
    ({"userId": 1, "movieId": "nvnv", "quantity": 1}, 400, {"error": "Bad Request"}, "Validation: MovieId as String"),
    ({"userId": "", "movieId": 25, "quantity": 1}, 400, {"error": "Bad Request"}, "Validation: Empty UserId"),
    ({"userId": 1, "movieId": "", "quantity": ""}, 400, {"error": "Bad Request"}, "Validation: Empty Movie and Quantity")
]

