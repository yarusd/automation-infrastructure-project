
class APIVerify:
    @staticmethod
    def status_code(response, expected_status_code: int):
        """
        Verifies that the API response status code matches the expected status code.
        """
        if isinstance(response, dict):  # If it's already JSON, we can't check status
            raise ValueError("Expected a Playwright response object, but got a dictionary. Ensure status code is checked before calling .json()")
        assert response.status == expected_status_code, \
            f"Expected status code {expected_status_code}, but got {response.status}"
        
    @staticmethod
    def verify_values_not_equals(actual, unexpected, message="Values are unexpectedly equal"):
        assert actual != unexpected, f"{message}: {actual} == {unexpected}"
    
    @staticmethod
    def verify_values_equals(actual, unexpected, message="Values are unexpectedly equal"):
        assert actual == unexpected, f"{message}: {actual} != {unexpected}"

    @staticmethod
    def verify_greater_than(actual: int, expected_minimum: int, message="Value comparison failed"):
        """
        Verifies that 'actual' is strictly greater than 'expected_minimum'.
        """
        assert actual > expected_minimum, \
            f"{message}: Expected {actual} to be greater than {expected_minimum}"


    @staticmethod
    def json_key_exists(response_data, key: str):
        """
        Verifies that a specific key exists in the JSON response.
        """
        assert key in response_data, f"Key '{key}' not found in the response JSON"

    
    @staticmethod
    def json_value_equals(response_data, key: str, expected_value):
        """
        Verifies that a specific key in the JSON response has the expected value.
        """
        assert response_data[key] == expected_value, (
            f"Expected value for key '{key}' is '{expected_value}', but got '{response_data[key]}'"
        )

    @staticmethod  #CHUCK
    def verify_required_fields_not_null(response_data: dict, required_fields: list):
        """
        Verifies that required fields exist and are not null/empty.
        """
        for field in required_fields:
            assert field in response_data, f"Field '{field}' is missing in response"

            value = response_data[field]
            assert value is not None, f"Field '{field}' is None"
            assert value != "", f"Field '{field}' is empty"


    @staticmethod
    def verify_required_fields_not_empty(movies_list: list, required_fields: list):
        report_errors = ""
                
        for index, movie in enumerate(movies_list):
                m_id = movie.get('id', f"Index {index}")
                    
                for field in required_fields:
                        value = movie.get(field)
                        if value is None or str(value).strip() == "":
                            report_errors += f"\n- Movie {m_id}: Missing {field}"

        assert report_errors == "", f"Found missing data in API response: {report_errors}"

            
    @staticmethod
    def list_equals(actual_list, expected_list, message):
            
            clean_actual = sorted([str(movie).strip().lower() for movie in actual_list])
            clean_expected = sorted([str(movie).strip().lower() for movie in expected_list])

            assert clean_actual == clean_expected, f"{message} - Lists are still not identical after cleaning."
   
    
    @staticmethod
    def json_contains(response_data, expected_data: dict):
        """
        Verifies that the JSON response contains the expected data.
        """
        for key, value in expected_data.items():
            assert key in response_data, f"Key '{key}' not found in the response JSON"
            assert response_data[key] == value, (
                f"Expected value for key '{key}' is '{value}', but got '{response_data[key]}'"
            )

    # Soft Assertions
    errors = []


    @staticmethod
    def soft_verify_statuses(responses: list, expected: int):
   
        if not responses:
                APIVerify.soft_assert(False, "❌ Error: Response list is empty! Check your Flow.")
                return

        for i, res in enumerate(responses, 1):
                actual = res.status
                msg = f"Request #{i}: Expected status {expected}, but got {actual}"
                
                # ביצוע ה-Soft Assert
                APIVerify.soft_assert(actual == expected, msg)


    @staticmethod
    def verify_all_movies_match_criteria(movie_list: list, criteria: dict):
        """
        עובר על כל הסרטים ומוודא שהם תואמים למאפיינים שביקשנו.
        """
        for movie in movie_list:
            for key, expected_value in criteria.items():
                # שליפת הערך מהסרט (מחזיר None אם המפתח חסר)
                actual_value = movie.get(key)
                condition = str(actual_value).lower() == str(expected_value).lower()
                
                if not condition:
                    error_msg = f"Movie ID {movie.get('id')}: Expected {key}='{expected_value}', but got '{actual_value}'"
                    APIVerify.soft_assert(False, error_msg)


    @staticmethod
    def soft_assert_verify_not_equals(actual, unexpected, message=None):
        """
        מבצע Soft Assert שהערכים אינם שווים - ללא פעולות בטסט עצמו.
        """
        condition = (actual != unexpected)
        APIVerify.soft_assert(condition, f"{message}: {actual} == {unexpected}")


    @staticmethod
    def soft_verify_keyword_anywhere_in_results(results_list: list, keyword: str):
      
        import json
        
        for i, movie_obj in enumerate(results_list):
            # הופכים את כל האובייקט של הסרט למחרוזת טקסט אחת גדולה
            movie_as_str = json.dumps(movie_obj).lower()
            
            # בודקים אם מילת המפתח נמצאת בתוך הטקסט הזה
            condition = keyword.lower() in movie_as_str
            
            msg = f"Result #{i}: Keyword '{keyword}' was not found anywhere in the movie data."
            APIVerify.soft_assert(condition, msg)


    @staticmethod
    def soft_assert(condition: bool, message: str):
        if not condition:
            # לא עוצר – רק אוסף את ההודעה
            APIVerify.errors.append(message)


    @staticmethod
    def assert_all():
        """
        Raises all collected assertion errors at once.
        """
        if APIVerify.errors:
            error_message = "\n".join(APIVerify.errors)
            APIVerify.errors.clear()  # Clear errors after raising
            raise AssertionError(f"Soft assertion failures:\n{error_message}")
    
