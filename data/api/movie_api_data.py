
MOVIE_API_URL ="https://movie-time-api.onrender.com/api/"
USE_API_KEY =True

# EXPECTED STATUS
EXP_SUCCESS_STAT = 200
EXP_CREATED_STAT = 201
EXP_BAD_REQUEST_STAT = 400
EXP_UNAUTHORIZED_STAT = 401
EXP_FORBIDDEN_STAT = 403
EXP_NOT_FOUND_STAT = 404
EXP_DUPLICATE_STAT = 409

# URL ENDPOINTS:
MOVIES_URL = "movies"
ORDER_URL = "orders"
DIRECT_CHECKOUT_URL= "payments/checkout"
DELETE_DATABASE = "test/reset"
PAY_FOR_RESERV_URL = "payments/pay-existing"
HEALTH_URL = "health"
REGISTER_URL = "register"
LOGIN_URL = "login"


ID_KEY = "id"
TITLE_KEY = "title"
ORDER_KEY = "orderId"
GET_REQUEST_AMOUNT = 20
EXPECTED_MOVIES_COUNT = 60
REQUIRED_FIELDS = ["id", "title", "genre","duration","year","badge"]
DEL_MOVIE_ID = 5
PUT_MOVIE_ID = 1
PATCH_MOVIE_ID = 2
VALID_PATCH_DATA = { "title": "BLOCKBUSTER" }
UNAUTHORIZED_MSG = "missing x-api-key"
EXP_DOUBLE_BOOKING_MSG = {'message': 'Seats already booked.'}
ORDER_CONFIRMED_MSG = {'status': 'confirmed'}
EXP_HEALTH_DATA = { "status": "UP", "moviesCount": 60}
NEW_MOVIE_DATA = {"title": "New Movie", "genre": "Action",
                    "duration": 148,"year": 2024, "badge": "NOW SHOWING"}
EXP_ORDER_DEL_MSG = { "message": "Order cancelled successfully"}
EXP_DOUBLE_REGISTER_MSG = {'message': 'User already exists'}
NEW_REGISTER = {"name": "Liya Degel",
                "email": "liya@test.com",
                "password": "securepass123",
                "password_confirmation": "securepass123"}
LOGIN_INFO = { "email": "user1@test.com", "password": "123456"}

DB_MOVIES_TABLE = "Movies"
API_DB_SEARCH_DATA = {
    "api_params": {"genre": "Action"},
    "db_column": "genre",
    "keyword": "Action"
}




