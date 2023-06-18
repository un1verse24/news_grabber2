import datetime
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

today = datetime.date.today()


class NewVoiceScraper:

    lst_articles = []
    page = 1
    headers = {
        'User-Agent': UserAgent().random
    }
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


    def get_news(self, period: int = 1) -> list[dict]:

        lower_bounds_day = today - datetime.timedelta(days=period)
        while True:
            response = requests.get(f'https://nv.ua/ukr/allnews.html?page={self.page}')
            soup = BeautifulSoup(response.text, 'html.parser')
            all_articles = soup.find_all(class_='row-result')
            # print(all_articles)
            for article in all_articles:
                topic = article.find(class_='atom-additional-category').text
                if topic == 'Події' or topic == 'Геополітика':
                    time = article.find(class_='additional-pub-date').text.strip()
                    time = time.split()
                    days = time[0]
                    month = time[1][:-1]
                    time = datetime.date(2023, self.hash_map_month[month], int(days))
                    if lower_bounds_day < time:
                        title = article.find(class_='title').text
                        link = article.find(class_='row-result-body').get('href')
                        article_obj = {
                            'time': time,
                            'link': link,
                            'title': title
                        }
                        self.lst_articles.append(article_obj)
                    else:
                        return self.lst_articles

                else:
                    continue
            self.page += 1




if __name__ == '__main__':
    scraper = NewVoiceScraper()
    scraper.get_news(2)
    print(scraper.lst_articles)