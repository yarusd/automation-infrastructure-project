import pytest
from pytest import FixtureRequest
from playwright.sync_api import Playwright

from data.api.chuck_api_data import *
from data.web.movie_time_data import *
from utils.common_ops import load_config
from utils.fixture_helpers import get_browser
from workflows.api.chuck_api_flows import ChuckApiFlows
from workflows.web.movie_time_flows import MovieFlows

# Load the configuration
CONFIG = load_config()     

@pytest.fixture(scope="class")
def page(playwright: Playwright, request:FixtureRequest):
    browser = get_browser(playwright,CONFIG["BROWSER_TYPE"].lower())
    context = browser.new_context(no_viewport=True)        
    page = context.new_page()
    page.goto(movie_time_URL)
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
def chuck_flows(request_context):
    return ChuckApiFlows(request_context)

