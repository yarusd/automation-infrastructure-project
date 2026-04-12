COMBINED_FILTER_SCENARIOS = [
    # POSITIVE SCENARIOS:
    ({"title": "superman", "genre": "action"}, 200, ["superman","action"], "T4.1 - Title and Genre match"),
    ({"cast": "Chris Evans", "genre": "romance"}, 200, ["chris","romance"], "T4.2 - Cast and Genre match"),
    ({"q": "wicked", "cast": "Ariana Grande"}, 200, ["wicked","Ariana Grande"], "T4.3 - Q + Year match"),
    
    # NEGATIVE: MISMATCH
    ({"title": "superman", "genre": "Romance"}, 400, "No movies found", "T4.4 - No results for Romance in Superman"),
    ({"q": "flow", "year": "2025"}, 400, "No movies found", "T4.5 - No results for 2025 in Flow"),
    ({"cast": "tom cruise", "genre": "romance"}, 400, "No movies found", "T.6 - cast exists but genre mismatch"),

    # NEGATIVE: INVALID COMBINATIONS
    ({"genre": "Action", "sort": "rating"}, 400, "cannot combine", "T4.7 - Genre + Sort: Forbidden"),
    ({"genre": "Action", "year": ""}, 400, "cannot be empty", "T4.8 - valid Genre + empty year"),
    ({"title": "!@#", "cast": "tom cruies"}, 400, "Invalid", "T4.9 - special chars + valid cast")

]