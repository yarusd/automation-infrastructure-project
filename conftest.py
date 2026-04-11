import os
import allure
import pytest
import time
import uuid
import sqlite3

from appium import webdriver
from dotenv import load_dotenv
import requests
from tenacity import *
from utils.common_ops import load_config
from pytest import FixtureRequest
from data.api.chuck_api_data import *
from data.web.movie_time_data import *
from data.api.movie_api_data import *
from playwright.sync_api import Page, Playwright
from workflows.api.movie_api_flows import MovieApiFlows
from workflows.mobile.mobile_flow import MobileFlows
from workflows.api.chuck_api_flows import ChuckApiFlows
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

    @retry(stop=stop_after_delay(60), wait=wait_fixed(2), reraise=True)
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
def chuck_context(playwright: Playwright):
    context = playwright.request.new_context(base_url=CHUCK_BASE_URL)
    yield context
    context.dispose()

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


@pytest.fixture
def chuck_flows(chuck_context):
    return ChuckApiFlows(chuck_context)

@pytest.fixture
def chuck_web_flows(page):
    return ChuckWebFlows(page)

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
    """
    Hook to attach screenshots, videos, and traces to Allure reports on test failure.
    """

    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
            page = item.funcargs.get("page")

            # Check if page exists AND our custom flag is True
            if page and getattr(page, "_tracing_active", False):
                timestamp = time.strftime("%Y%m%d-%H%M%S")
                unique_id = str(uuid.uuid4())[:8]
                base_filename = f"{item.name}_{timestamp}_{unique_id}"

                # Attach screenshot
                screenshot_path = os.path.join(CONFIG['ALLURE_RESULTS_DIR'], f"{CONFIG['SCREENSHOT_PREFIX']}_{base_filename}.png")
                attach_screenshot(page, item.name, screenshot_path)

                # Attach trace (only called if _tracing_active is True)
                trace_name = f"{CONFIG['TRACE_PREFIX']}_{item.name}_{timestamp}.zip"
                trace_path = os.path.join(CONFIG['ALLURE_RESULTS_DIR'], trace_name)
                
                try:
                    attach_trace(page, item.name, trace_path)
                    # Set to False so we don't try to stop it again elsewhere
                    page._tracing_active = False 
                except Exception as e:
                    print(f"Failed to stop/attach trace: {e}")



