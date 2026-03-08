import os
import allure
from playwright.sync_api import Page
from extensions.ui_actions import UIActions
from utils.common_ops import extract_digits_from_text
from google import genai
from google.genai import types

from page_objects.web.movie_time_register_page import MovieTimeRegisterPage
from page_objects.web.movie_time_all_movie_page import MovieTimeAllMoviesPage
from page_objects.web.movie_time_home_page import MovieTimeHomePage
from page_objects.web.movie_time_login_page import MovieTimeLoginPage
from page_objects.web.movie_time_movie_page import MovieTimeMoviePage
from page_objects.web.movie_time_navigation_menu_page import MovieTimeNavigationMenu


class MovieFlows:
    def __init__(self,page:Page):
        self.page = page
        self.login = MovieTimeLoginPage(page)
        self.home = MovieTimeHomePage(page)
        self.all_movies = MovieTimeAllMoviesPage(page)
        self.movie_page = MovieTimeMoviePage(page)
        self.navigation_manu = MovieTimeNavigationMenu(page)
        self.register = MovieTimeRegisterPage(page)

    @allure.step("Get actual now showing movies count")
    def get_actual_now_showing_icons_count(self)->int:
        return  self.home.actual_now_showing_icon.count()

    @allure.step("Get expected now showing movies count")   
    def get_expected_now_showing_icons__count(self)->int:
        return extract_digits_from_text(UIActions.get_text(self.home.expected_now_showing_icon))

    @allure.step("Get error message")   
    def get_error_booking_process_message(self)->str:
        UIActions.click(self.home.book_now_button)
        return self.home.actual_booking_movie_error_message

    @allure.step("Click on details button")
    def click_on_details_button(self) -> None:
        UIActions.click(self.home.details_button)

    @allure.step("Get movie description")
    def get_movie_description(self) -> str:
        return UIActions.get_text(self.movie_page.movie_description)

    @allure.step("Sign in")
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

    
    @allure.step("Navigate to homepage")
    def navigate_to_homepage(self) -> None:
        UIActions.click(self.navigation_manu.home_button)

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
    def click_and_get_actual_page_header(self, button_name: str) -> str:

        buttons = {
            "home": self.navigation_manu.home_button,
            "all movies": self.navigation_manu.all_movies_button,
            "login": self.navigation_manu.login_button,
            "register": self.navigation_manu.register_button
        }

        target = buttons[button_name.lower()]
        target.click()

        self.navigation_manu.page_header.wait_for(state="visible") 
        return self.navigation_manu.page_header.inner_text()

    @allure.step("Click on Theme Toggle Button")
    def click_on_Theme_Toggle(self) -> None:
        UIActions.click(self.navigation_manu.switch_mode_button)


    @allure.step("Verify theme mode with vision")
    def verify_theme_with_vision(self, expected_mode: str) -> bool:
        self.page.wait_for_timeout(1000)
        client = genai.Client(api_key=os.getenv("MY_API_KEY"))
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
    


    


  
  
    


            

        
      
        


