from playwright.sync_api import Page

class MovieTimeAllMoviesPage:
    def __init__(self,page:Page):
        self.header = page.locator("[data-test='title']")