import requests
import re
from bs4 import BeautifulSoup

"""
Example of scrapping 10 pages of cell phones:

urls = make_urls(['cell phones'], 10)
scrap_listings(urls, DIRECTORY_PATH)
"""

# Given listing it downloads first image
def get_image(page, name, path):
    result = requests.get(page)
    
    soup = BeautifulSoup(result.text, 'html.parser')
    links = soup.find(itemprop='image')
    
    image = links['src']

    f = open(path + '{}.jpg'.format(name), 'wb')
    f.write(requests.get(image).content)
    f.close()

# Creates num_pages urls of search results for each search term in names
def make_urls(names, num_pages=1):
    url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw={}&LH_Auction=1&rt=nc&LH_ItemCondition=7000'
    urls = []
    
    for i in range(1, num_pages+1):
        for name in names:
            urls.append(url.format(name.replace(' ', '+')) + '&_pgn={}'.format(i))
        
    return urls

# Takes list of search page urls and downloads first image from all listings on the pages
def scrap_listings(urls, path):
    listings = set()
    count = 0
    
    for url in urls:
        res = requests.get(url)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        raw_listings = soup.findAll('a', {'_sp': 'p2351460.m1686.l7400', 'href': re.compile("^https://www.ebay.com/itm")})

        for link in raw_listings:
            listings.add(link['href'])        
    print('Number of scraped listings:', len(listings))
    
    for i, listing in enumerate(listings):
        get_image(listing, 'phone{}'.format(i), path)    
    print('Done downloading images')