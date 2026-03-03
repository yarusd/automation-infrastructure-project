from playwright.sync_api import Page
class ChuckWebPage:
    def __init__(self,page:Page):
        self.page = page
        self.web_joke_value = page.locator("[id='joke_value']")