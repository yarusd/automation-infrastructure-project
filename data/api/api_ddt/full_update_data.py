import pytest

VALID_MOVIE = {
    "title": "Gladiator II: Extended Cut", 
    "genre": "Action",
    "duration": 155, 
    "year": 2025, 
    "badge": "EXTENDED RUN"}

PUT_MOVIE_SCENARIOS = [
    # --- valid ---
    (VALID_MOVIE, 200, {"message": "Movie updated successfully"}, "T1 - valid update"),

    # --- negative scenarios: title ---
    ({**VALID_MOVIE, "title": ""}, 400, {"message": "empty"}, "T2 - empty title"),
    ({**VALID_MOVIE, "title": 22}, 400, {"message": "must be a string"}, "T3 - numbers in title"),
    ({**VALID_MOVIE, "title": "A"*500}, 400, {"message": "length"}, "T4 - too long"),
    pytest.param({**VALID_MOVIE, "title": "!@#$%^&*"}, 400, {"message": "title"}, "T5 - invalid creds in title",
    marks=pytest.mark.xfail(reason="Bug: Title special characters validation missing")),

    # --- negative scenarios: genre ---
    ({**VALID_MOVIE, "genre": ""}, 400, {"message": "must be one of"}, "T6 - empty genre"),
    ({**VALID_MOVIE, "genre": "LOVELY"}, 400, {"message": "must be one of"}, "T7 - nonexsist genre"),

    # --- negative scenarios: duration ---
    ({**VALID_MOVIE, "duration": 0}, 400, {"message": "must be a positive number"}, "T8 - zero duration"),
    ({**VALID_MOVIE, "duration": -10}, 400, {"message": "must be a positive number"}, "T9 - negative duration"),

    # --- negative scenarios: year ---
    ({**VALID_MOVIE, "year": "year"}, 400, {"message": "must be a number"}, "T10 - alph year"),
    ({**VALID_MOVIE, "year": 2500}, 400, {"message": "must be less than or equal to 2030"}, "T11 - far future year"),
    pytest.param({**VALID_MOVIE, "year": 1900}, 
    400, {"message": "year"}, "T12 - past year",
    marks=pytest.mark.xfail(reason="Bug: Minimum year validation missing")),

    # --- negative scenarios: badge ---
    ({**VALID_MOVIE, "badge": "badge"}, 400, {"message": "must be one of"}, "T13 - nonexsiste badge"),
    ({**VALID_MOVIE, "badge": 123}, 400, {"message": "must be one of"}, "T14 - invalid numbers in badge"),
    ({**VALID_MOVIE, "badge": "EXTENDED RUN"*500}, 400, {"message": "must be one of"}, "T15 - long badge"),
    
    # --- T16: Missing Field (Manual) ---
    ({"title": "Gladiator II: Extended Cut", "genre": "Action","duration": 155, "year": 2025}, 
    400, {"message": "required"}, "T16 - missing badge field")
]