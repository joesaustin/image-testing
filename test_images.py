from selenium import webdriver
import image_diff, unittest, time

class TakeScreenshot(unittest.TestCase):
    
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.images = image_diff.ImageComparison()
        self.css = {"yahoo_logo":"a[id='yucs-logo-ani']",
                    "mail_image":"i[id='nav-mail']",
                    "news_image":"i[id='nav-news']",
                    "sports_image":"i[id='nav-sports']"}
        
    def test_take_screenshot(self):
        self.driver.get("http://www.yahoo.com")
        
        for key, value in self.css.iteritems(): 
            element = self.driver.find_element_by_css_selector(value)
            self.images.create_screenshot(self.driver, element, key, "baseline")
            self.images.compare_images(key)
        
    def tearDown(self):
        self.driver.quit()        
        
if __name__ == "__main__":
    unittest.main()
