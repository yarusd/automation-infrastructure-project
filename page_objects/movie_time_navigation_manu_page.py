from playwright.sync_api import Page
class MovieTimeNavigationMenu:
    def __init__(self,page:Page):
        self.movie_time_button = page.locator("[data-testid='logo']")
        self.home_button  = page.locator("[data-testid='nav-home']")
        self.all_movies_button  = page.locator("[data-testid='nav-movies']")
        self.theme_switch_button = page.locator("[data-testid='theme-toggle']")
        self.login_button = page.locator("[data-testid='theme-toggle']")
        self.register_button = page.locator("[data-testid='theme-toggle']")
        self.expected_toggle_icon = page.locator("//*[text()='🌙']")