from playwright.sync_api import Page

class MovieTimeMoviePage:
    def __init__(self,page:Page):
        self.movie_description = page.locator("[data-testid='movie-desc']")
        