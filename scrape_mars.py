# Import all the dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import requests 
import pandas as pd
import json
import pprint
import time 

executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
browser = Browser("chrome",**executable_path, headless=False)

# Start scrape which will return Python Dictonary with Data
def scrape():
    scrape_mars_dict = {}

# URL Page to scrape 
url = "https://mars.nasa.gov/news/"
browser.visit(url)
response = browser.html
soup = BeautifulSoup(response, 'html.parser')

#Find title 
results = soup.find('div', class_="content_title").get_text()
results

#Find article text 
paragraph_results = soup.find('div', class_="article_teaser_body").get_text()
paragraph_results

#Find Image
url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(url2)
time.sleep(2)
fullimage = browser.find_by_id('full_image')
fullimage.click()
time.sleep(2)
moreinfo = browser.find_link_by_partial_text('more info')
moreinfo.click()
time.sleep(3)
response2 = browser.html
soup2 = BeautifulSoup(response2, 'html.parser')\
featured_image_url = soup2.find('figure',class_="lede").find("img")["src"]
print (featured_image_url)
featured_image_url = "https://www.jpl.nasa.gov"+featured_image_url
featured_image_url

#Find Weather 
url3 = "https://twitter.com/marswxreport?lang=en"
browser.visit(url3)
time.sleep(3)
response3 = browser.html
soup3 = BeautifulSoup(response3, 'html.parser')
#Get last weather post
mars_weather = soup3.find('div',class_ = "js-tweet-text-container").find("p").get_text()
mars_weather
#Find Mars Facts
url4 = "https://space-facts.com/mars/"
browser.visit(url4)
time.sleep(3)
response4 = browser.html
soup4 = BeautifulSoup(response4, 'html.parser')
#use pandas to read_html to parse url
mars_facts = pd.read_html(url4)
mars_df = mars_facts[0]
mars_df.columns = ['Description','Value']
mars_df.set_index('Description', inplace=True)
mars_df.to_html()
data = mars_df.to_dict(orient='records')
mars_df
#Convert DF to HTML String 
mars_facts_HTML_table_string = mars_df.to_html()
pprint.pprint(mars_facts_HTML_table_string)
#Retrieve Mars Hemi Data
# Visit hemispheres website through splinter module 
hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(hemi_url)
hemi_response = requests.get(hemi_url)
Soup5 = BeautifulSoup(hemi_response.text, 'html.parser')
Hemi_List = Soup5.find_all('a', class_="itemLink product-item")
# Initialize array to store all the results - this will be an array of dictionaries
hemisphere_image_urls = []

# Loop through results to retrieve article image URL and Title

for image in Hemispheres_List: 
    image_title = image.find('h3').text 
    image_link = "https://astrogeology.usgs.gov/" + image['href'] 
    
    # This function will request the links to be clicked to in order to find the image url to the full resolution image.
    image_request = requests.get(image_link) 
    soup = BeautifulSoup(image_request.text, 'html.parser')
    image_tag = soup.find('div', class_='downloads')
    # Storing image URL variable loacated in <a> href </a> portion -> this is found by inspecting the image URL
    image_url = image_tag.find('a')['href']
    hemisphere_image_urls.append({"Title": image_title, "Image_URL": image_url})
    
# Printing the dictionary
pprint.pprint(hemisphere_image_urls)

#Create output dictionary 

   scrape_mars_dict = {
                        "News_Title": results,
                        "News_Paragraph": paragraph_results,
                        "Featured_Image_Link": featured_image_url,
                        "Weather": mars_weather,
                        "Interesting_Facts": mars_facts_HTML_table_string,
                        "Hemisphere_Images": hemisphere_image_urls
                        }
    return (scrape_mars_dict)
