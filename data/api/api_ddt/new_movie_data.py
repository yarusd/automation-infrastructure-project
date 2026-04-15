
import pytest


VALID_MOVIE = {
    "title": "New movie", 
    "genre": "Action",
    "duration": 155, 
    "year": 2025, 
    "badge": "EXTENDED RUN"}

NEW_MOVIE_SCENARIOS = [
    # --- valid ---
    (VALID_MOVIE, 201, {"message": "Movie added successfully"}, "1 - valid update"),

    # --- negative scenarios: title ---
    ({**VALID_MOVIE, "title": ""}, 400, {"message": "empty"}, "2 - empty title"),
    ({**VALID_MOVIE, "title": 22}, 400, {"message": "must be a string"}, "3 - numbers in title"),
    ({**VALID_MOVIE, "title": "A"*500}, 400, {"message": "length"}, "4 - too long"),
    pytest.param({**VALID_MOVIE, "title": "!@#$%^&*"}, 400, {"message": "title"}, "5 - invalid creds in title field",
    marks=pytest.mark.xfail(reason="Bug: Title special characters validation missing")),

    # --- negative scenarios: genre ---
    ({**VALID_MOVIE, "genre": ""}, 400, {"message": "must be one of"}, "6 - empty genre"),
    ({**VALID_MOVIE, "genre": "LOVELY"}, 400, {"message": "must be one of"}, "7 - nonexsist genre"),

    # --- negative scenarios: duration ---
    ({**VALID_MOVIE, "duration": 0}, 400, {"message": "must be a positive number"}, "8 - zero duration"),
    ({**VALID_MOVIE, "duration": -10}, 400, {"message": "must be a positive number"}, "9 - negative duration"),

    # --- negative scenarios: year ---
    ({**VALID_MOVIE, "year": "year"}, 400, {"message": "must be a number"}, "10 - alph year"),
    ({**VALID_MOVIE, "year": 2500}, 400, {"message": "must be less than or equal to 2030"}, "11 - far future year"),
    pytest.param({**VALID_MOVIE, "year": 1900}, 400, {"message": "year"}, "12 - using ancient year",
    marks=pytest.mark.xfail(reason="Bug: Minimum year validation missing")),
    # --- negative scenarios: badge ---
    ({**VALID_MOVIE, "badge": "badge"}, 400, {"message": "must be one of"}, "13 - nonexsiste badge"),
    ({**VALID_MOVIE, "badge": 123}, 400, {"message": "must be one of"}, "14 - invalid numbers in badge"),
    ({**VALID_MOVIE, "badge": "EXTENDED RUN"*500}, 400, {"message": "must be one of"}, "15 - long badge"),
    
    # --- negative scenario: missing field---
    ({"title": "Gladiator II: Extended Cut", "genre": "Action","duration": 155, "year": 2025}, 
    400, {"message": "required"}, "16 - missing badge field"),

    #  --- negative scenario : duplicate exsisting movie
    ({"title": "Gladiator II", "genre": "Action",
    "duration": 148,"year": 2024, "badge": "NOW SHOWING"} , 
    409 , {"message" : "Movie already exists"}, "T17 - Add exsisting movie attempt")
]