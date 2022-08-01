# # Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

#    Initiate headless driver for deployment
# executable_path = {'executable_path': ChromeDriverManager().install()}
# browser = Browser('chrome', **executable_path, headless=True)

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemisphere_images": hemisphere_data(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):
    # Initiate headless driver for deployment
    # executable_path = {'executable_path': ChromeDriverManager().install()}
    # browser = Browser('chrome', **executable_path, headless=True)

    # Visit the Mars news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    #Add try except for error handling

    try:

        slide_elem = news_soup.select_one('div.list_text')

        # slide_elem.find('div', class_='content_title')

        # Use the parent element to find the first a tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:

        return None, None
    
    return news_title, news_p

# ## JPL Space Images Featured Image
def featured_image(browser):
    # Initiate headless driver for deployment
    # executable_path = {'executable_path': ChromeDriverManager().install()}
    # browser = Browser('chrome', **executable_path, headless=True)

# Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
    # find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:

        return None

    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'     
    
    return img_url

# ## Mars Facts

def mars_facts():
    # Initiate headless driver for deployment
    # executable_path = {'executable_path': ChromeDriverManager().install()}
    # browser = Browser('chrome', **executable_path, headless=True)

    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

#Create a function to scrape hemisphere data
def hemisphere_data(browser):
    url = 'https://marshemispheres.com/'
    # Initiate headless driver for deployment
    # executable_path = {'executable_path': ChromeDriverManager().install()}
    # browser = Browser('chrome', **executable_path, headless=True)
    browser.visit(url + "index.html")
    html = browser.html
    hemi_soup = soup(html, 'html.parser')
    # Optional delay for loading the page
    # browser.is_element_present_by_css('div.list_text', wait_time=1) # ??????

# Create a list to hold the images and titles.
    hemisphere_image_urls = []

# Code to retrieve the image urls and titles for each hemisphere.

    # links = browser.find_by_css('a.product-item img')

    for i in range(4):
        browser.find_by_css('a.product-item img')[i].click()
        
        try:
            sample_elem = hemi_soup.find('a', text='Sample').get("href")
            hemisphere['img_url'] = url + sample_elem
            
            title_elem = hemi_soup.find("h2", 'title').get_text()
            hemisphere['title'] = title_elem

        except AttributeError:
            sample_elem = None
            title_elem = None
        hemisphere = {
            "title":title_elem,
            "img_url": sample_elem
        }
        hemisphere_image_urls.append(hemisphere)
        browser.back()


    # Print the list that holds the dictionary of each image url and title.
   

    #return the scraped data as a list of dictionaries with the URL string and title of each hemisphere image
    return hemisphere_image_urls


if __name__ == "__main__":

     # If running as script, print scraped data
    print(scrape_all())