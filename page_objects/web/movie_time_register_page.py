from playwright.sync_api import Page

class MovieTimeRegisterPage:
    def __init__(self,page:Page):
        self.register_header = page.locator("[class='authtitle']")
        self.full_name_field = page.locator("[data-testid='input-name']")
        self.email_field = page.locator("[data-testid='input-email']")
        self.password_field = page.locator("[data-testid='input-password']")
        self.confirm_password_field = page.locator("[data-testid='input-confirm']")
        self.creat_account_button = page.locator("[data-testid='btn-submit-register']")
        self.error_message = page.locator("[class='ferr']")
        self.login_here_button = page.locator("[data-testid='link-login']")