from requests import get
from bs4 import BeautifulSoup
import os
import pandas as pd
import numpy as np

def get_blog_articles(use_cache=True):

    # establish a filename for the local csv
    filename = 'codeup_blog_articles.csv'
    
    if use_cache:
        
        # check to see if a local copy already exists
        if os.path.exists(filename):
            print('Reading from local CSV...')
            # if so, return the local csv
            return pd.read_csv(filename)
        
    # otherwise, scrape the data from codeup.com
    print('Reading blog articles from codeup.com...')
    
    articles = []

    # go to blog homepage
    url = 'https://codeup.com/blog/'
    headers = {'user-agent': 'Innis Data Science Cohort'}
    response = get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # get url for next page of articles
    # (returns None if there are no more pages)
    next_page = soup.select_one('.pagination.clearfix').div.a

    # get the urls for the rest of the articles on this page
    urls = []
    for article in soup.select('article'):
        #for link in article.select('.more-link'):
        for link in article.select('.entry-featured-image-url'):
            urls.append(link.attrs['href'])

    # go to each article page
    for url in urls:
        response = get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # pull article info and append to list
        dct = {}
        dct['title'] = soup.select_one('.entry-title').text
        dct['content'] = soup.select_one('.entry-content').text.strip()
        articles.append(dct)

    page_counter = 1
    print(f'{page_counter} pages complete     ', end='\r')

    # check whether there is a next page
    while next_page != None:
        # go to the next page
        url = next_page.attrs['href']
        response = get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # get url for next page of articles
        # (this will return None if there are no more pages)
        next_page = soup.select_one('.pagination.clearfix').div.a

        # get all the urls for articles on this page
        urls = []
        for article in soup.select('article'):
            for link in article.select('.entry-featured-image-url'):
                urls.append(link.attrs['href'])

        # go to each article page
        for url in urls:
            response = get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')

            # pull article info and append to list
            dct = {}
            dct['title'] = soup.select_one('.entry-title').text
            dct['content'] = soup.select_one('.entry-content').text.strip()
            articles.append(dct)

        page_counter += 1
        print(f'{page_counter} pages complete     ', end='\r')
        
    print(f'{page_counter} pages scraped. No more pages available.')
    
    articles = pd.DataFrame(articles)

    # cache local copy
    print('Writing to local CSV...')
    articles.to_csv(filename, index=False)
    
    return articles

def get_news_articles(categories=['business', 'sports', 
                                  'technology', 'entertainment'], 
                      use_cache=True):
    
    # establish a filename for the local csv
    filename = 'news_articles.csv'
    
    if use_cache:
        # check to see if a local copy already exists
        if os.path.exists(filename):
            print('Reading from local CSV...')
            # if so, return the local csv
            return pd.read_csv(filename)
        
    # otherwise, scrape the data from codeup.com
    print('Reading blog articles from inshorts.com...')

    articles = []

    for category in categories:

        url = f'https://inshorts.com/en/read/{category}'
        response = get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        for card in soup.select('.news-card'):
            dct = {}
            dct['title'] = card.select('.news-card-title')[0].span.text
            dct['author'] = card.select('.author')[0].text
            dct['content'] = card.select_one('.news-card-content').div.text
            dct['category'] = category
            articles.append(dct)
            
    articles = pd.DataFrame(articles)
    
    # cache local copy
    print('Writing to local CSV...')
    articles.to_csv(filename, index=False)
            
    return articles