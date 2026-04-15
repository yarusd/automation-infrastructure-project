
MOVIE_API_URL ="https://movie-time-api.onrender.com/api/"
USE_API_KEY =True

# EXPECTED STATUS
EXPECTED_SUCCESS_STATUS_CODE = 200
EXPECTED_CREATED_STATUS_CODE = 201
EXPECTED_BAD_REQUEST_STATUS = 400
EXPECTED_UNAUTHORIZED_STATUS_CODE = 401
EXPECTED_FORBIDDEN_STATUS = 403
EXPECTED_NOT_FOUND_STATUS = 404

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






