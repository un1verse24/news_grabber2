import datetime
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


today = datetime.date.today()


class Channel24Scraper:
    lst_articles = []
    headers = {
        'User-Agent': UserAgent().random
    }
    counter_article = 0
    hash_map_month = {
        'січня': 1,
        'лютого': 2,
        'березня': 3,
        'квітня': 4,
        'травня': 5,
        'червня': 6,
        'липня': 7,
        'серпня': 8,
        'вересня': 9,
        'жовтня': 10,
        'листопада': 11,
        'грудня': 12
    }


    def get_news(self, period: int = 1):
        lower_bound_day = today - datetime.timedelta(days=period)


        while True:

            response = requests.get(f'https://24tv.ua/golovni-novini_tag1792/fromnews{self.counter_article}/',
                                    headers=self.headers)

            soup = BeautifulSoup(response.text, 'html.parser')
            all_articles = soup.find(class_='news-list oink').find_all(class_='simple-news-item without-photo')
            # print(len(all_articles))

            for article in all_articles:
                time = article.find(class_='news-info').find('span').text.split(',')[-1].strip().split()
                day = int(time[0])
                month = self.hash_map_month[time[1]]
                time = datetime.date(2023, month, day)
                if time < lower_bound_day:
                    return self.lst_articles

                title = article.find(class_='news-title').text
                link = article.find(class_='full-block-link').get('href')

                article_obj = {
                    'time': time,
                    'link': link,
                    'title': title
                }

                self.lst_articles.append(article_obj)


            self.counter_article += 14

            if self.counter_article > 1300:    # work with limit of site
                return self.lst_articles





        # print(all_articles)



if __name__ == '__main__':
    scraper = Channel24Scraper()
    scraper.get_news(2)
    print(scraper.lst_articles)