from playwright.sync_api import Page
class MovieTimeLoginPage:
    def __init__(self,page:Page):
        self.email_address_field = page.locator("[data-testid='input-email']")
        self.password_field = page.locator("[data-testid='input-password']")
        self.log_in_button = page.locator("[data-testid='btn-submit-login']")
        self.log_out_button = page.locator("[data-testid='btn-logout']")
        self.actual_log_in_header = page.locator("[class='hero-t']")
        self.error_message = page.locator('[data-testid*="error"]')
