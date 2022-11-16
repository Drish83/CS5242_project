
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import pandas as pd
options = webdriver.ChromeOptions()
browser = webdriver.Chrome('../../chromedriver', options=options)

def is_ready(browser):
    return browser.execute_script(r"""
        return document.readyState === 'complete'
    """)

def concat_keyword(search_words):
    words = search_words.split()
    keywords = ""
    for i in range(len(words)):
        keywords += words[i]
        if i+1 < len(words):
            keywords += "+"
    return keywords

def get_search_links(page, keyword, name):
    browser.get("https://www.misstamchiak.com/page/%d/?s=%s" % (page,keyword))
    WebDriverWait(browser, 30).until(is_ready)
    main_content = browser.find_element(By.CLASS_NAME, "archive-posts-w")
    results = main_content.find_elements(By.CLASS_NAME, "entry-title")
    matching_results = []

    for result in results:
        links = result.find_elements(By.TAG_NAME, "a")
        link = links[0].get_attribute("href")
        link_text = links[0].text
        if name in link_text.lower():
            matching_results.append(link)

    return pd.DataFrame(matching_results, columns=['source_url'])
    # search_results_df.to_csv(search_result_links, index=False)


def crawl_data(page, keyword, name, result_df):
    df = get_search_links(page, keyword, name)
    matching_results = df['source_url']
    img_links = []
    for i in range(len(matching_results)):
        matching_result = matching_results[i]
        browser.get(matching_result)
        WebDriverWait(browser, 300).until(is_ready)
        main_content = browser.find_element(By.CLASS_NAME, "page-content")
        height = browser.execute_script("return document.body.scrollHeight")
        cur_height = 0
        while cur_height < height:
            cur_height += 500
            browser.execute_script("window.scrollTo(0,%d)" % cur_height)
            time.sleep(1)
        images = main_content.find_elements(By.TAG_NAME, "img")
        for img in images:
            src = img.get_attribute('src')
            # actual_url = src[src.find("http",5):]
            img_links.append([matching_result, src])
        result_df = result_df.append(img_links)
        print(result_df.head())
    print(df.shape[0])
    return result_df

categories = ["chicken rice", "char kway teow", "hokkien mee", "prawn noodle", "wanton mee", "laksa"]
for category in categories:
    search_results_df = pd.DataFrame(columns=['source_url', 'img_url'])
    for i in range(2):
        i += 1
        keyword = concat_keyword(category)
        search_results_df = crawl_data(i, keyword, category, search_results_df)
    search_results_df.to_csv("%s_links.csv" % category)
