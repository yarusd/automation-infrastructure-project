MOVIE_API_URL ="https://movie-time-api.onrender.com/api/"

USE_API_KEY =True
EXPECTED_STATUS_SUCCESS_CODE = 200
EXPECTED_CREATED_STATUS_CODE = 201
EXPECTED_BAD_REQUEST_STATUS = 400
EXPECTED_UNAUTORIZED_STATUS_CODE = 401
EXPECTED_FORBIDDEN_STATUS = 403
EXPECTED_NOT_FOUND_STATUS = 404

TITLE_KEY = "title"
MOVIES_URL = "movies"
ORDERS_URL = "orders"
RANDOM_KEYWORD = "superman"
DICT_KEYWORD ={"genre" : "action"}
GET_REQUEST_AMOUNT = 20
EXPECTED_MOVIES_COUNT = 60
REQUIRED_FIELDS = ["id", "title", "genre","duration"]
DELETE_DATABASE ="test/reset"
PUT_MOVIE_SUCCESS_MSG = {"message" :"Movie updated successfully"}
ORDER_CONFIRMED_MSG = {'status': 'confirmed'}
PUT_MOVIE_ID = 1
PUT_MOVIE_DATA = { "title": "Bolts"}

BOOKING_SCENARIOS = [
    # --- Positive Tests ---
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

