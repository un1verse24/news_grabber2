import datetime
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

today = datetime.date.today()


class CensorScraper:
    lst_articles = []
    headers = {
        'User-Agent': UserAgent().random
    }
    page = 1

    def get_news(self, period: int = 1) -> list[dict]:

        lower_bound_day = today - datetime.timedelta(days=period)

        while True:

            response = requests.get(f'https://censor.net/ua/news/all/page/{self.page}/category/0/interval/5/sortby/date', headers=self.headers)

            soup = BeautifulSoup(response.text, 'html.parser')

            all_articles = soup.find(class_='col-12 items-list').find_all(class_='news-list-item')

            for article in all_articles:
                time = article.find(class_='g-time').get('datetime').split('T')[0].split('-')
                year, month, day = int(time[0]), int(time[1]), int(time[2])
                time = datetime.date(year, month, day)
                if time < lower_bound_day:
                    return self.lst_articles

                title = article.find('h2').find(class_='news-list-item__title').text
                link = article.find('a').get('href')

                article_obj = {
                    'time': time,
                    'link': link,
                    'title': title
                }

                self.lst_articles.append(article_obj)

            self.page += 1



if __name__ == '__main__':
    scraper = CensorScraper()
    scraper.get_news(2)
    print(scraper.lst_articles)