
import pytest

VALID_BOOKING = {"userId": 1,"movieId": 25, "ticketCount": 1, "seats": ["B1"], "date": "10/10/2026", "time": "20:00"}

BOOKING_SCENARIOS = [
    # POSITIVE SCENARIOS:
    ({**VALID_BOOKING}, 201, {"status": "confirmed"}, "1 - Valid: Min Boundary (1)"),
    ({**VALID_BOOKING, "ticketCount": 8, "seats": ["B1", "B2","B3", "B4","B5", "B6","B7", "B8"]}, 201, {"status": "confirmed"}, "2 - Valid: Max Boundary (8)"),

    # NEGATIVE SCENARIONS: UserId & MoveeId
    ({**VALID_BOOKING, "userId": 999}, 401, {"error": "Unauthorized"}, "3 - User 999 Not Found"),
    ({**VALID_BOOKING, "movieId": ""}, 400, {"error": "Bad Request"}, "4 - Movie field empty"),
    ({**VALID_BOOKING, "movieId": "שלום"}, 400, {"error": "Bad Request"}, "5 - String in MovieId"),

    # NEGATIVE SCENARIOS : TICKETS COUNT & SEATS
    ({**VALID_BOOKING, "ticketCount": 0}, 400, {"error": "Bad Request"}, "6 - TicketCount Zero"),
    ({**VALID_BOOKING, "ticketCount": 9}, 400, {"error": "Bad Request"}, "7 - TicketCounty Too High "),
    ({**VALID_BOOKING, "ticketCount": "jdhhf"}, 400, {"error": "Bad Request"}, "8 - TicketCount as String"),
    ({**VALID_BOOKING, "seats": []}, 400, {'error': 'Bad Request'}, "9 - Empty Seats Array"),
    ({**VALID_BOOKING, "seats": ["F1"]}, 400, {'error': 'Bad Request'}, "10 - Invalid Seat Pattern"),
    ({**VALID_BOOKING, "seats": ["1"]}, 400, {'error': 'Bad Request'}, "11 - Invalid Seat Pattern "),

    # NEGATIVE SCENARIOS : MISMATCH TICKETS &S SEATS + DUPLICATION
    ({**VALID_BOOKING, "ticketCount": 2, "seats": ["A1","F2"]}, 400, {'error': 'Bad Request'}, "12 - One Valid One Invalid Seat"),
    ({**VALID_BOOKING, "ticketCount": 2, "seats": ["A1"]}, 400, {'error': 'Data Mismatch'}, "13 - Data Mismatch (Count vs Array)"),
    
    # bug:
    pytest.param({**VALID_BOOKING, "ticketCount": 2, "seats": ["A1", "A1"]}, 409, {'error': 'Conflict'}, "14 - Duplicate Seats",
    marks=pytest.mark.xfail(reason="API Bug: Allows duplicate seats in same order")),

    # NEGATIVE TESTS: DATE & TIME 
    ({**VALID_BOOKING, "date": "33/12/2026"}, 400, {'error': 'Bad Request'}, "15 - Invalid Day in Date"),
    ({**VALID_BOOKING, "date": "09-04-2026"}, 400, {'error': 'Bad Request'}, "16 - Invalid Date Format"),
    ({**VALID_BOOKING, "time": "0:30"}, 400, {'error': 'Bad Request'}, "17 - Missing Leading Zero "),

    # bug:
    pytest.param({**VALID_BOOKING, "time": "25:00"}, 400, {'error': 'Bad Request'}, "18 - Invalid Time Hour",
    marks=pytest.mark.xfail(reason="API Bug: No validation for 24h format"))

]


