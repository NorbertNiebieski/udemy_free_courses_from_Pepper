import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
import random

import pepper_handling
import udemy_handling
import log


class WebBot:
    def __init__(self, udemy_login="", udemy_password="", pepper_login="", pepper_password="",
                 path_to_chrome_profile="", sleep_time=5, starting_file="main.py"):

        self.udemy_login = udemy_login
        self.udemy_password = udemy_password

        self.pepper_login = pepper_login
        self.pepper_password = pepper_password

        # set depends on speed of your internet connection
        self.__sleep_time = sleep_time

        # Some function can restart program - need known starting program
        self.starting_file = starting_file

        # cache setting and data
        self.cache_folder_path = "data\\"
        self.cache_owned_courses_file_name = "cached_owned_courses_information.txt"
        self.cache_owned_courses = dict()

        # stats
        self.number_of_link_looked = 0
        self.number_of_new_course = 0
        self.number_of_had_course = 0
        self.number_of_not_free_course = 0
        self.number_of_unrecognized_course = 0
        self.number_of_checkout_problem = 0

        # flags for logged accounts
        self.is_logged_to_pepper = False
        self.is_logged_to_udemy = False

        # web browser settings
        options = Options()

        options.add_argument("--disable-infobars")
        options.add_argument("start-maximized")
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--enable-javascript")

        # Path to your chrome profile
        if path_to_chrome_profile != "":
            options.add_argument("user-data-dir=" + path_to_chrome_profile)

        # options.add_argument("headless")
        # options.add_argument("--incognito")
        options.add_argument("use_subprocess=True")

        # setting browser preferences
        # pass the argument 1 to allow and 2 to block
        options.add_experimental_option("prefs", {
            # block notification
            "profile.default_content_setting_values.notifications": 2,
            # block third party cookies
            "profile.default_content_setting_values.cookies": 1,
            "profile.block_third_party_cookies": True,
            # turn on do not track preference
            "enable_do_not_track": True
        })

        # web browser experimental options
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        self.driver = uc.Chrome(options=options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    def printing_stats_udemy_courses(self):

        print("I looked at " + str(self.number_of_link_looked) + " course and I find:")
        if self.number_of_new_course > 0:
            print(" - " + str(self.number_of_new_course) + " new course, which i added to your account")
        if self.number_of_not_free_course > 0:
            print(" - " + str(self.number_of_not_free_course) + " paid course")
        if self.number_of_had_course > 0:
            print(" - " + str(self.number_of_had_course) + " course, which you had already")
        if self.number_of_unrecognized_course > 0:
            print(" - " + str(self.number_of_unrecognized_course) + " course i dont recognize")
        if self.number_of_checkout_problem > 0:
            print(" - " + str(self.number_of_checkout_problem) + " course i had a problem with checkout")

    def log_to_pepper_account(self):

        if self.is_logged_to_pepper:
            return True

        self.is_logged_to_pepper = pepper_handling.log_to_pepper_account(self, self.pepper_login, self.pepper_password)
        return self.is_logged_to_pepper

    def give_plus_pepper_promotion(self, pepper_promotion_url=""):
        if self.is_logged_to_pepper:
            return pepper_handling.give_plus_pepper_promotion(self, pepper_promotion_url)
        else:
            return False

    def find_udemy_promotions_on_pepper(self):
        return pepper_handling.find_udemy_promotions_on_pepper(self)

    def taking_links_to_udemy_from_pepper_promotion(self, promotion_link):
        return pepper_handling.taking_links_to_udemy_from_pepper_promotion(self, promotion_link)

    def log_to_udemy(self):

        if self.is_logged_to_udemy:
            return True
        else:
            self.is_logged_to_udemy = udemy_handling.log_to_udemy(self, self.udemy_login, self.udemy_password)
            return self.is_logged_to_udemy

    def buy_free_course(self, link, course_number=0, number_of_course=0):
        if self.is_logged_to_udemy:
            return udemy_handling.buy_free_course(self, link, course_number, number_of_course)
        else:
            log.log_and_print("warning", "You are not logged to udemy account, when trying to handle this link - " +
                              link)
            return 0

    def get_sleep_time(self):
        return self.__sleep_time + random.uniform(-self.__sleep_time / 3, self.__sleep_time / 2)

    def set_sleep_time(self, sleep_time):
        self.__sleep_time = sleep_time if sleep_time > 0 else 0
