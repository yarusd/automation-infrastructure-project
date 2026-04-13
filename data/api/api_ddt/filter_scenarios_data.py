import pytest

FILTER_SCENARIOS = [
    #POSITIVE SCENARIOS
    ({"genre" : "action"},200, "action","1 - filter by genre"),
    ({"title" : "superman"},200, "superman","2 - filter by title"),
    ({"cast" : "tom cruise"},200, "om cruise","3 - filter by cast name"),
    ({"q" : "superman"},200, "superman","4 - filter by random keyword"),

   # POSITIVE BOUNDARY TESTS (2 to 50 characters)
    ({"title": "fl"}, 200, "fl", "5 - boundary: minimum 2 chars"),
    ({"title": "Mission: Impossible 8 — Dead Reckoning Part Two"}, 200, "mission", "6 - boundary: maximum  chars"),

    # NEGATIVE SCENARIOS: GENRE 
    ({"genre": ""}, 400, "empty", "7 - filter by empty genre"),
    ({"genre": "lovely"}, 400, "no movies found", "8 - filter by nonexsiste genre"),

    # NEGATIVE SCENARIOS: TITLE 
    ({"title": "m" * 51}, 400, "must be 2-50 chars", "9 - title keyword too long"),
    ({"title": "m"}, 400, "must be 2-50 chars", "10 - title keyword too short"),

    # NEGATIVE SCENARIOS: CAST
    ({"cast": "!@#$$"}, 400, "invalid", "11 - cast: invalid special characters"),

    # NEGATIVE SCENARIOS : Q
    ({"q": "!@#$$"}, 400, "invalid", "12 - q: invalid special characters"),
    ({"q": ""}, 400, "empty", "T15 - filter by empty keyword"),

    pytest.param({"q" : "125"}, 200, "125", "13 - filter by random number",
    marks=pytest.mark.xfail(reason=": Global search (q) does not filter by Duration field"))
]