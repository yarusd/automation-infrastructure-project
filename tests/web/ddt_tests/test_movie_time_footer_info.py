import allure
import pytest
from extensions.web_verifications import WebVerify
from utils.common_ops import read_data_from_csv
from workflows.web.movie_time_flows import MovieFlows

# שימוש בנתיב ישיר כפי שעשית עד עכשיו
STATIC_FOOTER_DATA_PATH = r"data\ddt\footer_static_info.csv"

class TestFooterContent:

    @allure.title("Verify Static Footer Content")
    @allure.description("Validate that business info, address, and pricing are visible in the footer.")
    @pytest.mark.parametrize("data", read_data_from_csv(STATIC_FOOTER_DATA_PATH))
    def test_verify_footer_static_info(self, movie_time_flows: MovieFlows, navigate_to_homepage, data):
        # 1. שליפת המידע מה-CSV בדיוק כמו במבנה הקודם
        expected_text = data["InfoText"]

        # 2. ביצוע האימות בעזרת הפונקציה ב-Flows
        is_visible = movie_time_flows.verify_footer_static_content(expected_text)

        # 3. בדיקת התוצאה בעזרת WebVerify (במקום assert רגיל)
        WebVerify.is_true(is_visible, f"ERROR - Static content '{expected_text}' was not found in the footer")