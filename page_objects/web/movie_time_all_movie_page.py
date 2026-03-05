from playwright.sync_api import Page

class MovieTimeAllMoviesPage:

    def __init__(self,page:Page):
        self.all_movies_header = page.locator("[data-testid='nav-movies']")
        self.movie_genre_button = page.locator("//div[@class='pills mb24']/button")
        self.movie_title = page.locator("[class='mtitle']")
        self.movie_search_bar = page.locator("[data-testid='search-input']")
        self.search_button = page.locator("[data-testid='search-btn']")
        self.empty_search_results = page.locator("//div[@class='emp']/h3")
        self.sorting_selector = page.locator("[data-testid='sort-select']")
        self.movie_rating = page.locator("//div[@class='mmeta']/span[1]")
        self.movie_year = page.locator("//div[@class='mmeta']/span[3]")


