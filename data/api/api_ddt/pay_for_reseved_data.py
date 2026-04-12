

VALID_PAY = {
  "orderId": "",
  "cardHolder": "Adam Norado",
  "cardNumber": "4580123456789012",
  "expiry": "12/28",
  "cvv": "123"
}

PAY_RESERVATION = [
    # --- POSITIVE TESTS : ---
    ({**VALID_PAY} , 200 , {"message" : "paid order"} , "T17.1 - valid pay"),


    ({**VALID_PAY, "cardHolder": "@#!"}, 400, {'error': 'Bad Request'}, "T17.2 - Special Characters in Name"),
    ({**VALID_PAY, "cardHolder": 0}, 400, {'error': 'Bad Request'}, "T17.3 - Numbers in Name"),
    ({**VALID_PAY, "cardHolder": "    "}, 400, {'error': 'Bad Request'}, "T17.4 - Only Spaces in Name"),
    ({**VALID_PAY, "cardHolder": "Ne"}, 400, {'error': 'Bad Request'}, "T17.5 - Name Too Short"),
    ({**VALID_PAY, "cardHolder": "Neomi"*50}, 400, {'error': 'Bad Request'}, "T17.6 - Name Too Long"),

    # --- NEGATIVE TESTS: cardNumber ---
    ({**VALID_PAY, "cardNumber": "145"}, 400, {'error': 'Bad Request'}, "T17.7 - Card too short"),
    ({**VALID_PAY, "cardNumber": "452584185051564461354"}, 400, {'error': 'Bad Request'}, "T17.8 - Card too long"),
    ({**VALID_PAY, "cardNumber": "0000 0000 0000 0000"}, 400, {'error': 'Bad Request'}, "T17.9 - Card number with spaces"),

    # MISSING FIELD
    ({"userId": 1, "movieId": 25, "ticketCount": 1, "seats": ["A1"],
    "cardHolder": "Neomi Levi", "expiry": "12/28", "cvv": "123", "date": "01/12/2026", "time": "19:00"},
    400, {'error': 'Bad Request'}, "T17.10 - Missing cardNumber Field"),
    
    # --- NEGATIVE TESTS: expiry ---
    ({**VALID_PAY, "expiry": "12/22"}, 402, {'error': 'Payment Required'}, "T17.11 - Expired Card"),
    ({**VALID_PAY, "expiry": "12/50"}, 402, {'error': 'Payment Required'}, "T17.12 - Expiry Too Far in Future"),
    ({**VALID_PAY, "expiry": "13/28"}, 400, {'error': 'Bad Request'}, "T17.13 - Invalid Month in Expiry"),

    # --- NEGATIVE TESTS: cvv ---
    ({**VALID_PAY, "cvv": "1234", "date": "01/05/2026"}, 400, {'error': 'Bad Request'}, "T17.14 - CVV Too Long"),
    ({**VALID_PAY, "cvv": "12"}, 400, {'error': 'Bad Request'}, "T17.15 - CVV Too Short")

]