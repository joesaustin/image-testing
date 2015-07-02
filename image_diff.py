import ntpath, os
from PIL import Image
import subprocess as sub

class ImageComparison():
    def compare_images(self, directory, file_name, threshold = 0, file_type ='.png'):
        perceptualdiff_path =self.get_perperceptualdiff_path().rstrip()
        diff = ntpath.basename(file_name)+"-diff"
        diff_file = os.path.join(directory, 'screenshots', '%s.png' % diff)
        baseline = os.path.join(directory, 'screenshots', 'baseline', '%s.png' % file_name)
        screenshot = os.path.join(directory, 'screenshots', '%s.png' % file_name)
        num_of_pixels = self.get_num_pixels(baseline)
        
        if threshold == 0:
            threshold = (num_of_pixels *.05)
        
        cmd = '%s -threshold %s %s %s -output %s' % (perceptualdiff_path, str(threshold), 
                                                              baseline, screenshot, diff_file)
        process = sub.Popen(cmd, shell=True, stdout=sub.PIPE, stderr=sub.PIPE)
        output, _ = process.communicate()

        image_result = {"status": None,
                "msg": ''}
        
        #print process.returncode
        if process.returncode == 0:
            image_result['status'] = True
            image_result['msg'] = "All good"
            return image_result
        else:
            image_result['status'] = False
            image_result['msg'] = output
            return image_result
    
    def get_screenshot(self, driver, element, image_name, set_window =True):
        #set browser size width and height
        
        width = 1024
        height = 768
        #driver.set_window_size(width, height)
        
        # Measure the difference between the actual document width and the
        # desired viewport width so we can account for scrollbars:
        measured = driver.execute_script("return {width: document.body.clientWidth, height: document.body.clientHeight};")
        delta = width - measured['width']
        if set_window == True:
            driver.set_window_size(width + delta, height)
        
        location = element.location
        image_file= image_name+'.png'
        size = element.size
        driver.save_screenshot(image_file)
        
        #uses PIL library to open image in memory
        image = Image.open(image_file) 
        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']
        
        #define crop points and save new cropped image
        image = image.crop((left, top, right, bottom))
        image.save(image_file)
        return image_file
        
    def create_screenshot(self, directory, driver, element, image_name, mode = "screenshots", set_window = True):
        #create screenshot directory if it does not exits
        if mode == "baseline":
            screenshot_directory = directory+"/screenshots/baseline/"
        else:
            screenshot_directory = directory+"/screenshots/" 
            
        if not os.path.exists(screenshot_directory):
            os.makedirs(screenshot_directory)
        
        #move image file to baseline directory
        image_file = self.get_screenshot(driver, element, image_name, set_window)
        screenshot_image = screenshot_directory+image_file
        os.rename(image_file, screenshot_image)
        
    def get_perperceptualdiff_path(self):
        p = os.popen('which perceptualdiff')
        path =''
        while 1:
            line = p.readline()
            if not line:break
            path = line
        return path

    def get_num_pixels(self,filepath):
        width, height = Image.open(open(filepath)).size
        return (width*height)
