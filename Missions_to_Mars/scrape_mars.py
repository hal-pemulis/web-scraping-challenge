# Import dependencies
import pandas as pd
import requests
from bs4 import BeautifulSoup
from splinter import Browser
import time

def scrape():

    recent_mars_info = {}

    # Get latest Mars news title/teaser
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    nasa_url = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find('ul', class_="item_list")
    results_title = results.find('div', class_='content_title')
    news_title = results_title.a.text
    news_link = results.a['href']
    news_p = results.find('div', class_='article_teaser_body').text
    # news_img = results.img['src']

    time.sleep(5)

    # Get JPL featured image
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    featured_image_url = (f"https://www.jpl.nasa.gov{soup.find('a', class_='button fancybox')['data-fancybox-href']}")
    browser.quit()

    # Get lastest Mars weather tweet
    request = requests.get('https://twitter.com/marswxreport?lang=en')
    soup = BeautifulSoup(request.content, 'html.parser')
    mars_weather = soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

    # Use Pandas' `read_html` to parse the url
    space_facts = 'https://space-facts.com/mars/'
    tables = pd.read_html(space_facts)
    df = tables[0]
    df.columns = ['Index', 'Value']
    df.set_index('Index', inplace=True)
    # Convert DF to dictionary
    fact_dict = df.to_dict()
    # df.to_html('../Resources/mars_table.html')

    mars_pics_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    request = requests.get(mars_pics_url)
    soup = BeautifulSoup(request.content, 'html.parser')
    results = soup.find_all('a', class_="itemLink product-item")
    img_list = []
    for result in results:   
        img = (f"https://astrogeology.usgs.gov{result['href']}")                      
        pic_req = requests.get(img)              
        pic_soup = BeautifulSoup(pic_req.content, 'html.parser')           
        page_name = (pic_soup.find('h2', class_='title')).text            
        title = page_name.split(' ')[0]       
        results = pic_soup.find('li')
        full_pic = results.find('a')['href']
        img_list.append({'title': title, 'image_url': full_pic})
                
    # Create and return dictionary from scraped data             
    recent_mars_info={}
    recent_mars_info['Latest_News'] = {'Title':news_title, 'Teaser': news_p, 'URL': news_link}
    recent_mars_info['JPL_Featured_Image'] = featured_image_url
    recent_mars_info['Current_Mars_Weather'] = mars_weather
    recent_mars_info['Hemisphere_images'] = img_list
    recent_mars_info['Mars_Facts'] = fact_dict['Value']

    print(recent_mars_info)

    return recent_mars_info

# scrape()