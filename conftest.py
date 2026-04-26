import os
import allure
import pytest
import time
import uuid
import sqlite3
import requests
from tenacity import *
from appium import webdriver
from dotenv import load_dotenv
from utils.common_ops import load_config
from pytest import FixtureRequest
from data.web.movie_time_data import *
from data.api.movie_api_data import *
from playwright.sync_api import Page, Playwright
from workflows.api.movie_api_flows import MovieApiFlows
from workflows.web.movie_time_flows import MovieFlows
from utils.fixture_helpers import *

load_dotenv()
CONFIG = load_config()     


@pytest.fixture(scope = "class")
def page(playwright: Playwright, request:FixtureRequest):
    browser = get_browser(playwright,CONFIG["BROWSER_TYPE"].lower())
    context = browser.new_context(no_viewport=True)    
    context.tracing.start(screenshots=True, snapshots=True, sources=True)    
    page = context.new_page()
    page._tracing_active = True
    yield page    
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
        requests.get(f"{MOVIE_API_URL}/{HEALTH_URL}", timeout=2).raise_for_status()
    try:
        attempt()
        print("--- ✅ API is Awake! ---")
    except:
        print("--- ⚠️ Trying again ---")
        
    
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
def movie_flows(movie_context, db_connection):
    return MovieApiFlows(movie_context, db_connection)

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
def db_connection():
    db = sqlite3.connect(CONFIG["DB_PATH"])
    yield db
    db.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
       
        page = item.funcargs.get("page")
        if page and getattr(page, "_tracing_active", False):
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            unique_id = str(uuid.uuid4())[:8]
            base_filename = f"{item.name}_{timestamp}_{unique_id}"

            screenshot_path = os.path.join(CONFIG['ALLURE_RESULTS_DIR'], f"{CONFIG['SCREENSHOT_PREFIX']}_{base_filename}.png")
            attach_screenshot(page, item.name, screenshot_path)

            trace_name = f"{CONFIG['TRACE_PREFIX']}_{item.name}_{timestamp}.zip"
            trace_path = os.path.join(CONFIG['ALLURE_RESULTS_DIR'], trace_name)
            try:
                attach_trace(page, item.name, trace_path)
                page._tracing_active = False 
            except Exception as e:
                print(f"Failed to stop/attach trace: {e}")

