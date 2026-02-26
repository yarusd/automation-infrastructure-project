from playwright.sync_api import Page

class MovieTimeHomePage:
    def __init__(self,page:Page):
        self.header = page.locator("[data-test='title']")
        self.actual_now_showing_icon = page.locator("[style^='position: absolute; t']")
        self.expected_now_showing_icon = page.locator("span[style='opacity: 0.6; font-size: 12px;']").first
        self.book_now_button = page.locator("[class='btn sec']")
        self.actual_booking_movie_error_message = page.locator("[class='alert err']")
        self.details_button = page.locator("[data-testid='details-btn-1']")
        self.movie_description = page.locator("[data-testid='movie-desc']")
        self.log_in_icon = page.locator("[data-testid='btn-login']")
        
