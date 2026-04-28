# 🏗️ YT Automation Labs: Multi-Platform Testing Ecosystem

Welcome to the official repository of **YT Automation Labs**. This project showcases a robust, industrial-grade automation infrastructure designed to validate a complex ecosystem across **Web and API** platforms.

This suite demonstrates the power of scalable test architecture, Data-Driven Testing (DDT), and modern CI/CD integration.

---

## 🛰️ System Architecture
Our framework is built on a modular, decoupled architecture to ensure maintainability and reusability:

| Layer | Technology | Focus |
| :--- | :--- | :--- |
| **Frontend (Web)** | **Playwright** / Pytest | Modern E2E flows, Page Object Model (POM), Cross-browser stability. |
| **Backend (API)** | Requests Library | Business logic, JSON Schema validation, Persistence layer checks. |
| **Data Layer** | SQLite & DDT | Data-Driven Testing using external DB and JSON sources. |
| **CI/CD** | Render / GitHub Actions | Automated execution triggers and cloud-based deployment. |

---

## 🚀 Test Coverage & Platforms

### 🌐 Web UI Automation
**Target Site:** [MovieTime Theater](https://yarusd.github.io/movie-theater/)  
Powered by **Playwright**, the web suite focuses on high-performance user scenarios:
* **State-Based Flows:** Validating system behavior for Guests vs. Authenticated users.
* **Dynamic UI Components:** Testing sliders, theme toggles (Dark/Light), and responsive layouts.
* **Complex E2E:** Full booking cycle—from search to secure payment simulation.
* **Order Management:** Specialized flows for order placement and cancellation.

### ⚙️ API & Backend Integrity
**Target AP & Documentation:** [API Documentation](https://movie-time-api.onrender.com/docs)  
Robust validation of data integrity and server-side logic:
* **DDT (Data-Driven Testing):** Extensive data validation using **SQLite** to compare DB records vs. API responses.
* **JSON Schema Enforcement:** Guaranteeing unique IDs and mandatory field constraints (Not Null).
* **Search & Filter Logic:** Verifying precise retrieval of resources based on category and text queries.
* **Server Reliability:** Assessing status codes and response times on the **Render** production environment.

---

## 📊 Reporting & Quality Insights
The project utilizes **Allure Reports** to provide a 360° view of our quality status:
* 📸 **Visual Evidence:** Automatic screenshots and traces upon Web failures.
* 📜 **Execution Logs:** Detailed request/response tracing for API debugging.
* 📈 **Severity Levels:** Categorizing tests by business impact (Critical, Normal, Minor).

---

## 🛠️ Quick Start
```bash
# Clone the repository
git clone [https://github.com/YT-Automation-Labs/automation-infrastructure.git](https://github.com/YT-Automation-Labs/automation-infrastructure.git)

# Install dependencies
pip install -r requirements.txt

# Run Playwright & API tests
pytest --alluredir=reports
