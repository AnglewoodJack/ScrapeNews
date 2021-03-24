import random
import selenium
from selenium.webdriver.common.keys import Keys

from time import sleep
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from tqdm import tqdm


class NewsScraper:
    """
    Scrape news from rosatom site based on search.
    """

    def __init__(self, driver, link: str, timeout: float):
        """
        :param driver: preconfigured webdriver (result of "configure_driver" function)
        :param link: IAEA job page url to scrape
        :param timeout: webdriver wait time for page loading
        """
        # browser driver
        self.driver = driver
        # timeout
        self.timeout = timeout
        # jobs page link
        self.link = link
        # list of news dictionaries
        self.news = None

    def scrape_brief(self, search_query):
        """
        Get title and link.
        :param search_query: text to search.
        """
        # go to jobs page
        self.driver.get(self.link)
        # locate search button and click it
        self.driver.find_element_by_class_name("btn-search").click()
        # locate search input field
        inputElement = self.driver.find_element_by_id("searchMain")
        # put in search string
        inputElement.send_keys(search_query)
        # send search request
        inputElement.send_keys(Keys.ENTER)

        # click on "show more results" until all search results displayed on page
        while True:
            try:
                element = self.driver.find_element_by_class_name('load-more')
            except selenium.common.exceptions.NoSuchElementException:
                break
            self.driver.execute_script("arguments[0].click();", element)
            sleep(0.5)

        # get page source
        s = BeautifulSoup(self.driver.page_source, features="html.parser")
        # collect links and titles from search results
        news = []
        for a in tqdm(s.findAll('a', href=True, attrs={'class': 'greyBG'}), desc=f"Scraping search results"):
            if a.span.text:
                new = {'url': urljoin(self.link, a['href']),
                       'title': a.findChild('span', attrs={'class': 'title'}).text}
                news.append(new)

        # save news list to class attribute
        self.news = news

    def scrape_full(self):
        """
        The full text of the news.
        """
        # for each news in the list
        for new in tqdm(self.news, desc="Getting news text"):
            # go to news page
            self.driver.get(new['url'])
            # get page source
            s = BeautifulSoup(self.driver.page_source, features="html.parser")
            # empty string to place article text
            article_text = ''
            for div in s.findAll('div', attrs={'class': 'article__body'}):
                article_text += div.text
            # save article text to dictionary
            new['text'] = article_text
            # sleep random time after each article
            sleep(random.uniform(0.75, 1.0))
        # close driver after getting all news info
        self.driver.quit()
