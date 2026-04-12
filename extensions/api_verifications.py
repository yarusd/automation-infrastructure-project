
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
    def verify_required_fields_not_empty(input_data, required_fields: list):
        """
        הגרסה שבאמת מקבלת הכל: 
        גם אובייקט Response וגם רשימה (list) או דיקשנרי (dict) שכבר חולצו.
        """
        # 1. חילוץ הנתונים בצורה חכמה:
        # אם זה Response - נחלץ את ה-JSON. אם זה כבר דאטה - נשתמש בו כמו שהוא.
        if hasattr(input_data, 'json'):
            data = input_data.json()
        else:
            data = input_data

        report_errors = ""

        # 2. הבטחה שזה תמיד יהיה רשימה (גם אם זה סרט בודד מה-POST)
        movies_to_check = data if isinstance(data, list) else [data]

        for index, movie in enumerate(movies_to_check):
            m_id = movie.get('id', f"Index {index}")
            for field in required_fields:
                value = movie.get(field)
                if value is None or str(value).strip() == "":
                    report_errors += f"\n- Movie {m_id}: Missing or Empty {field}"

        assert report_errors == "", f"Found data integrity issues: {report_errors}"

    @staticmethod
    def list_equals(actual_list, expected_list, message):
            
        actual_set = {str(x).strip().lower() for x in actual_list}
        expected_set = {str(x).strip().lower() for x in expected_list}

        if actual_set != expected_set:
            diff = f"{message}\nOnly Actual: {actual_set - expected_set}\nOnly Expected: {expected_set - actual_set}"
            print(diff)
            assert actual_set == expected_set, diff
   
               

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
    def json_contains(response_data, expected_data, partial=True):
        """
        בדיקה גמישה: תומכת במילון (שדות) או במחרוזת (הודעות).
        """
        # אם זה מילון, נרוץ על המפתחות
        if isinstance(expected_data, dict):
            for key, value in expected_data.items():
                assert key in response_data, f"Key '{key}' missing"
                actual = response_data[key]
                
                # בדיקת הכלה חלקית למחרוזות, אחרת השוואה מלאה
                if partial and isinstance(value, str) and isinstance(actual, str):
                    assert value.lower() in actual.lower(), f"Expected {value} in {actual}"
                else:
                    assert str(actual) == str(value), f"Expected {value}, got {actual}"
        
        # אם זה לא מילון (מחרוזת/מספר), נבדוק הכלה בטקסט הכללי
        else:
            assert str(expected_data).lower() in str(response_data).lower(), \
                f"'{expected_data}' not found in response"


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
    def soft_assert_verify_not_equals(actual, unexpected, message=None):
        """
        מבצע Soft Assert שהערכים אינם שווים - ללא פעולות בטסט עצמו.
        """
        condition = (actual != unexpected)
        APIVerify.soft_assert(condition, f"{message}: {actual} == {unexpected}")


    @staticmethod
    def soft_verify_search_integrity(results, keyword):
        keyword = str(keyword).lower()

        # 1. טיפול במקרה של שגיאה (dict) במקום רשימה (list)
        # אם השרת החזיר שגיאה (כמו ב-400), נבדוק אם ה-keyword נמצא בהודעת השגיאה
        if isinstance(results, dict):
            error_msg = str(results.get('message', '')).lower()
            found_in_error = keyword in error_msg
            
            msg = f"Bug: Expected error message to contain '{keyword}', but got: '{error_msg}'"
            APIVerify.soft_assert(found_in_error, msg)
            return

        # 2. אם לא חזרו תוצאות בכלל (רשימה ריקה)
        if not results:
            APIVerify.soft_assert(False, f"Bug: Search for '{keyword}' returned 0 results!")
            return 

        # 3. בדיקת שלמות לכל סרט (כשהתוצאה היא רשימה)
        for m in results:
            title = str(m.get('title', '')).lower()
            genre = str(m.get('genre', '')).lower()
            cast = " ".join([str(a) for a in m.get('cast', [])]).lower()
            
            found = (keyword in title) or (keyword in genre) or (keyword in cast)
            
            msg = f"Bug: '{keyword}' not found in ID {m.get('id')} (Title/Genre/Cast)"
            APIVerify.soft_assert(found, msg)


    @staticmethod
    def verify_sorting(results, sort_key, sort_type="alpha"):
        # הגנה: אם זה לא רשימה (למשל חזר JSON שגיאה) או שאין מפתח - אל תבדוק
        if not isinstance(results, list) or not sort_key or len(results) < 2:
            return

        if sort_type == "numbers":
            values = [float(m.get(sort_key) or 0) for m in results]
            expected = sorted(values, reverse=True) # מיון מספרים (Rating/Year) מהגבוה לנמוך
        else:
            # לוגיקת "המילה הראשונה" - חסינה גם לרשימות (כמו Cast)
            def clean_val(m):
                val = m.get(sort_key)
                if isinstance(val, list): val = val[0] # אם זה רשימת שחקנים, קח את הראשון
                return str(val or "").lower().strip().split()[0]

            values = [clean_val(m) for m in results]
            expected = sorted(values)

        is_sorted = (values == expected)
        msg = f"Sorting Bug in {sort_key}! Got: {values[:3]}..."
        APIVerify.soft_assert(is_sorted, msg)


    @staticmethod
    def soft_verify_multiple_criteria(results, expected_values):
        """
        מתודה גלובלית לוידוא קריטריונים מרובים בתוצאות חיפוש.
        תומכת גם ברשימת ערכים וגם במילה בודדת.
        """
        vals = expected_values if isinstance(expected_values, list) else [expected_values]
        if isinstance(results, dict):
            error_msg = str(results.get('message', '')).lower()
            for v in vals:
                v_str = str(v).lower()
                APIVerify.soft_assert(v_str in error_msg, 
                                    f"Expected '{v_str}' to be in error message: '{error_msg}'")
            return

        if not results:
            APIVerify.soft_assert(False, f"No results returned for criteria: {vals}")
            return
        for movie in results:
            # איחוד כל שדות הטקסט של הסרט לחיפוש מהיר
            title = str(movie.get('title', ''))
            genre = str(movie.get('genre', ''))
            cast = " ".join(map(str, movie.get('cast', [])))
            movie_content = f"{title} {genre} {cast}".lower()
            for v in vals:
                v_str = str(v).lower()
                msg = f"Criteria '{v_str}' not found in Movie ID {movie.get('id')}"
                APIVerify.soft_assert(v_str in movie_content, msg)


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
    
