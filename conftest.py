import pytest
from pytest import FixtureRequest
from playwright.sync_api import Page, Playwright
import os
from dotenv import load_dotenv

load_dotenv()
from data.api.chuck_api_data import *
from data.web.movie_time_data import *
from utils.common_ops import load_config
from utils.fixture_helpers import get_browser, attach_screenshot, attach_trace
from workflows.api.chuck_api_flows import ChuckApiFlows
from workflows.web.chuck_web_flows import ChuckWebFlows
from workflows.web.movie_time_flows import MovieFlows
import os
import time
import uuid
import pytest
import sqlite3
# Load the configuration
CONFIG = load_config()     

@pytest.fixture(scope="class")
def page(playwright: Playwright, request:FixtureRequest):
    browser = get_browser(playwright,CONFIG["BROWSER_TYPE"].lower())
    context = browser.new_context(no_viewport=True)    
    context.tracing.start(screenshots=True, snapshots=True, sources=True)    
    page = context.new_page()
    page.goto(MOVIE_TIME_URL)
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


@pytest.fixture
def movie_time_flows(page):
    return MovieFlows(page)

@pytest.fixture
def navigate_to_all_movies_page(movie_time_flows:MovieFlows):
    movie_time_flows.navigate_to_all_movies()
    movie_time_flows.navigate_to_all_category()


@pytest.fixture
def chuck_flows(request_context):
    return ChuckApiFlows(request_context)




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

    if report.when == "call":
        # Attachments (only if the test failed)
        if report.failed:
            page = item.funcargs.get("page")

            if page:
                timestamp = time.strftime("%Y%m%d-%H%M%S")
                unique_id = str(uuid.uuid4())[:8]
                base_filename = f"{item.name}_{timestamp}_{unique_id}"

                # Attach screenshot
                screenshot_name = f"{CONFIG['SCREENSHOT_PREFIX']}_{base_filename}.png"
                screenshot_path = os.path.join(CONFIG['ALLURE_RESULTS_DIR'], screenshot_name)
                attach_screenshot(page, item.name, screenshot_path)

                # Attach trace
                trace_name = f"{CONFIG['TRACE_PREFIX']}_{item.name}_{timestamp}.zip"
                trace_path = os.path.join(CONFIG['ALLURE_RESULTS_DIR'], trace_name)
                attach_trace(page, item.name, trace_path)


@pytest.fixture
def chuck_web_flows(page):
    return ChuckWebFlows(page)


@pytest.fixture
def navigate_to_homepage(movie_time_flows:MovieFlows):
    movie_time_flows.navigate_to_homepage()