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
* **Get Random Joke:** Validating `200 OK` and non-empty response body.
* **Get by Category:** Filtering resources and verifying data relevance.
* **Resource Creation (POST):** Adding new entries and verifying persistence.
* **Update Resource (PUT/PATCH):** Modifying existing data and checking updates.
* **Delete Resource:** Removing data and verifying it no longer exists.
* **Negative Testing (404):** Requesting non-existent resources.
* **Authentication (401):** Accessing protected endpoints without a token.
* **Schema Validation:** Ensuring the JSON structure matches the contract.
* **Response Time:** Performance check to ensure responses are under 2 seconds.
* **Data Integrity:** Cross-referencing API results with the SQL Database (SQLite).

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
