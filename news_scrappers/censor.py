import datetime
import requests
from bs4 import BeautifulSoup
from news_scrappers.general_scraper import NewsScraper


class CensorScraper(NewsScraper):
    page = 1

    def get_news(self, period: int = 0) -> list[dict]:
        '''

        :param period: number of days that we want to observe.
        :return: json of news articles
        '''

        self.calculate_lower_bound_day(period)

        while True:

            # ------------------------- Scrape with BeautifulSoup ----------------------------

            response = requests.get(f'https://censor.net/ua/news/all/page/{self.page}/category/0/interval/5/sortby/date', headers=self.headers)

            soup = BeautifulSoup(response.text, 'html.parser')

            all_articles = soup.find(class_='col-12 items-list').find_all(class_='news-list-item')

            for article in all_articles:
                time = article.find(class_='g-time').get('datetime').split('T')[0].split('-')
                year, month, day = int(time[0]), int(time[1]), int(time[2])
                time = datetime.date(year, month, day)
                if time < self.lower_bound_day:
                    return self.lst_articles

                title = article.find('h2').find(class_='news-list-item__title').text
                link = article.find('a').get('href')


                self.lst_articles.append(self.create_article_object(time, title, link))


            # ------------------------- Scrape with BeautifulSoup ----------------------------

            self.page += 1



if __name__ == '__main__':
    scraper = CensorScraper()
    scraper.get_news(0)
    print(scraper.lst_articles)