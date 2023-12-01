from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By



class BookingReport:
    def __init__(self, boxes_section_element:WebElement):
        self.boxes_section_element = boxes_section_element
        self.deal_boxes=self.pull_deal_boxes()

    def pull_deal_boxes(self):
        return self.boxes_section_element.find_elements(
                  By.CSS_SELECTOR,
                 'div[data-testid="property-card-container"]')
    
    def pull_deal_box_attributes(self):
        collection=[]
        
        for deal_box in self.deal_boxes:
            hotel_name=deal_box.find_element(By.CSS_SELECTOR, 'div[data-testid="title"]').get_attribute('innerHTML').strip()
            hotel_price =deal_box.find_element(By.CSS_SELECTOR, 'span[data-testid="price-and-discounted-price"]').get_attribute('innerHTML').strip()
            try:
                hotel_score=deal_box.find_element(By.CSS_SELECTOR, '.a3b8729ab1.d86cee9b25').get_attribute('innerHTML').strip()
            except:
                hotel_score="N/A"
            collection.append([hotel_name, hotel_price, hotel_score])
        
        return collection
            