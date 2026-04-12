
import pytest


SORT_SCENARIOS = [
    # POSITIVE SCENARIOS:
    # Payload, Expected Status, Sort Key, Sort Type, Test Num
    ({"sort": "year"}, 200, "year", "numbers", "T5.1 - Year Sort"),
    ({"sort": "title"}, 200, "title", "alpha", "T5.2 - Title Sort"),
    ({"sort": "rating"}, 200, "rating", "numbers", "T5.3 - Rating Sort"),
    ({"sort": "cast"}, 200, "cast", "alpha", "T5.4 - Cast Sort"),
    ({"sort": "duration"}, 200, "duration", "numbers", "T5.5 - Duration Sort"),
    ({"sort": "badge"}, 200, "badge", "alpha", "T5.6 - badge Sort"),
    
    # Negative: 
    ({"sort": ""}, 400, None, "numbers", "T5.7 - Empty Sort"),
    # bug:
    pytest.param({"sort": "love"}, 400, None, "alpha", "T5.8 - Nonexistent Sort",
    marks=pytest.mark.xfail(reason=": API returns 200 OK for invalid sort fields instead of 400 Bad Request"))
]

