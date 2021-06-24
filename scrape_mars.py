# Dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt

#Choose the executable path to driver
#def init_browser():
def init_browser():
    executable_path = {'executable_path':ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

def mars_news(browser):
    # Visit the NASA Mars News Site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    import time
    time.sleep(3)

    # Scrape page into Soup
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')

    # Get the title and paragraph of news
    news_title = soup.find("div",class_="content_title").get_text()
    news_paragraph= soup.find("div", class_="article_teaser_body").get_text()

    return news_title, news_paragraph



def featured_image(browser):

    # Mars Image to be scraped
    images_url = 'https://spaceimages-mars.com'

    # Browser to page
    browser.visit(images_url)

    import time
    time.sleep(3)

    # Find the first full size image
    html = browser.html
    images_soup = BeautifulSoup(html,'html.parser')

    # Retrieve featured image link
    relative_image_path = images_soup.find_all('img')[3]["src"]
    featured_image_url = images_url + relative_image_path
    return featured_image_url
    


def mars_facts():
    # Set the url and use pandas to pull table
    url_facts = "https://galaxyfacts-mars.com"
    df_mars_facts = pd.read_html(url_facts)[1]

    df_mars_facts.columns = ["Parameter", "Values"]
    df_mars_facts.set_index("Parameter", inplace = True)

    mars_html_table = df_mars_facts.to_html()
    mars_html_table = mars_html_table.replace("\n", "")
         
    return mars_html_table


def mars_hemispheres(browser):
    url_hemisphere = "https://marshemispheres.com/"
    browser.visit(url_hemisphere)

    import time
    time.sleep(3)

    html_hemispheres = browser.html
    soup = BeautifulSoup(html_hemispheres ,'html.parser')

    #Create an empty list of links for the hemispheres
    hemisphere_image_urls=[]
    products=soup.find('div', class_='result-list')
    hemispheres=products.find_all('div',{'class':'item'})

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://marshemispheres.com/" + end_link    
        browser.visit(image_link)
        html_hemispheres = browser.html
        soup=BeautifulSoup(html_hemispheres,'html.parser')
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        hemisphere_image_urls.append({"title": title, "img_url": image_url})
        
        return  hemisphere_image_urls

#################################################
# Main Web Scraping Bot
#################################################
def scrape_all():
    browser=init_browser ()
    news_title, news_paragraph = mars_news(browser)
    featured_image_url = featured_image(browser)
    facts = mars_facts()
    hemisphere_image_urls = mars_hemispheres(browser)
    timestamp = dt.datetime.now()

    mars_data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image_url,
        "facts": facts,
        "mars_hemispheres": hemisphere_image_urls,
        "last_modified": timestamp
    }
    
    # Close the browser after scraping
    browser.quit()
    # Return results
    return mars_data 


if __name__ == "__main__":
       print(scrape_all())