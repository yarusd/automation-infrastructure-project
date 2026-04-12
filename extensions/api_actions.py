import json
from typing import Optional
import allure
from playwright.sync_api import APIRequestContext

class APIActions:
    def __init__(self, request_context: APIRequestContext):
        """
        Initialize APIActions with a Playwright APIRequestContext.
        """
        self.request_context = request_context


    @allure.step("Send GET request to {url}")
    def get(self, url: str, params: Optional[dict] = None, headers: Optional[dict] = None):
        """
        Send a GET request to the specified URL with optional parameters and headers.
        """
        response = self.request_context.get(url, params=params, headers=headers)
        self._log_response(response)  # Log the response
        return response
    

    @allure.step("Send POST request to {url}")
    def post(self, url: str, payload: dict, headers: Optional[dict] = None):
        """
        Send a POST request to the specified URL with a JSON payload and optional headers.
        """
        final_headers = {"Content-Type": "application/json"}
        
        if headers:
            final_headers.update(headers)

        response = self.request_context.post(
            url,
            data=json.dumps(payload),
            headers=final_headers
        )
        self._log_response(response)
        return response

    @allure.step("Send PUT request to {url}")
    def put(self, url: str, payload: dict, headers: dict = None):
        request_headers = {"Content-Type": "application/json"}
        
        if headers:
            request_headers.update(headers)

        response = self.request_context.put(
            url,
            data=json.dumps(payload),
            headers=request_headers
        )
        self._log_response(response)
        return response
    
    @allure.step("Send PATCH request to {url}")
    def patch(self, url: str, payload: dict, headers: Optional[dict] = None):
        request_headers = {"Content-Type": "application/json"}
        
        if headers:
            request_headers.update(headers)

        response = self.request_context.patch(
            url,
            data=json.dumps(payload),
            headers=request_headers
        )
        self._log_response(response)
        return response


    @allure.step("Send DELETE request to {url}")
    def delete(self, url: str, headers: Optional[dict] = None):
        """
        Send a DELETE request. Merges default headers with provided headers.
        """
        request_headers = {"Content-Type": "application/json"}
        if headers:
            request_headers.update(headers)
            
        response = self.request_context.delete(
            url,
            headers=request_headers
        )
        self._log_response(response)
        return response
    
    

    @allure.step("Log Response")
    def _log_response(self, response):
        """
        Log response details to Allure report safely.
        """
        try:
            # נסיון לחלץ JSON לצורך תצוגה יפה בדו"ח
            response_data = response.json()
            content = json.dumps(response_data, indent=4)
            type = allure.attachment_type.JSON
        except Exception:
            # אם זה לא JSON (למשל HTML), נשמור את הטקסט הגולמי
            content = response.text()
            type = allure.attachment_type.TEXT

        allure.attach(
            content,
            name=f"API Response - {response.status}",
            attachment_type=type
        )
        # assert response.ok, f"API request failed with status {response.status} - {response.text()}"


    @staticmethod
    @allure.step("Get occurrence count of '{text}' in page source")
    def get_text_count_in_source(driver, text: str) -> int:
        """
        Retrieves the full page source and counts how many times 
        a specific string appears.
        """
        source = driver.page_source
        return source.count(text)
    

    @staticmethod
    def count(response) -> int:
        """
        מחזירה את מספר האיברים ברשימת ה-JSON.
        """
        # response.json() הופך את התוצאה לרשימה/מילון של פייתון
        return len(response)