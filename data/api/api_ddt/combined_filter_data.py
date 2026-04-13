COMBINED_FILTER_SCENARIOS = [
    # POSITIVE SCENARIOS:
    ({"title": "superman", "genre": "action"}, 200, ["superman","action"], "1 - Title and Genre match"),
    ({"cast": "Chris Evans", "genre": "romance"}, 200, ["chris","romance"], "2 - Cast and Genre match"),
    ({"q": "wicked", "cast": "Ariana Grande"}, 200, ["wicked","Ariana Grande"], "3 - Q + Year match"),
    
    # NEGATIVE: MISMATCH
    ({"title": "superman", "genre": "Romance"}, 400, "No movies found", "4 - No results for Romance in Superman"),
    ({"q": "flow", "year": "2025"}, 400, "No movies found", "5 - No results for 2025 in Flow"),
    ({"cast": "tom cruise", "genre": "romance"}, 400, "No movies found", "T.6 - cast exists but genre mismatch"),

    # NEGATIVE: INVALID COMBINATIONS
    ({"genre": "Action", "sort": "rating"}, 400, "cannot combine", "7 - Genre + Sort: Forbidden"),
    ({"genre": "Action", "year": ""}, 400, "cannot be empty", "8 - valid Genre + empty year"),
    ({"title": "!@#", "cast": "tom cruies"}, 400, "Invalid", "9 - special chars + valid cast")

]