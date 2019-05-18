from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pymongo
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    browser = init_browser()

    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    title = soup.find('div', class_='content_title').find('a').text
    paragraph = soup.find('div', class_='article_teaser_body').text

    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)

    html2 = browser.html
    soup2 = BeautifulSoup(html2, 'html.parser')

    article = soup2.find('a', class_='fancybox')
    href = article['data-fancybox-href']
    main_URL = 'https://www.jpl.nasa.gov'
    featured_image_url = main_URL + href

    url3 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url3)

    html3 = browser.html
    soup3 = BeautifulSoup(html3, 'html.parser')

    mars_weather = soup3.find('div', class_ = 'js-tweet-text-container')
    mars_weather = soup3.find('p' , class_ = 'TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
    mars_weather = mars_weather.replace('.twitter.com/qtElTnSRJj', '')

    url4 = 'https://space-facts.com/mars/'
    browser.visit(url4)

    table = pd.read_html(url4)
    df_mars = table[0]
    df_mars.columns = ['Features', 'Measurements']
    df_mars.set_index('Features', inplace = True)

    html_mars = df_mars.to_html()
    html_mars = html_mars.replace('\n', '')

    url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url5)

    html5 = browser.html
    soup5 = BeautifulSoup(html5, 'html.parser')

    image = soup5.find_all('div', class_='item')
    image_url=[]
    image_title=[]
    list_dict=[]
    for x in image:
        image_title.append(x.find('h3').text)
        url = x.find('a', class_ = 'itemLink product-item')['href']
        goto = 'https://astrogeology.usgs.gov/' + url
        browser.visit(goto)
        image_html = browser.html
        soup_html = BeautifulSoup(image_html, 'html.parser')
        image_url.append('https://astrogeology.usgs.gov/' + soup_html.find('img', class_ = 'wide-image')['src'])
    for value in range(4):
        list_dict.append({'title': image_title[value], 'img_url': image_url[value]})

    mars_data = {
        "title": title, 
        "paragraph": paragraph,
        "image": featured_image_url,
        "weather": mars_weather,
        "facts": html_mars,
        "hemisphere": list_dict
    }

    browser.quit()

    return mars_data