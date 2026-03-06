from playwright.sync_api import Page
class MovieTimeNavigationMenu:
    def __init__(self,page:Page):
        self.movie_time_button = page.locator("[data-testid='logo']")
        self.home_button  = page.locator("[data-testid='nav-home']")
        self.all_movies_button  = page.locator("[data-testid='nav-movies']")
        self.login_button = page.locator("[data-testid='btn-login']")
        self.register_button = page.locator("[data-testid='btn-register']")
        self.menu_links = page.locator("nav.navbar a, nav.navbar button, [data-testid='nav-home']")
        self.page_header = page.locator("//h1")
        self.switch_mode_button = page.locator("[data-testid='theme-toggle']")
        self.expected_result = page.locator("[class='app light']")
