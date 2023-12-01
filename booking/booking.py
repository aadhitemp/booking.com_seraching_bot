from selenium import webdriver
from booking.booking_filtration import BookingFiltration
# import os
# from time import sleep
import booking.constants as const
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from booking.booking_report import BookingReport

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from prettytable import PrettyTable
from os import chdir, getcwd
from subprocess import Popen


class Booking(webdriver.Chrome): 
    def __init__(self, teardown=False, use_cache=False): 
        self.teardown=teardown
        options=Options()
        if use_cache:
            options.add_experimental_option("debuggerAddress", "localhost:9014")
            self.start_chrome()
        else: 
            options.add_experimental_option('detach', not teardown)
        super(Booking, self).__init__(options=options)
        self.implicitly_wait(15)
        self.maximize_window()
        self.wait=WebDriverWait(self, 15, 1)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:            
            self.quit()                 

    #  Starts chrome in debug mode with current user settings
    def start_chrome(self, path=const.PATH_TO_CHROME): ##WORKS
        chdir(path)
        try:
            Popen(["chrome.exe", "-remote-debugging-port=9014"]) #--user-data-dir="%LOCALAPPDATA%\Google\Chrome\User Data"  this argument doesn't work, so didn't put it  
            # subprocess.run() waits for process, this stalls the program or something, the program doesn't load the page when using .run(), subprocess.Popen() instead
            # subprocess.run("chrome.exe -remote-debugging-port=9014") # sytax like Popen also works ([...,...])
        except:
            print("Counldn't find chrome.exe in the current path.")
            print(getcwd())
            self.start_chrome(input("Input path to chrome.exe:"))

    def land_first_page(self): ##WORKS
        self.get(const.BASE_URL)
        print(f"Opening: {const.BASE_URL}")
        try:
            self.find_element(
                 By.CSS_SELECTOR,
                 'button[aria-label="Dismiss sign-in info."]'
                 ).click()
            self.dimiss_google_sign_in()
        except:
            print("Didn't ask for sign in.")

    def dimiss_google_sign_in(self): ##WORKS
        self.implicitly_wait(3)
        try:
            iframe = self.find_element(By.CSS_SELECTOR, '#credential_picker_container > iframe')
            self.switch_to.frame(iframe)
            self.find_element(By.ID, 'close').click()
            self.switch_to.default_content()
        except:
            self.switch_to.default_content()
        self.implicitly_wait(15)

    def change_currency(self, currency='USD'): ##Works
        self.dimiss_google_sign_in()
        currency_element=self.find_element(
            By.CSS_SELECTOR, 
            'button[data-testid="header-currency-picker-trigger"]')
        currency_element.click()
        currencies=self.find_elements(By.CSS_SELECTOR, 'button[data-testid="selection-item"]')
        for c in currencies:
            if (c.find_element(By.CLASS_NAME, 'ea1163d21f').text==f'{currency}'):
                c.click()
                print(f"Chaning currency to {currency}")
                break
    
    def select_place_to_go(self, place_to_go): ##Works
        search_field=self.find_element(By.ID, ':re:')
        action = ActionChains(self)
        search_field.clear()
        search_field.click()
        action.key_down(Keys.CONTROL).send_keys('A').key_up(Keys.CONTROL).perform()
        search_field.send_keys(Keys.BACK_SPACE, place_to_go)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
        suggestion_visible=EC.staleness_of(self.find_element(By.ID, 'group-0-heading'))
        self.wait.until(suggestion_visible)
        try:
            search_id = self.find_element(By.ID, 'autocomplete-result-0')
            search_id.click()
            print(f"Selected location as {place_to_go}")
        except:
            print("Couldn't select location.")
        
    def select_dates(self, check_in_date, check_out_date): ##Works
        date_picker=self.find_element(By.CSS_SELECTOR, 'button[data-testid="date-display-field-start"]')
        date_picker.click() #This has a tendency to not register... so the following lines of code...
        try:
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="searchbox-datepicker-calendar"]')),"Could not find the calendar.")
        except:
            date_picker=self.find_element(By.CSS_SELECTOR, 'button[data-testid="date-display-field-end"]')
            date_picker.click()
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="searchbox-datepicker-calendar"]')),"Could not find the calendar.")
        self.find_element(
            By.CSS_SELECTOR,
            f'span[data-date="{check_in_date}"]'
            ).click()        
        print(f"Selected check-in date as: {check_in_date}")

        self.find_element(
            By.CSS_SELECTOR, 
            f'span[data-date="{check_out_date}"]'
            ).click()        
        print(f"Selected check-out date as: {check_out_date}")

    def select_count(self, adult=1, rooms=1): ##Works
        self.find_element(
            By.CSS_SELECTOR,
              'button[data-testid="occupancy-config"]').click()
        selection_divs=self.find_elements(By.CLASS_NAME, 'a7a72174b8')
        for div in selection_divs:
            if div.find_element(By.CLASS_NAME, 'a984a491d9').text=='Adults':
                minus_button=div.find_element(By.CLASS_NAME, 'e91c91fa93')
                plus_button=div.find_element(By.CLASS_NAME, 'f4d78af12a')
                elem=div.find_element(By.CLASS_NAME, 'd723d73d5f')      # element.get_attribute can also be used
                while(int(elem.text) < adult):                          # Clicking the correct number of times, instead of checking and clicking everytime may be a better way to do this.
                    plus_button.click()                                 # It may also be a good idea to make as a function : redundant code
                while(int(elem.text) > adult):
                    minus_button.click()
                print(f"Set Adult count to: {adult}")
            elif div.find_element(By.CLASS_NAME, 'a984a491d9').text=='Rooms':
                minus_button=div.find_element(By.CLASS_NAME, 'e91c91fa93')
                plus_button=div.find_element(By.CLASS_NAME, 'f4d78af12a')
                elem=div.find_element(By.CLASS_NAME, 'd723d73d5f')
                while(int(elem.text) < rooms):
                    plus_button.click()
                while(int(elem.text) > rooms):
                    minus_button.click()
                print(f"Set room count to: {rooms}")
        
    def click_search(self): #Works
        self.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        print("Searching...")

    def apply_filtration(self):
       filtration = BookingFiltration(driver=self)
       filtration.apply_star_rating(3,4,5)
       print("Filtering by star rating...")
       filtration.sort_price_lowest_first()
       print("Sorting by lowest price first...\n\n")

    def report_results(self):
        hotel_boxes=self.find_element(By.CLASS_NAME, "bcbf33c5c3")
        self.implicitly_wait(0)
        report = BookingReport(hotel_boxes)
        table=PrettyTable(field_names=["Name", "Price", "Score"])
        table.add_rows(report.pull_deal_box_attributes())
        self.implicitly_wait(15)
        print(table)
      
        

# # Explicit waiting
# WebDriverWait(driver, 30).until(
#     EC.text_to_be_present_in_element(
#         (By.CLASS_NAME, 'show'),# Element filtration
#         'Your username is invalid!'# The expected text
#     )
# )

