import datetime
import requests
from bs4 import BeautifulSoup
from general_scraper import NewsScraper





class UkrainianTruthScraper(NewsScraper):

    def get_news(self, period: int = 0) -> list[dict]:
        '''

        :param period: number of days that we want to observe.
        :return: json of news articles
        '''

        # if period < 1 and type(period) != int:
        #     return list()

        self.calculate_lower_bound_day(period)
        self.lower_bound_day -= datetime.timedelta(days=1)

        # tdelta = datetime.timedelta(days=period)
        # self.lower_bound_day = current_time - tdelta

        while self.today > self.lower_bound_day:
            tmp = self.today
            str_day = str(tmp).split('-')
            str_day.reverse()
            str_day = ''.join(str_day)
            url = f'https://www.pravda.com.ua/news/date_{str_day}/'

            # ------------------------- Scrape with BeautifulSoup ----------------------------

            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')

            all_news_articles = soup.find(class_='container_sub_news_list_wrapper mode1')
            articles_with_photo = all_news_articles.find_all(
                class_='article_news_list article_news_bold article_news_img')
            bold_articles = all_news_articles.find_all(class_='article_news_list article_news_bold')
            lst_of_united_articles = [*articles_with_photo, *bold_articles]


            for article in lst_of_united_articles:
                time = article.find(class_='article_time').text
                link = article.find(class_='article_header').find('a').get('href')
                link = link if link[0] == 'h' else 'https://www.pravda.com.ua' + link
                title = article.find(class_='article_header').text

                self.lst_articles.append(self.create_article_object(time, title, link))


            # ------------------------- Scrape with BeautifulSoup ----------------------------


            # self.lower_bound_day += datetime.timedelta(days=1)
            self.today -= datetime.timedelta(days=1)  # problem with current_day

        return self.lst_articles


if __name__ == '__main__':
    scraper = UkrainianTruthScraper()
    scraper.get_news()
    print(scraper.lst_articles)