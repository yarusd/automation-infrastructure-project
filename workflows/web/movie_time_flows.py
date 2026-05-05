<<<<<<< Updated upstream
=======
import os
import allure
from playwright.sync_api import Page
from extensions.ui_actions import UIActions
from page_objects.web.movie_time_footer_page import MovieTimeFooterPage
from utils.common_ops import extract_digits_from_text
from google import genai
from google.genai import types
import os
import allure
from google import genai
from google.genai import types
import time
from google.genai.errors import ServerError
>>>>>>> Stashed changes
import re

import allure
from playwright.sync_api import Locator, Page
from data.web.movie_time_data import *
from extensions.ui_actions import UIActions
from extensions.web_verifications import WebVerify
from page_objects.web.movie_time_Register_page import MovieTimeRegisterPage
from page_objects.web.movie_time_all_movie_page import MovieTimeAllMoviesPage
from page_objects.web.movie_time_home_page import MovieTimeHomePage
from page_objects.web.movie_time_login_page import MovieTimeLoginPage
from page_objects.web.movie_time_movie_page import MovieTimeMoviePage
from page_objects.web.movie_time_navigation_manu_page import MovieTimeNavigationMenu
from utils.common_ops import extract_digits_from_text
from google import genai
from google.genai import types
from page_objects.web.movie_time_navigation_menu_page import MovieTimeNavigationMenu


class MovieFlows:
    def __init__(self,page:Page):
        self.page = page
        self.login = MovieTimeLoginPage(page)
        self.home = MovieTimeHomePage(page)
        self.all_movies = MovieTimeAllMoviesPage(page)
        self.movie_page = MovieTimeMoviePage(page)
        self.navigation_manu = MovieTimeNavigationMenu(page)
<<<<<<< Updated upstream
=======
        self.register = MovieTimeRegisterPage(page)
        self.footer = MovieTimeFooterPage(page)
>>>>>>> Stashed changes

    @allure.step("Sign in:")
    def get_actual_now_showing_icons_count(self)->int:
        return  self.home.actual_now_showing_icon.count()
    
    def get_expected_now_showing_icons__count(self)->int:
        return extract_digits_from_text(UIActions.get_text(self.home.expected_now_showing_icon))
    
    def get_error_booking_process_message(self)->str:
        UIActions.click(self.home.book_now_button)
        return self.home.actual_booking_movie_error_message

    def click_on_details_button(self) -> None:
        UIActions.click(self.home.details_button)

    def get_movie_description(self) -> str:
        return UIActions.get_text(self.movie_page.movie_description)


    def sign_in(self,user_name:str,password:str)->None:
        UIActions.click(self.home.log_in_icon)
        UIActions.update_text(self.login.email_address_field,user_name)
        UIActions.update_text(self.login.password_field,password)
        UIActions.click(self.login.log_in_button)


    @allure.step("Navigte to:")
    def navigate_to(self,url:str)->None:
        UIActions.navigate_to(self.page,url)
   
    @allure.step("Get Home Header")
    def get_home_header(self)->str:
        return UIActions.get_text(self.home.header)
    

    @allure.step("Navigate to all Movies:")
    def navigate_to_all_movies(self) -> None:
        UIActions.force_click(self.all_movies.all_movies_header)

    @allure.step("Navigate to all section")
    def navigate_to_all_category(self) -> None:
        UIActions.force_click(self.all_movies.movie_genre_button.first)


    @allure.step("Enter keyword to search bar")
    def search_a_movie_name(self,keyword:str) -> None:
        UIActions.force_click(self.all_movies.all_movies_header)     
        UIActions.update_text(self.all_movies.movie_search_bar,keyword)
        UIActions.click(self.all_movies.search_button)


    @allure.step("Choose sorting method")
    def choose_sorting_method(self, option:str) -> None:
         self.all_movies.sorting_selector.select_option(option)
   
   
    @allure.step("Get rating list")
    def get_rating_list(self) -> list:
        rating_list = UIActions.get_text_list(self.all_movies.movie_rating)
        scores = []
        for score in rating_list:
            if score != "Unrated":
                score = float(score.replace("★",""))
                scores.append(score)
        return(scores)

    @allure.step("Get title list")
    def get_title_list_text(self) -> list:
        title_list = UIActions.get_text_list(self.all_movies.movie_title)
        return title_list


    @allure.step("Get year list") 
    def get_year_list(self) -> list:
        year_list = UIActions.get_text_list(self.all_movies.movie_year)
        return year_list

    @allure.step("Get top movie")  
    def get_top_movie(self,movie_list:list) -> str:
        return movie_list[0]

    @allure.step("Filter by genre name and count movies")
    def get_movie_count_by_genre_name(self, genre_name: str) -> int:
        target_genre = self.all_movies.movie_genre_button.filter(has_text=genre_name)
        UIActions.force_click(target_genre)
        return UIActions.count(self.all_movies.movie_title)
    
    @allure.step("Get Navigation header text")
    def get_page_header(self, button_name: str) -> str:
        if button_name.lower() == 'theme':
            target = self.navigation.theme_switch_button
        else:
            WebVerify.contain_text(self.login.error_message,LOGIN_ERROR_MESSAGE)

    
    @allure.step("Click on Theme Toggle Button")
    def click_on_Theme_Toggle(self) -> None:
        UIActions.click(self.navigation_manu.switch_mode_button)


    @allure.step("Verify theme mode with vision")
    def verify_theme_with_vision(self, expected_mode: str) -> bool:
        self.page.wait_for_timeout(1000)
        client = genai.Client(api_key=GEMENI_API_KEY)
        screenshot_bytes = self.page.screenshot(type="png")
        prompt = (
            "Examine the screenshot. Is the main background color of the website white or very light? "
            "Respond with 'Yes' or 'No' only."
        )
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                prompt,
                types.Part.from_bytes(
                    data=screenshot_bytes,
                    mime_type="image/png"
                )
            ]
        )
        result = response.text.strip().lower()
        print(f"\nThe result from AI: {result}")
        return "yes" in result
  

    
            

            



        

   
    

    @allure.step("Verify navigation by checking if '{expected_text}' appears prominently")
    def verify_navigation_with_vision(self, expected_text: str) -> bool:
        self.page.wait_for_timeout(1000)
        # --- שלב 1: חיפוש מהיר בעזרת Playwright ---
        # הפונקציה get_by_text עם exact=False מתעלמת אוטומטית מאותיות גדולות/קטנות
        try:
            element = self.page.get_by_text(expected_text, exact=False)
            if element.first.is_visible(timeout=3000):
                print(f"\n[Fast Verification] Playwright found text '{expected_text}' on the page")
                return True
        except:
            pass # אם פליירייט לא מצא, עוברים ל-AI שיפעיל שיקול דעת ויזואלי
        print(f"\n[Fallback] Switching to AI Vision to find '{expected_text}'...")
        # --- שלב 2: גיבוי AI עם הנחיה מדויקת לחיפוש הטקסט ---
        try:
            client = genai.Client(api_key=os.getenv("MY_API_KEY"))
            screenshot_bytes = self.page.screenshot(type="png")
            
            # הפרומפט עודכן בדיוק לדרישה שלך: חפש את הטקסט, תתעלם מרישיות, תחזיר כן/לא
            prompt = (
                f"Look at this screenshot of a web page. "
                f"Your task is to determine if the exact text '{expected_text}' appears anywhere in this image. "
                f"You must exercise visual judgment, but you should be case-insensitive "
                f"(treat uppercase and lowercase letters as the same). "
                f"If you see this text on the page, respond with exactly 'Yes'. "
                f"If this text is NOT present on the page, respond with exactly 'No'."
            )
            
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    prompt,
                    types.Part.from_bytes(data=screenshot_bytes, mime_type="image/png")
                ]
            )
            
            result = response.text.strip().lower()
            print(f"The AI vision result for finding '{expected_text}': {result}")
            
            time.sleep(15) # הגנה מעומסים (שגיאת 503 שקיבלת קודם)
            return "yes" in result
            
        except Exception as e:
            print(f"AI Verification failed due to error: {e}")
            return False



    @allure.step("Click on Login_Link Button")
    def click_on_login_link(self) -> None:
        UIActions.click(self.footer.login_link)


    @allure.step("Click on dynamic link: '{link_name}'")
    def click_dynamic_link(self, link_name: str):
        # בדיקה אם זה אחד מכפתורי הסושיאל (לפי השם שנתנו ב-CSV)
        if "Social_" in link_name:
            # שולפים את המספר מתוך השם (למשל Social_1 ייתן לנו 1)
            index = link_name.split("_")[1]
            # לוחצים על הכפתור במיקום המתאים בתוך הפוטר
            self.page.locator(f"//footer//button[{index}]").click()
        else:
            # לכל שאר הלינקים שיש להם טקסט (Login, About Us וכו')
            self.page.locator(f"text='{link_name}'").first.click()
  
    
    



    @allure.step("Verify footer static content: '{expected_text}'")
    def verify_footer_static_content(self, expected_text: str) -> bool:
        clean_text = expected_text.strip()
        
        # --- שלב 1: ניסיון קלאסי ומהיר עם Playwright ---
        try:
            self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            self.page.wait_for_timeout(1000) 
            
            elements = self.page.get_by_text(clean_text, exact=False)
            
            # מחכים עד 4 שניות. אם זה לא שם, חבל על הזמן, נעבור ל-AI
            elements.first.wait_for(state="attached", timeout=4000)
            
            for i in range(elements.count() - 1, -1, -1):
                el = elements.nth(i)
                try:
                    el.scroll_into_view_if_needed(timeout=1000)
                except:
                    pass
                
                if el.is_visible():
                    return True
                    
        except Exception as e:
            # תפסנו את השגיאה (ה-Timeout) של פליירייט - לא מכשילים את הטסט עדיין!
            print(f"\n[Fallback] Playwright couldn't find '{clean_text}', switching to AI Vision...")
            pass # ממשיכים הלאה לשלב 2
            
        # --- שלב 2: תותחים כבדים - אימות AI כגיבוי ---
        # נשתמש בפונקציית ה-Vision שכבר קיימת לך באותו קלאס
        return self.verify_navigation_with_vision(expected_text=clean_text)
    
            

        
      
        


