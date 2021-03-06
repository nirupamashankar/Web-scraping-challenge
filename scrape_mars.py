#import dependencies/libraries
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import pymongo
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import time

#set up driver to access browser
def init_browser():
    executable_path = {"executable_path": "C:/Users/aolan/PythonStuff/Assignment1/Web-scraping-challenge/chromedriver.exe"}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_dict = {}
    news_url = 'https://mars.nasa.gov/news/'
#visit site and breakdown html characteristics
    browser.visit(news_url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

#retrieve latest news title and display result
    news_title = soup.find("div", class_="list_text").find("div", class_="content_title").text
    
#retrieve latest news para summary and display result
    news_para = soup.find("div", class_="article_teaser_body").text


# JPL Mars Space Images - Featured Image

#define required url to access
    mars_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

#visit site and breakdown html characteristics
    html = browser.html
    browser.visit(mars_url)
    soup = BeautifulSoup(html, "html.parser")
    
    full_image = browser.click_link_by_partial_text("FULL IMAGE")
    time.sleep(4)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    full_image_url = soup.find('img', class_="fancybox-image")["src"]
    image_url = "https://www.jpl.nasa.gov" + full_image_url
    
    
# ## Mars Facts

# # define required url to access
    facts_url = "https://space-facts.com/mars/"

#use pandas to scrape data from table
    facts_tables = pd.read_html(facts_url)


#strip required content into tables
    mars_facts_df = facts_tables[2]

#name columns and display pandas table
    mars_facts_df.columns = ["Mars Attribute", "Numeric Value"]
    mars_facts_df

#convert the dataframe to html

    mars_facts_html = mars_facts_df.to_html()
    mars_facts_html

#get rid of extraneous text
    mars_facts_html.replace('\n', '')
    

## Mars Hemispheres

# define required url to access

    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
# HTML Object
    html_hemispheres = browser.html

# Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html_hemispheres, 'html.parser')

# Retreive all items that contain mars hemispheres information
    items = soup.find_all('div', class_='item')
    
# Create empty list for hemisphere urls 
    hemisphere_image_urls = []

# Store the main_ul 
    hemispheres_main_url = 'https://astrogeology.usgs.gov'
    
# Loop through the items previously stored
    for i in items: 
        # Store title
        title = i.find('h3').text
        
        # Store link that leads to full image website
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
        
        # Visit the link that contains the full image website 
        browser.visit(hemispheres_main_url + partial_img_url)
        
        # HTML Object of individual hemisphere information website 
        partial_img_html = browser.html
        
        # Parse HTML with Beautiful Soup for every individual hemisphere information website 
        soup = BeautifulSoup( partial_img_html, 'html.parser')
        
        # Retrieve full image source 
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
        
        # Append the retreived information into a list of dictionaries 
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
        

    # Display hemisphere_image_urls
        hemisphere_image_urls
        print(image_url)

    mars_dict = {
        "news_title": news_title,
        "news_para": news_para,
        "featured_image_url": image_url,
        "fact_table": str(mars_facts_html),
        "hemisphere_images": hemisphere_image_urls
    }
        
    return(mars_dict)
scrape()
