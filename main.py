import pandas as pd

from scraper import NewsScraper
from config import configure_driver

# create driver object
driver = configure_driver()
# specify link
link = 'https://www.rosatom.ru/'


rosatom = NewsScraper(driver, link, 3)

rosatom.scrape_brief("водород")

rosatom.scrape_full()

print(rosatom.news[0]['text'])

results = pd.DataFrame(rosatom.news)

results.to_csv('search_res.csv')
