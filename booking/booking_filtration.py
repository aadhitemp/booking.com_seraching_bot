from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BookingFiltration():
    def __init__ (self, driver:WebDriver): #..:WebDriver tells the type is Webdriver, gives acces to autocomplete, we need to import the library still...
        self.driver=driver
    
    def apply_star_rating(self, *star_values): #...* is used to give multiple arguments
        star_filtration_box = self.driver.find_element(By.CSS_SELECTOR, 'div[data-filters-group="class"]')
        star_child_elements = star_filtration_box.find_elements(By.CSS_SELECTOR, '*')

        for star_value in star_values:
            for star_element in star_child_elements: #instead of going through specific buttons like in the bookig.py, here we go through every single element and it's inner html
                if str(star_element.get_attribute('innerHTML')).strip() == f'{star_value} stars':
                    star_element.click()

    def sort_price_lowest_first(self):
        wait=WebDriverWait(self.driver, 15)
        dropdown=self.driver.find_element(By.CSS_SELECTOR, 'button[data-testid="sorters-dropdown-trigger"]')
        dropdown.click()
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'ad7c39949a')), "We didn't find the sort-button.")
        self.driver.find_element(By.CLASS_NAME, 'ad7c39949a').find_element(By.CSS_SELECTOR, 'button[data-id="price"]').click()
       
