
DELETE_MOVIE_SCENARIOS = [
                        ("1", 200, "1 - valid ID"),           # בהנחה ש-123 קיים
                        ("999999", 404, "2 - nonesxist ID"),
                        ("abc", 400, "3 - string in id")
                    ]