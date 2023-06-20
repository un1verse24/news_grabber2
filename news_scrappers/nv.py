import datetime
import requests
from bs4 import BeautifulSoup
from news_scrappers.general_scraper import NewsScraper

class NewVoiceScraper(NewsScraper):
    page = 1
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


    def get_news(self, period: int = 0) -> list[dict]:
        '''

        :param period: number of days that we want to observe.
        :return: json of news articles
        '''

        self.validate_period(period)

        period = abs(period)

        self.calculate_lower_bound_day(period)
        # self.lower_bound_day -= datetime.timedelta(days=1)

        while True:

            # ------------------------- Scrape with BeautifulSoup ----------------------------

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

                    if time < self.lower_bound_day:
                        return self.lst_articles

                    title = article.find(class_='title').text
                    link = article.find(class_='row-result-body').get('href')

                    self.lst_articles.append(self.create_article_object(time, title, link))

                # ------------------------- Scrape with BeautifulSoup ----------------------------

                else:
                    continue
            self.page += 1




if __name__ == '__main__':
    scraper = NewVoiceScraper()
    scraper.get_news()
    print(scraper.lst_articles)