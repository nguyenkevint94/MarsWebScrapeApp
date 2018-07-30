# Dependencies
import requests
import re
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser

def init_browser():
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    # Python dictionary 
    mars_data={}

    # News retrieval
    news_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(news_url)
    html = browser.html
    soup = bs(html, "html.parser")
    title = soup.find("h3")
    para = soup.find("div", class_="article_teaser_body")
    news_title = title.text.strip()
    news_p = para.text.strip()
    mars_data["news_title"]=news_title
    mars_data["news_p"]=news_p

    # Mars images retrieval
    mars_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(mars_image_url)
    html = browser.html
    soup = bs(html, "html.parser")
    image_url = soup.find("ul", class_ = "articles")("li", class_ = "slide")[0]("a", class_="fancybox")[0]["data-fancybox-href"]
    featured_image_url = ("https://www.jpl.nasa.gov/" + image_url)
    mars_data["latestImageURL"] = featured_image_url

    # Mars weather retrieval
    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)
    html = browser.html
    soup = bs(html, "html.parser")
    mars_weather = soup.find(text=re.compile("Sol "))
    mars_data["marsWeather"]=mars_weather

    # Mars facts
    mars_facts_url = "https://space-facts.com/mars/"
    browser.visit(mars_facts_url)
    html = browser.html
    soup = bs(html, "html.parser")
    table = pd.read_html(mars_facts_url)
    dfmars = table[0]
    dfmars.columns=["Description", "Value"]
    dfmars.set_index("Description",inplace=True)
    mars_facts_html = dfmars.to_html()
    mars_facts_html = mars_facts_html.replace("\n"," ")
    mars_data["marsFacts"] = mars_facts_html
 
    # Mars hemispheres
    hemispheres_url ="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html = browser.html
    soup = bs(html, "html.parser")
    links = soup.find_all("div", class_="item")
    page_links=[]
    for link in links:
        page_links.append("https://astrogeology.usgs.gov" + link("a", class_="itemLink product-item")[0]["href"])
    
    hemisphere_image_urls=[]
    for page in page_links:
        title=""
        img_url=""
        detailDict = {"title":"","img_url":""}
        browser.visit(page)
        html = browser.html
        soup = bs(html, "html.parser")
        title = soup("h2",class_="title")[0].text
        img_url = soup('div',class_="wide-image-wrapper")[0]("a")[0]["href"]
        detailDict["title"] = title
        detailDict["img_url"] = img_url
        hemisphere_image_urls.append(detailDict)
        
    mars_data["page_links"] = page_links
    mars_data["imageURL"] = hemisphere_image_urls
    
    return mars_data
