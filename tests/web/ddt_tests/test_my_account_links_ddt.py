import allure
import pytest
from extensions.web_verifications import WebVerify
from utils.common_ops import read_data_from_csv
from workflows.web.movie_time_flows import MovieFlows

# הנתיב לקובץ הנתונים (בדיוק לפי מבנה התיקיות בתמונה שלך)
NAVIGATION_DATA_PATH = r"data\ddt\footer_data.csv"

class TestDDT:

    @allure.title("Navigation Links DDT")
    @allure.description("Validate navigation behavior using diverse data-driven inputs (from CSV).")
    @pytest.mark.parametrize("nav_data", read_data_from_csv(NAVIGATION_DATA_PATH))
    def test0_verify_navigation_links_with_vision(self, movie_time_flows: MovieFlows, navigate_to_homepage, nav_data):
        
        # 1. שולפים את שם הלינק מה-CSV (שים לב ל-LinkName עם אותיות גדולות בדיוק כמו בקובץ)
        link_name = nav_data["LinkName"]
        
        # 2. לחיצה דינמית על הלינק בעזרת הפונקציה שהוספת
        movie_time_flows.click_dynamic_link(link_name)
        
        # 3. אימות מול ה-AI בעזרת המילה המשתנה
        is_expected_page = movie_time_flows.verify_navigation_with_vision(expected_text=link_name)
        
        # 4. בדיקת התוצאה
        WebVerify.is_true(is_expected_page, f"ERROR - AI failed to find '{link_name}' prominently on the new page")