

PATCH_SCENARIOS = [
    # POSITIVE TESTS (Success 200)
    ({"title": "BLOCKBUSTER"}, 200, "Fields updated", "T13.1 - valid title Patch"),
    ({"year": 2023}, 200, "Fields updated", "T13.2 - valid year Patch"),
    ({"duration": 158}, 200, "Fields updated", "T13.3 - valid duration Patch"),
    ({"genre": "Animation"}, 200, "Fields updated", "T13.4 - valid genre Patch"),
    ({"badge": "COMING SOON"}, 200, "Fields updated", "T13.5 - valid badge Patch"),
    ({"rating": 10}, 200, "Fields updated", "T13.6 - max rating 10"),
    ({"rating": 6, "title": "New Title"}, 200, "Fields updated", "T13.7 - multi-field update"),

    # NEGATIVE TESTS (Validation Errors 400)
    ({"title": 1213}, 400, "must be a string", "T13.8 - numbers in title"),
    ({"title": "!@#$%"}, 400, "invalid characters", "T13.9 - special chars in title"),
    ({"title": ""}, 400, "empty", "T13.10 - empty title"),
    ({"rating": "hello"}, 400, "must be a number", "T13.11 - alpha in rating"),
    ({"rating": 30}, 400, "less than or equal to 10", "T13.12 - rating out of range"),
    ({"genre": "love"}, 400, "must be", "T13.13 - nonexsist genre field"),
    ({"year": 2500}, 400, "less than or equal to 2030", "T13.14 - year in far future"),
    ({"duration": -3}, 400, "must be a positive number", "T13.15 - negative num in duration"),
    ({"badge": "HOT"}, 400, "must be one of", "T13.16 - unauthorized badge status"),
    ({"new_field": "Booya"}, 400, "is not allowed", "T13.17 - field injection")
]