import os
import allure
import pytest
import time
import uuid
import sqlite3
from utils.jira_reporter import add_attachment_to_jira, report_jira_bug
from appium import webdriver
from dotenv import load_dotenv
import requests
from tenacity import *
from utils.common_ops import load_config
from pytest import FixtureRequest
from data.web.movie_time_data import *
from data.api.movie_api_data import *
from playwright.sync_api import Page, Playwright
from workflows.api.movie_api_flows import MovieApiFlows
from workflows.mobile.mobile_flow import MobileFlows
from workflows.web.chuck_web_flows import ChuckWebFlows
from workflows.web.movie_time_flows import MovieFlows
from utils.fixture_helpers import get_browser, attach_screenshot, attach_trace


load_dotenv()
# Load the configuration
CONFIG = load_config()     

@pytest.fixture(scope = "class")
def page(playwright: Playwright, request:FixtureRequest):
    browser = get_browser(playwright,CONFIG["BROWSER_TYPE"].lower())
    context = browser.new_context(no_viewport=True)    
    context.tracing.start(screenshots=True, snapshots=True, sources=True)    
    page = context.new_page()
    page._tracing_active = True
    yield page    
    # Best practice: Close page before context
    page.close()
    context.close()
    browser.close()

#to wake the free use RENDER:
@pytest.fixture(scope="session", autouse=True)
def wake_up_movie_api(request):
    if not any("api" in item.nodeid for item in request.session.items):
        return
    print(f"\n--- 🔄 Waking up Movie API... ---")

    @retry(stop=stop_after_delay(62), wait=wait_fixed(2), reraise=True)
    def attempt():
        requests.get(MOVIE_API_URL, timeout=5).raise_for_status()
    try:
        attempt()
        print("--- ✅ API is Awake! ---")
    except:
        print("--- ⚠️ Wake-up failed ---")
        
    
@pytest.fixture(scope = "class")
def movie_time_flows(page):
    page.goto(MOVIE_TIME_URL)
    return MovieFlows(page)

@pytest.fixture
def navigate_to_all_movies_page(movie_time_flows:MovieFlows):
    movie_time_flows.navigate_to_all_movies()
    movie_time_flows.navigate_to_all_category()


@pytest.fixture
def navigate_to_homepage(movie_time_flows:MovieFlows):
    movie_time_flows.navigate_to_homepage()


@pytest.fixture(scope="class")
def movie_context(playwright: Playwright):
    context = playwright.request.new_context(base_url=MOVIE_API_URL)
    yield context
    context.dispose()

@pytest.fixture
def movie_flows(movie_context):
    return MovieApiFlows(movie_context)

@pytest.fixture(autouse=True)
def setup_clean_database(movie_flows: MovieApiFlows, request):
    response = None 
        
    if "test_movie_api" in request.node.nodeid:
            with allure.step("Setup: Resetting database before test"):
                response = movie_flows.delete_request(DELETE_DATABASE, use_api_key=True)
                
    yield response


@pytest.fixture(scope="function")
def web_sync_context(playwright: Playwright):
    browser = get_browser(playwright, CONFIG["BROWSER_TYPE"].lower())
    context = browser.new_context(no_viewport=True)    
    context.tracing.start(screenshots=True, snapshots=True, sources=True)    
    page = context.new_page()
    page._tracing_active = True
    page.goto(MOVIE_TIME_URL)
    flows = MovieFlows(page)
    yield flows 
    page.close()
    context.close()
    browser.close()



@pytest.fixture(scope="class")
def mobile_setup():
        dc = {}
        dc['udid'] = 'RF8N63P9Z9R'
        dc['appPackage'] = 'com.example.android.apis'
        dc['appActivity'] = '.ApiDemos'
        dc['platformName'] = 'android'
        driver = webdriver.Remote('http://localhost:4724/wd/hub',dc)
        driver.implicitly_wait(10)
        yield driver
        driver.quit()


@pytest.fixture(scope="function")
def mobile_flows(mobile_setup):
    # Injecting the driver instance into the business logic layer
    return MobileFlows(mobile_setup)


@pytest.fixture(scope="class")
def db_connection():
    path = "tests/api/joke_categories.db"
    conn = sqlite3.connect(path)
    yield conn
    conn.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        jira_key = None
        is_new = False

        # --- JIRA REPORTING DISABLED (Quick way) ---
        # try:
        #     allure_title_marker = item.get_closest_marker("allure_title")
        #     display_title = allure_title_marker.args[0] if allure_title_marker else item.name
        #     
        #     allure_severity = item.get_closest_marker("allure_severity")
        #     severity_val = allure_severity.args[0] if allure_severity else "normal"
        #     priority_level = "High" if severity_val in ['critical', 'blocker'] else "Medium"
        #
        #     browser_name = CONFIG.get("BROWSER_TYPE", "Unknown").upper()
        #     
        #     error_lines = str(report.longreprtext).split('\n')
        #     short_error = error_lines[-1] if error_lines else "Unknown Error"
        #
        #     formatted_description = (
        #         f"h2. 🛑 Test Failure: {display_title}\n\n"
        #         f"*Technical Name:* `{item.name}`\n"
        #         f"*Summary:* {short_error}\n"
        #         f"*Environment:* QA Automation | *Browser:* {browser_name}\n\n"
        #         f"h3. 📝 Error Details\n"
        #         f"{{code:python}}\n{report.longreprtext}\n{{code}}\n\n"
        #         f"---- \n"
        #         f"ℹ️ _This bug was created automatically by the Playwright Automation Framework._"
        #     )
        #
        #     jira_key, is_new = report_jira_bug(
        #         test_name=item.name, 
        #         summary=f"Bug: {display_title} - {short_error[:40]}", 
        #         description=formatted_description,
        #         priority=priority_level,
        #         labels=['Automation', 'Playwright', browser_name]
        #     )
        #     
        #     if jira_key:
        #         allure.dynamic.link(f"{os.getenv('JIRA_URL')}/browse/{jira_key}", name=f"Jira: {jira_key}")
        # except Exception as e:
        #     print(f"Jira reporting failed (Expected - Disabled): {e}")

        # --- טיפול בצילומי מסך ו-Trace (נשאר פעיל עבור Allure בלבד) ---
        page = item.funcargs.get("page")
        if page and getattr(page, "_tracing_active", False):
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            unique_id = str(uuid.uuid4())[:8]
            base_filename = f"{item.name}_{timestamp}_{unique_id}"

            screenshot_path = os.path.join(CONFIG['ALLURE_RESULTS_DIR'], f"{CONFIG['SCREENSHOT_PREFIX']}_{base_filename}.png")
            attach_screenshot(page, item.name, screenshot_path)

            # ניסיון צירוף הקובץ לג'ירה מושבת כי jira_key תמיד יהיה None
            # if jira_key and is_new:
            #     add_attachment_to_jira(jira_key, screenshot_path)

            trace_name = f"{CONFIG['TRACE_PREFIX']}_{item.name}_{timestamp}.zip"
            trace_path = os.path.join(CONFIG['ALLURE_RESULTS_DIR'], trace_name)
            try:
                attach_trace(page, item.name, trace_path)
                page._tracing_active = False 
            except Exception as e:
                print(f"Failed to stop/attach trace: {e}")



# אחרי שנסיים את כל הטסטים- להוריד מהערה ולמחוק את הנוכחי.
# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     outcome = yield
#     report = outcome.get_result()

#     if report.when == "call" and report.failed:
#         jira_key = None
#         is_new = False

#         try:
#             # --- שיפור 1: חילוץ כותרת Allure (במקום שם הפונקציה הטכני) ---
#             allure_title_marker = item.get_closest_marker("allure_title")
#             display_title = allure_title_marker.args[0] if allure_title_marker else item.name
            
#             # --- שיפור 2: חילוץ חומרה (Severity) לטובת עדיפות בג'ירה ---
#             allure_severity = item.get_closest_marker("allure_severity")
#             severity_val = allure_severity.args[0] if allure_severity else "normal"
#             priority_level = "High" if severity_val in ['critical', 'blocker'] else "Medium"

#             # --- שיפור 3: חילוץ דפדפן מהקונפיג ---
#             browser_name = CONFIG.get("BROWSER_TYPE", "Unknown").upper()
            
#             error_lines = str(report.longreprtext).split('\n')
#             short_error = error_lines[-1] if error_lines else "Unknown Error"

#             # עיצוב התיאור עם כותרת קריאה ופרטי סביבה
#             formatted_description = (
#                 f"h2. 🛑 Test Failure: {display_title}\n\n"
#                 f"*Technical Name:* `{item.name}`\n"
#                 f"*Summary:* {short_error}\n"
#                 f"*Environment:* QA Automation | *Browser:* {browser_name}\n\n"
#                 f"h3. 📝 Error Details\n"
#                 f"{{code:python}}\n{report.longreprtext}\n{{code}}\n\n"
#                 f"---- \n"
#                 f"ℹ️ _This bug was created automatically by the Playwright Automation Framework._"
#             )

#             # שליחה לג'ירה - שים לב שאנחנו שולחים את ה-display_title לסמרי
#             # אבל משאירים את item.name לטובת בדיקת כפילויות בתוך report_jira_bug
#             jira_key, is_new = report_jira_bug(
#                 test_name=item.name, 
#                 summary=f"Bug: {display_title} - {short_error[:40]}", 
#                 description=formatted_description,
#                 priority=priority_level,
#                 labels=['Automation', 'Playwright', browser_name]
#             )
            
#             if jira_key:
#                 allure.dynamic.link(f"{os.getenv('JIRA_URL')}/browse/{jira_key}", name=f"Jira: {jira_key}")
#         except Exception as e:
#             print(f"Jira reporting failed: {e}")

#         # --- טיפול בצילומי מסך ו-Trace (נשאר כפי שהיה, רק מוודא שמשתמשים ב-jira_key) ---
#         page = item.funcargs.get("page")
#         if page and getattr(page, "_tracing_active", False):
#             timestamp = time.strftime("%Y%m%d-%H%M%S")
#             unique_id = str(uuid.uuid4())[:8]
#             base_filename = f"{item.name}_{timestamp}_{unique_id}"

#             screenshot_path = os.path.join(CONFIG['ALLURE_RESULTS_DIR'], f"{CONFIG['SCREENSHOT_PREFIX']}_{base_filename}.png")
#             attach_screenshot(page, item.name, screenshot_path)

#             if jira_key and is_new:
#                 add_attachment_to_jira(jira_key, screenshot_path)
#             elif jira_key and not is_new:
#                 print(f"ℹ️ Skipping screenshot upload for existing bug {jira_key}")

#             trace_name = f"{CONFIG['TRACE_PREFIX']}_{item.name}_{timestamp}.zip"
#             trace_path = os.path.join(CONFIG['ALLURE_RESULTS_DIR'], trace_name)
#             try:
#                 attach_trace(page, item.name, trace_path)
#                 page._tracing_active = False 
#             except Exception as e:
#                 print(f"Failed to stop/attach trace: {e}")