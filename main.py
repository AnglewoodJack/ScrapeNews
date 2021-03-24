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




with open("search_res.txt", 'w', encoding="utf-8") as file:
    for n in rosatom.news:
        file.write(str(n['title']) + ';' + str(n['url']) + ';' + str(n['text']) + ';' + '\n')
