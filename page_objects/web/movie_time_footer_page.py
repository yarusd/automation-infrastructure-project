from playwright.sync_api import Page

class MovieTimeFooterPage:
    def __init__(self,page:Page):
        self.Social_1 = page.locator("//footer//button[1]")
        self.Social_2 = page.locator("//footer//button[2]")
        self.Social_3 = page.locator("//footer//button[3]")
        self.Social_4 = page.locator("//footer//button[4]")
        self.login_link = page.locator("//span[text()='Login']")
        self.Register_link = page.locator("//span[text()='Register']")
        self.My_Orders_link = page.locator("//span[text()='My Orders']")
        self.Favorites_link = page.locator("//span[text()='Favorites']")
        self.Profile_Settings_link = page.locator("//span[text()='Profile Settings']")
        self.About_Us = page.locator("//span[text() = 'About Us']")
        self.Contact = page.locator("//span[text() = 'Contact']")
        self.Group_Bookings = page.locator("//span[text() = 'Accessibility']")
        self.Accessibility = page.locator("//span[text() = 'Gift Cards']")
        self.Gift_Cards = page.locator("//span[text() = 'Group Bookings']")
        self.address = page.locator("//div[span[text()='📍']]//span[2]")
        self.phon_number = page.locator("//div[span[text()='📞']]//span[2]")
        self.email = page.locator("//div[span[text()='✉️']]//span[2]")
        self.working_hours = page.locator("//div[span[text()='🕐']]//span[2]")
        self.standard_ticket = page.locator("//*[@id='root']/div/footer/div[2]/div/div[1]")
        self.Premium_ticket = page.locator("//*[@id='root']/div/footer/div[2]/div/div[2]")
        self.Back_Row_ticket = page.locator("//*[@id='root']/div/footer/div[2]/div/div[3]")
        self.Student_ticket = page.locator("//*[@id='root']/div/footer/div[2]/div/div[4]")
        self.Senior_ticket = page.locator("//*[@id='root']/div/footer/div[2]/div/div[5]")
        self.Child_ticket = page.locator("//*[@id='root']/div/footer/div[2]/div/div[6]")
        self.Family_Pack_ticket = page.locator("//*[@id='root']/div/footer/div[2]/div/div[7]")
        self.Privacy_Policy_link = page.locator("//span[text()='Privacy Policy']']")
        self.Terms_of_Use_link = page.locator("//span[text()='Terms of Use']")
        self.Cookie_Settings_link = page.locator("//span[text()='Cookie Settings']")
        self.Sitemap_link = page.locator("//span[text()='Sitemap']")



