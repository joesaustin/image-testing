from selenium import webdriver
import image_compare, unittest, time, os

class TakeScreenshot(unittest.TestCase):
    
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.images = image_compare.ImageComparison()
        self.verification_errors = []
        self.css = {"yahoo_logo":"a[id='yucs-logo-ani']",
                    "mail_image":"i[id='nav-mail']",
                    "news_image":"i[id='nav-news']",
                    "sports_image":"i[id='nav-sports']"}
        
    def test_take_screenshot(self):
        self.driver.get("http://www.yahoo.com")

        directory = os.path.dirname(os.path.realpath(__file__))        
        for key, value in self.css.iteritems(): 
            element = self.driver.find_element_by_css_selector(value)
            self.images.create_screenshot(directory, self.driver, element, key, set_window = False, mode = "baseline")
            result = self.images.compare_images(directory,key, value[1])
            #try:
            #    self.assertEqual(True, result['status'], "%s image is off. %s" % (key, result['msg']))
            #except AssertionError, e:
            #    self.verification_errors.append(e)
                
    def tearDown(self):
        self.driver.quit()
        self.assertEquals([], self.verification_errors)        
        
if __name__ == "__main__":
    unittest.main()
