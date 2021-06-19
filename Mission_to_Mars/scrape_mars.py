# Import Python Modules
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

data = {}


def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Go to the NASA Mars News Site 
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    # Create a Beautiful Soup object
    soup = bs(browser.html, 'lxml')

    news_title = soup.find_all('div', class_ = 'content_title')
    news_articles = []
    for news in news_title:
        if (news.a):
            if (news.a.text):
                news_articles.append(news.a.text)

    # Print paragraph for the latest news article
    news_story = soup.find_all('div', class_ = 'article_teaser_body')
    news_paragraph = []
    for paragraph in news_story:
        if (paragraph.text):
            news_paragraph.append(paragraph.text)

    # Create variables for our latest news article and paragraph
    first_article = news_articles[0]
    news_p = news_paragraph[0]
    data["news_title"] = first_article
    data["news_paragraph"] = news_p

    # Visit the url for JPL Featured Space Image
    url_2 = 'https://www.jpl.nasa.gov/images?search=&category=Mars'
    browser.visit(url_2)

    # Create a Beautiful Soup object
    soup2 = bs(browser.html, 'lxml')

    # Find and append the links(href) for each image featured on the page
    article_images = soup2.find_all('a', class_="group cursor-pointer block")
    image_links = []
    for image in article_images:
        image_links.append(image['href'])

    # Scrape through the first href and find the full sized image url
    soup2 = bs(browser.html, 'lxml')

    domain_url = 'https://' + browser.url.replace('http://','').replace('https://','').split('/', 1)[0]

    browser.visit(domain_url + image_links[0]) 
    soup3 = bs(browser.html, 'lxml')
    img_url = soup3.find_all('div', class_ = "lg:w-auto w-full")
    img_href = []
    for i in img_url:
        if (i.a):
            if (i.a['href']):
                img_href.append(i.a['href'])
                
    featured_image_url = img_href[0]

    data["featured_image"] = featured_image_url

    # Visit the Mars Facts webpage
    url_3 = 'https://space-facts.com/mars/'
    browser.visit(url_3)

    # Create a Beautiful Soup object
    soup3 = bs(browser.html, 'lxml')

    # Scrape the table containing facts about the planet including Diameter, Mass, etc.
    mars_facts = pd.read_html(browser.html)
    table_df = mars_facts[0]

    # Use Pandas to convert the data to a HTML table string.

    table_df.columns = ["description", "value"]
    data["facts"] = table_df.to_html(index=False)
    
    # Bring in the USGS Astrogeology site for our web scrapping
    url_4 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_4)

    # Create a Beautiful Soup object
    soup4 = bs(browser.html, 'lxml')

    hemisphere_image_urls = []

    # Run a for loop to click through our hemisphere links in order to 
    # append the titles & urls for the full resolution hemisphere images
    links = browser.find_by_css("a.product-item h3")
    for item in range(len(links)):
        hemisphere = {}
    
        browser.find_by_css("a.product-item h3")[item].click()
        
        # find urls for the full resolution hemisphere images
        aref_list = browser.find_link_by_text("Sample").first
        hemisphere["img_url"] = aref_list["href"]
        
        # find the titles for our hemisphere images
        hemisphere["title"] = browser.find_by_css("h2.title").text
        
        # append titles & urls for our hemisphere images
        hemisphere_image_urls.append(hemisphere)
        
        browser.back()
  
        data["hemispheres"] = hemisphere_image_urls

    browser.quit()

    return data