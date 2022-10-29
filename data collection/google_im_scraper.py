
import requests
from io import BytesIO
import os
from PIL import Image
import time
import pandas as pd
import imghdr
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
import bs4 

from tqdm.auto import tqdm
## C:\Users\kradk\Documents\NUS\sem 4\CS5242 - NNs\project

driver_path = r"C:\Users\kradk\Documents\NUS\sem 4\CS5242 - NNs\project\chromedriver.exe"
driver = webdriver.Chrome(driver_path)


"""
barbecue stingray
https://www.google.com/search?q=barbecue+stingray&sxsrf=ALiCzsaLKOAeTwqCIfZvRXt6ui8iY6HTyQ:1665829932816&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjZhJuLhOL6AhWIwzgGHdqvDaoQ_AUoAXoECAEQAw&biw=960&bih=911&dpr=2
barbeque stingray
https://www.google.com/search?q=barbeque+stingray&tbm=isch&ved=2ahUKEwjx2_eMhOL6AhXTxKACHXnPCRAQ2-cCegQIABAA&oq=barbeque+stingray&gs_lcp=CgNpbWcQAzIFCAAQgAQyCQgAEIAEEAoQGFDhDli2D2CMFGgAcAB4AIABKYgBdZIBATOYAQCgAQGqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=MIxKY_GDGtOJg8UP-Z6ngAE&bih=911&biw=960

charsiew
https://www.google.com/search?q=char+siew&sxsrf=ALiCzsatkIOEIMKS_7Ok7jPGgwkfz1Th1g:1666502295423&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiX39fqzPX6AhVziuYKHQ_MB-cQ_AUoAXoECAIQAw&biw=1920&bih=969&dpr=2

satay
https://www.google.com/search?q=satay&sxsrf=ALiCzsYc4WIdcg8lJ22O156z5dpwTVinuw:1666506648240&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjRtaKG3fX6AhVf4XMBHYmmAi0Q_AUoAXoECAEQAw&biw=1920&bih=913&dpr=2

oyster omelette
https://www.google.com/search?q=oyster+omelette&sxsrf=ALiCzsZ7bImvUrn89Yc_cG8PDynl80degg:1666508899581&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjmyeW35fX6AhVCHbcAHWCyB98Q_AUoAXoECAIQAw&biw=1920&bih=913&dpr=2

fishhead curry
https://www.google.com/search?q=fish+head+curry&sxsrf=ALiCzsYVBmWwuXFLtROUckpHyeDYWAMneA:1666512082448&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjFpcCl8fX6AhUkRnwKHQEAAbkQ_AUoAXoECAEQAw&biw=1920&bih=913&dpr=2
"""

url = "https://www.google.com/search?q=fish+head+curry&sxsrf=ALiCzsYVBmWwuXFLtROUckpHyeDYWAMneA:1666512082448&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjFpcCl8fX6AhUkRnwKHQEAAbkQ_AUoAXoECAEQAw&biw=1920&bih=913&dpr=2"
data_path = Path('data')
class_name = 'fish_head_curry'
if not os.path.exists(data_path/class_name):
    (data_path/class_name).mkdir()

driver.get(url)

a = input('waiting. press any key to continue')
driver.execute_script("window.scrollTo(0,0);")

page_src  = driver.page_source
page_soup = bs4.BeautifulSoup(page_src, 'html.parser')

containers = page_soup.findAll('div', {'class': "isv-r PNCib MSM1fd BUooTd"})

print('number of images: ', len(containers))

meta_list = []
for i in tqdm(range(1, len(containers)+1)):
    
    if i % 25 == 0:
        continue
    meta_dict = dict()

    xPath = """//*[@id="islrg"]/div[1]/div[%s]"""%(i)
    try:
        previewImageXPath = """//*[@id="islrg"]/div[1]/div[%s]/a[1]/div[1]/img"""%(i)
        previewImageElement = driver.find_element(By.XPATH, previewImageXPath)
        previewImageURL = previewImageElement.get_attribute("src")
        
        driver.find_element(By.XPATH, xPath).click()
    except:
        continue
    
    time.sleep(1.0)
    """
    /html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img
    //*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img
    """
    # imageElement = driver.find_element(By.XPATH, """//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div[1]/a/img""")
    try:
        imageElement = driver.find_element(By.XPATH, """//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img""")
        imageURL= imageElement.get_attribute('src')
        response = requests.get(imageURL, timeout=5)
        if response.status_code==200:
            image = response.content
            # extension = imghdr.what(image)
            image=Image.open(BytesIO(image))
            if image.mode.lower() != 'rgb':
                image = image.convert('RGB')
            # image.show()
            image.save('temp.jpg')
            ext = imghdr.what('temp.jpg')

            image.save(data_path/class_name/f"{i}.{ext}")

            meta_dict['image_path'] = f'{class_name}/{i}.{ext}'
            meta_dict['image_url'] = imageURL
            meta_dict['image_class'] = class_name

            meta_list.append(meta_dict)

        # print("Downloaded element %s out of %s total. URL: %s" % (i, len_containers + 1, imageURL))
    except Exception as E:
        # print("Couldn't download an image %s, continuing downloading the next one"%(i))
        print(E)
        continue
    #//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div[1]/a/img
    #//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div[1]/a/img

pd.DataFrame.from_records(meta_list).to_csv(f'{class_name}.csv', index=False)
