
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
    def verify_not_equals(actual, unexpected, message="Values are unexpectedly equal"):
        """
        Verifies that two values are NOT equal.
        """
        assert actual != unexpected, f"{message}: {actual} == {unexpected}"

    @staticmethod
    def verify_greater_than(actual: int, expected_minimum: int, message="Value comparison failed"):
        """
        Verifies that 'actual' is strictly greater than 'expected_minimum'.
        """
        # האסרט עצמו כבר מבצע את ה-IF הפנימי. אם התנאי לא מתקיים, הוא זורק AssertionError.
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

    @staticmethod
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
    def list_equals(actual_list, expected_list, message):
        print(f"\n{actual_list}")
        print(f"\n{expected_list}")
        assert sorted(actual_list) == sorted(expected_list), f"{message} \nActual: {actual_list} \nExpected: {expected_list}"
   
    
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
   
        for i, res in enumerate(responses, 1):
            msg = f"Request #{i}: Expected status {expected}, but got {res.status}"
            
            APIVerify.soft_assert(res.status == expected, msg)



    @staticmethod
    def soft_assert_verify_not_equals(actual, unexpected, message=None):
        """
        מבצע Soft Assert שהערכים אינם שווים - ללא פעולות בטסט עצמו.
        """
        condition = (actual != unexpected)
        APIVerify.soft_assert(condition, f"{message}: {actual} == {unexpected}")


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
    
