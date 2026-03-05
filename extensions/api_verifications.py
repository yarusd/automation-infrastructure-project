
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
    def compare_values(value1: int, value2: int):
        """
        Compares two integer values and asserts that the first value is greater than the second.
        Provides a clear assertion message indicating the relationship.
        """
        if value1 > value2:
            assert value1 > value2
        elif value1 < value2:
            raise AssertionError(f"{value2} is greater than {value1}")
        else:
            raise AssertionError(f"Both values are equal: {value1}")


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
    @staticmethod
    def soft_assert_status_code(response, expected_status_code: int):
        """
        Soft asserts that the API response status code matches the expected status code.
        """
        if isinstance(response, dict):  
            APIVerify.errors.append("Expected a Playwright response object, got a dictionary.")

        elif response.status != expected_status_code:
            APIVerify.errors.append(
                f"Expected status code {expected_status_code}, but got {response.status}."
            )



    errors = []

    @staticmethod
    def verify_responses_status_ok(responses: list, expected_status_code: int = 200):
        """
        Iterates over all APIResponse objects and soft asserts that each has status 200.
        """
        for i, response in enumerate(responses, start=1):
            if isinstance(response, dict):
                APIVerify.errors.append(f"Expected APIResponse, got dict at request #{i}")
            elif response.status != expected_status_code:
                APIVerify.errors.append(
                    f"Request #{i}: Expected status {expected_status_code}, got {response.status}"
                )



    errors = []

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
<<<<<<< HEAD
        if VerifyAPI.errors:
            error_message = "\n".join(VerifyAPI.errors)
            VerifyAPI.errors.clear()  # Clear errors after raising
            raise AssertionError(f"Soft assertion failures:\n{error_message}")
    
    @staticmethod
    def list_equals(actual_list, expected_list, message):
        assert sorted(actual_list) == sorted(expected_list), f"{message} \nActual: {actual_list} \nExpected: {expected_list}"
=======
        if APIVerify.errors:
            error_message = "\n".join(APIVerify.errors)
            APIVerify.errors.clear()  # Clear errors after raising
            raise AssertionError(f"Soft assertion failures:\n{error_message}")
>>>>>>> yarus
