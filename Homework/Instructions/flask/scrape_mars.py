import pandas as pd
from bs4 import BeautifulSoup
from splinter import Browser
import re
import time

# 1. create a browser - you should only be doing this one per run. 
# 2. each time you visit a different url, you should have a time.sleep(3) line to allow the browser to load the HTML completely
# 3. after the wait, you can do the browser.html to get the HTML code
# 4. each new page = a new soup object -> if you click and visit another page, you should create a new soup object
# 5. one over-arching function that calls on subsequent functions to perform each scrape (each website). this function, should hold and return a dictionary that contains each piece of information (returned from each website)
# 6. close the browser after finishing

def mars_news(browser):
    
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(3)
    #set up first item selection
    
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # slider = soup.find("ul.item_list li.slide")
    try:
        slider_title = soup.find_all("div", class_="content_title")[1].text
        slider_p = soup.find("div", class_="article_teaser_body").text
    except AttributeError:
        return None, None
    return slider_title, slider_p

def mars_image(browser):
    url ='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(1)
    soup_image = browser.links.find_by_partial_text ('FULL IMAGE')
    soup_image.click()
    time.sleep(1)
    soup_info = browser.links.find_by_partial_text ('more info')
    soup_info.click()
    time.sleep(3)
    html = browser.html
    soup_weather = BeautifulSoup(html, 'html.parser')
    
    try: 
        mars_url = soup_weather.find("figure", class_="lede").find('a').find('img')['src']
    except AttributeError:
        return None
    full_url_img = f'https://www.jpl.nasa.gov{mars_url}'
    return full_url_img
                                 
def twitter_mars(browser):
    mars_weather = []                             
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    time.sleep(3)
    html=browser.html
    soup=BeautifulSoup(html, 'html.parser')
    
    try:                             
        all_tweets=soup.find_all("div", attrs={'data-testid': 'tweet'})
        for each_tweet in all_tweets:
            # print(each_tweet.get_text())
            mars_weather.append(each_tweet.get_text())
    except AttributeError:
        return None
    return mars_weather[0]

def mars_facts():
    try:
        table = pd.read_html('https://space-facts.com/mars/')[0]
    except BaseException:
        return None                       
    table.columns=["Description", "Value"]
    table.set_index("Description", inplace=True)
    return table.to_html(classes="table table-striped")

def mars_hemi(browser):
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    time.sleep(5)
    hemi_image =[]
    links = browser.find_by_css("a.product-item h3")
    for link in range(len(links)):
        hemi={}
        browser.find_by_css("a.product-item h3")[link].click()
        time.sleep(1)
        image_url = browser.links.find_by_text("Sample").first
        hemi["url"] = image_url["href"]
        hemi["title"] = browser.find_by_css("h2.title").text
        hemi_image.append(hemi)
        browser.back()
    return hemi_image

def scrape_all():
    executable_path = {"executable_path": "chromedriver.exe"}
    browser = Browser("chrome", **executable_path)
    slider_title, slider_p = mars_news(browser)                        
    full_url_img = mars_image(browser)                             
    mars_weather = twitter_mars(browser)                         
    facts = mars_facts()
    hemi_image = mars_hemi(browser)
    
    data={
        "news_title": slider_title,
        "news_paragraph": slider_p,
        "image": full_url_img,
        "weather": mars_weather,
        "facts": facts,
        "hemispheres": hemi_image
    }
    browser.quit()
    return data

if __name__ == "__main__":
    results=scrape_all()
    # for key, value in results.items():
    #     print(key)
    #     print(value)
    #     print('-------------------------------------')