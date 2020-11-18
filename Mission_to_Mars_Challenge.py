# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd


# %%
# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path' : 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

# %% [markdown]
# ### Visit the NASA Mars News Site

# %%
# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# %%
# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('ul.item_list li.slide')


# %%
slide_elem.find("div", class_='content_title')


# %%
# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# %%
# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p

# %% [markdown]
# ### JPL Space Images Featured Image

# %%
# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# %%
# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()


# %%
# Find the more info button and click that
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()


# %%
# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# %%
# find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel


# %%
# Use the base url to create an absolute url
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url

# %% [markdown]
# ### Mars Facts

# %%
df = pd.read_html('http://space-facts.com/mars/')[0]

df.head()


# %%
df.columns=['Description', 'Mars']
df.set_index('Description', inplace=True)
df


# %%
df.to_html()

# %% [markdown]
# ### Mars Weather

# %%
# Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)


# %%
# Parse the data
html = browser.html
weather_soup = soup(html, 'html.parser')


# %%
# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())

# %% [markdown]
# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
# %% [markdown]
# ### Hemispheres

# %%
# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# %%
# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
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


# %%
# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# %%
# 5. Quit the browser
browser.quit()


# %%



