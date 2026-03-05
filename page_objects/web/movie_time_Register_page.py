from playwright.sync_api import Page
class MovieTimeRegisterPage:
    def __init__(self,page:Page):
        self.Register_header = page.locator("[class='authtitle']")