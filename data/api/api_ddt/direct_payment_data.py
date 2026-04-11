
VALID_PAYMENT = {
    "userId": 1, 
    "movieId": 25, 
    "ticketCount": 1, 
    "seats": ["A1"],
    "cardHolder": "Neomi Levi", 
    "cardNumber": "4580123456789012",
    "expiry": "12/28", 
    "cvv": "123", 
    "date": "01/12/2026", 
    "time": "19:00"
}

# TEST SCENARIOS

DIRECT_PAYMENT_SCENARIOS = [
    # --- POSITIVE TESTS ---
    (VALID_PAYMENT, 201, {'message': 'Payment successful!'}, "T1 - Valid Single Ticket"),
    
    ({**VALID_PAYMENT, "ticketCount": 8, "seats": ["A1","A2","A3","A4","A5","A6","A7","A8"]}, 
     201, {'message': 'Payment successful!'}, "T2 - Valid Max Tickets"),

    # --- NEGATIVE TESTS: userId ---
    ({**VALID_PAYMENT, "userId": 0, "ticketCount": 4, "seats": ["A1","B2","C3","E4"]}, 404, {'error': 'Not Found'}, "T4 - UserId 0"),
    ({**VALID_PAYMENT, "userId": "hello"}, 400, {'error': 'Bad Request'}, "T5 - UserId String"),
    ({**VALID_PAYMENT, "userId": ""}, 400, {'error': 'Bad Request'}, "T6 - Empty UserId"),

    # --- NEGATIVE TESTS: movieId ---
    ({**VALID_PAYMENT, "movieId": 0}, 404, {'error': 'Not Found'}, "T7 - MovieId 0"),

    # --- NEGATIVE TESTS: ticketCount ---
    ({**VALID_PAYMENT, "ticketCount": 0}, 400, {'error': 'Bad Request'}, "T8 - Zero Tickets"),
    ({**VALID_PAYMENT, "ticketCount": 9}, 400, {'error': 'Bad Request'}, "T9 - Exceed Max Tickets"),
    ({**VALID_PAYMENT, "ticketCount": "hfh"}, 400, {'error': 'Bad Request'}, "T10 - Invalid Ticket Count Type"),

    # --- NEGATIVE TESTS: seats ---
    ({**VALID_PAYMENT, "seats": []}, 400, {'error': 'Bad Request'}, "T11 - Empty Seats Array"),
    ({**VALID_PAYMENT, "seats": ["F1"]}, 400, {'error': 'Bad Request'}, "T12 - Invalid Seat Pattern (F1)"),
    ({**VALID_PAYMENT, "seats": ["1"]}, 400, {'error': 'Bad Request'}, "T13 - Invalid Seat Pattern (1)"),
    ({**VALID_PAYMENT, "ticketCount": 2, "seats": ["A1","F2"]}, 400, {'error': 'Bad Request'}, "T14 - One Valid One Invalid Seat"),
    ({**VALID_PAYMENT, "ticketCount": 2, "seats": ["A1","A1"]}, 409, {'message': 'Duplicate seats in request.'}, "T15 - Duplicate Seats"),
    ({**VALID_PAYMENT, "ticketCount": 2, "seats": ["A1"]}, 400, {'error': 'Data Mismatch'}, "T16 - Data Mismatch (Count vs Array)"),

    # --- NEGATIVE TESTS: cardHolder ---
    ({**VALID_PAYMENT, "cardHolder": "@#!"}, 400, {'error': 'Bad Request'}, "T17 - Special Characters in Name"),
    ({**VALID_PAYMENT, "cardHolder": 0}, 400, {'error': 'Bad Request'}, "T18 - Numbers in Name"),
    ({**VALID_PAYMENT, "cardHolder": "    "}, 400, {'error': 'Bad Request'}, "T19 - Only Spaces in Name"),
    ({**VALID_PAYMENT, "cardHolder": "Ne"}, 400, {'error': 'Bad Request'}, "T20 - Name Too Short"),
    ({**VALID_PAYMENT, "cardHolder": "Neomi Levijsdfdlcvnewkjlcsdirjtrfdkscjnweirenvck ejfcewoifclswenrjec jewcfjmekwl"}, 400, {'error': 'Bad Request'}, "T21 - Name Too Long"),

    # --- NEGATIVE TESTS: cardNumber ---
    ({**VALID_PAYMENT, "cardNumber": "145"}, 400, {'error': 'Bad Request'}, "T22 - Card too short"),
    ({**VALID_PAYMENT, "cardNumber": "452584185051564461354"}, 400, {'error': 'Bad Request'}, "T23 - Card too long"),
    ({"userId": 1, "movieId": 25, "ticketCount": 1, "seats": ["A1"],
    "cardHolder": "Neomi Levi", "expiry": "12/28", "cvv": "123", 
    "date": "01/12/2026", "time": "19:00"}, 400, {'error': 'Bad Request'}, "T24 - Missing cardNumber Field"),
    ({**VALID_PAYMENT, "cardNumber": "0000 0000 0000 0000"}, 400, {'error': 'Bad Request'}, "T25 - Card number with spaces"),

    # --- NEGATIVE TESTS: expiry ---
    ({**VALID_PAYMENT, "expiry": "12/22"}, 402, {'error': 'Payment Required'}, "T26 - Expired Card"),
    ({**VALID_PAYMENT, "expiry": "12/50"}, 402, {'error': 'Payment Required'}, "T27 - Expiry Too Far in Future"),
    ({**VALID_PAYMENT, "expiry": "13/28"}, 400, {'error': 'Bad Request'}, "T28 - Invalid Month in Expiry"),

    # --- NEGATIVE TESTS: cvv ---
    ({**VALID_PAYMENT, "cvv": "1234", "date": "01/05/2026"}, 400, {'error': 'Bad Request'}, "T29 - CVV Too Long"),
    ({**VALID_PAYMENT, "cvv": "12"}, 400, {'error': 'Bad Request'}, "T30 - CVV Too Short"),

    # --- NEGATIVE TESTS: date & time ---
    ({**VALID_PAYMENT, "date": "33/12/2026"}, 400, {'error': 'Bad Request'}, "T31 - Invalid Date (Day 33)"),
    ({**VALID_PAYMENT, "date": "09-04-2026"}, 400, {'error': 'Bad Request'}, "T32 - Invalid Date Format"),
    ({**VALID_PAYMENT, "time": "25:00"}, 400, {'error': 'Bad Request'}, "T33 - Invalid Time (25 Hours)"),
    ({**VALID_PAYMENT, "time": "0:30"}, 400, {'error': 'Bad Request'}, "T34 - Invalid Time Format (Missing Leading Zero)")
]