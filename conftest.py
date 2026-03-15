import pytest
from pytest import FixtureRequest
from playwright.sync_api import Page, Playwright
import os
from dotenv import load_dotenv
from appium import webdriver
from workflows.Mobile.mobile_flow import MobileFlows

from data.api.chuck_api_data import *
from data.web.movie_time_data import *
from utils.common_ops import load_config
from utils.fixture_helpers import get_browser, attach_screenshot, attach_trace
from workflows.api.chuck_api_flows import ChuckApiFlows
from workflows.web.chuck_web_flows import ChuckWebFlows
from workflows.web.movie_time_flows import MovieFlows
import time
import uuid
import sqlite3
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
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

@pytest.fixture(scope= "class")
def request_context(playwright: Playwright, request:FixtureRequest):
    request_context=playwright.request.new_context(base_url=CHUCK_BASE_URL)
    yield request_context
    request_context.dispose()

# @pytest.fixture(scope= "class")
# def mobile_driver(request:FixtureRequest):
#     driver = None
#     yield driver
#     driver.close()

# def mobile_flow(mobile_driver):
#     return MobileFlows(mobile_driver)



@pytest.fixture(scope = "class")
def movie_time_flows(page):
    page.goto(MOVIE_TIME_URL)
    return MovieFlows(page)

@pytest.fixture
def navigate_to_all_movies_page(movie_time_flows:MovieFlows):
    movie_time_flows.navigate_to_all_movies()
    movie_time_flows.navigate_to_all_category()


@pytest.fixture
def chuck_flows(request_context):
    return ChuckApiFlows(request_context)

@pytest.fixture
def chuck_web_flows(page):
    return ChuckWebFlows(page)


@pytest.fixture
def navigate_to_homepage(movie_time_flows:MovieFlows):
    movie_time_flows.navigate_to_homepage()



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



    
@pytest.fixture(scope="class")
def mobile_setup():
        dc = {}
        dc['udid'] = '8dad0f967d78'
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
