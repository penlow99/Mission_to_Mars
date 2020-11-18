
from bs4 import BeautifulSoup as soup
from splinter import Browser
import pandas as pd
import datetime as dt


###########################
####  Master Function  ####
###########################
def scrape_all():
    # Set the executable path
    executable_path = {'executable_path': 'chromedriver'}
    # initialize the chrome browser in splinter
    browser = Browser('chrome', **executable_path, headless=True)
    news_title, news_paragraph = mars_news(browser)
    hemi_dict = hemi_scrape(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres" : hemi_dict
    }

    # kill the browser...until its DEAD!!!
    browser.quit()
    # return the data dictionary
    return data


#################
### Mars News ###
#################
def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
    # Convert the html from browser to soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None

    return news_title, news_p
#################


#######################
### Featured Images ###
#######################
def featured_image(browser):

    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # find and click the 'Full Image' button
    full_image_elem = browser.find_by_id('full_image')[0]
    full_image_elem.click()

    # find the 'More Info' button and click it
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get('src')
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

    return img_url
#######################


##################
### Mars Facts ###
##################
def mars_facts():

    try:
        # Use the read_html function to find the first table on the page
        # and read it into a DataFrame 
        df = pd.read_html('http://space-facts.com/mars')[0]
    except BaseException:
        return None

    # Assign column names and set index
    df.columns = ['Description', 'Mars']
    df.set_index('Description', inplace=True)
    df.index.name = None

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped table-hover")
##################


##########################
### Hemispheres Scrape ###
##########################
def hemi_scrape(browser):
    # Use browser to visit the URL 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # Write code to retrieve the image urls and titles for each hemisphere.
    start_url = 'https://astrogeology.usgs.gov'
    html = browser.html
    html_soup = soup(html, 'html.parser')
    hemi_soup = html_soup.find_all('div', class_='item')
    for item in hemi_soup:
        title = item.find('h3')
        url = item.find('a')
        browser.visit(start_url + url.get('href'))
        individual_page_soup = soup(browser.html, 'html.parser')
        div_soup = individual_page_soup.find('div', class_='downloads')
        img_url = div_soup.select_one('ul li a').get('href')
        hemisphere_image_urls.append({'img_url' : img_url, 'title' : title.text})

    return hemisphere_image_urls
##########################


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())






