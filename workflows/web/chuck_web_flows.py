
import allure
from playwright.sync_api import Page
from extensions.ui_actions import UIActions
from page_objects.api_web.chuck_web_page import ChuckWebPage


class ChuckWebFlows:

    def __init__(self,page:Page):
        self.web_chuck = ChuckWebPage(page)

    @allure.step("Navigate to")
    def navigate_to_web(self,url):
        self.web_chuck.page.goto(url)
    
    @allure.step("Get web joke value")
    def get_web_joke_value(self):
        web_joke_value = UIActions.get_text(self.web_chuck.web_joke_value)
        return web_joke_value
    