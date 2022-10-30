from selenium import webdriver
import time
import os
import requests
import io
from PIL import Image

class GoogleImageScraper():
    def __init__(self, webdriver_path, image_path, search_key, number_of_images):
        image_path = os.path.join(image_path)
        driver = webdriver.Chrome(webdriver_path)
        self.driver = driver
        self.search_key = search_key
        self.number_of_images = number_of_images
        self.webdriver_path = webdriver_path
        self.image_path = image_path
        self.url = "https://www.google.com/search?q=%s&source=lnms&tbm=isch&sa=X&ved=2ahUKEwie44_AnqLpAhUhBWMBHUFGD90Q_AUoAXoECBUQAw&biw=1920&bih=947"%(search_key)
    
    def find_image_urls(self):
        print("[INFO] Gathering image links")
        image_urls=[]
        count = 0
        missed_count = 0
        self.driver.get(self.url)
        time.sleep(3)
        indx = 1
        while self.number_of_images > count:
            imgurl = self.driver.find_element_by_xpath('//*[@id="islrg"]/div[1]/div[%s]/a[1]/div[1]/img'%(str(indx)))
            imgurl.click()
                #select image from the popup
            time.sleep(1)
            class_names = ["n3VNCb"]
            images = [self.driver.find_elements_by_class_name(class_name) for class_name in class_names if len(self.driver.find_elements_by_class_name(class_name)) != 0 ][0]
            for image in images:
               #only download images that starts with http
                src_link = image.get_attribute("src")
                if(("http" in  src_link) and (not "encrypted" in src_link)):
                    print(f"[INFO] {self.search_key} \t #{count} \t {src_link}")
                    image_urls.append(src_link)
                    count +=1
            try:
                #scroll page to load next image
                if(count%3==0):
                    self.driver.execute_script("window.scrollTo(0, "+str(indx*60)+");")
                element = self.driver.find_element_by_class_name("mye4qd")
                element.click()
                time.sleep(3)
            except Exception:
                time.sleep(1)
            indx += 1
        self.driver.quit()
        return image_urls

    def save_images(self,image_urls, keep_filenames):
        print("Saving image")
        new=[]
        for indx,image_url in enumerate(image_urls):
                search_string = ''.join(e for e in self.search_key if e.isalnum())
                image = requests.get(image_url,timeout=5)
                if image.status_code == 200:
                    with Image.open(io.BytesIO(image.content)) as image_from_web:
                        try:
                            filename = "%s%s.%s"%(search_string,str(indx),image_from_web.format.lower())
                            new.append(filename)
                            image_path = os.path.join(self.image_path, filename)
                            image_from_web.save(image_path)
                        except OSError:
                            rgb_im = image_from_web.convert('RGB')
                            rgb_im.save(image_path)
                        image_from_web.close()
        return new
        