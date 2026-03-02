# Automation Testing Final Project: Web & API

## 📌 Project Overview
This project is a comprehensive automated testing suite designed as a final graduation project. It demonstrates advanced automation capabilities by covering both **Frontend (Web UI)** and **Backend (REST API)** testing layers. The suite ensures system stability, data integrity, and a seamless user experience.

## 🛠️ Tech Stack
* **Language:** Python
* **Web Automation:** Selenium WebDriver / Pytest
* **API Testing:** Requests library
* **Reporting:** Allure Reports
* **Database:** SQLite (for data-driven testing and validation)

---

## 🧪 Test Coverage

### 1. Web UI Automation (10 Test Cases)
The Web suite focuses on end-to-end user scenarios, UI components, and cross-browser functionality:
* **User Authentication:** Login with valid credentials and session verification.
* **Failed Login:** Error message validation for incorrect password/email.
* **Registration Flow:** Creating a new user account with unique data.
* **Search Functionality:** Validating search results for specific keywords.
* **Add to Cart:** Ensuring items are correctly added to the shopping session.
* **Checkout Process:** End-to-end flow from cart to order confirmation.
* **Filter & Sort:** Verifying product filtering by price, category, and rating.
* **Responsive Design:** Checking element visibility on different screen resolutions.
* **Form Validation:** Testing mandatory fields and input constraints.
* **Logout Flow:** Ensuring secure session termination.

### 2. API Testing (10 Test Cases)
The API suite validates the business logic, status codes, and JSON schema integrity:
* **Get Random Joke: Validates the successful retrieval of a random joke with a 200 OK status code.
* **Get Joke by Category: Ensures that fetching a joke from a specific category returns a valid and relevant response.
* **Get Categories List: Verifies that the endpoint for retrieving all available joke categories is functional and accurate.
* **Verify Free Text Search: Validates the free-text search functionality for jokes containing specific keywords.
* **Verify Required Fields: Ensures that essential response fields, such as ID and content, are not null and maintain data integrity.
* **Get Categories from DB: Validates the persistence layer by retrieving and verifying category data from the SQLite database.
* **Compare Result Counts: Compares the volume of results between different search queries to ensure consistency.
* **Verify Joke Web URL: Extracts and validates the integrity and format of the joke's direct web link.
* **Verify Unique ID: Ensures that every joke returned by the service carries a globally unique identifier.
* **Verify Content Uniqueness: Confirms that joke text content is unique and not duplicated across different API responses.

---

## 📊 Reports & Insights
The project utilizes **Allure Reports** to provide a clear, visual representation of test results, including:
* Step-by-step execution logs.
* Screenshots of failed Web tests.
* Detailed request/response logs for API tests.
* Severity levels and execution trends.

## 🚀 How to Run
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/your-project.git](https://github.com/your-username/your-project.git)
