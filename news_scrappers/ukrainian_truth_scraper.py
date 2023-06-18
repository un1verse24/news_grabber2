import datetime
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

current_time = datetime.datetime.now()


# current_day = datetime.date.today()


class NewsScraper:
    pass


class UkrainianTruthScraper:
    headers = {
        'User-Agent': UserAgent().random
    }
    lst_articles = []

    current_day = datetime.date.today()

    def test_func(self):
        response = requests.get('https://www.pravda.com.ua/news/', headers=self.headers)
        # print(response.text)
        soup = BeautifulSoup(response.text, 'html.parser')
        all_news_articles = soup.find(class_='container_sub_news_list_wrapper mode1')
        default_articles = all_news_articles.find_all(class_='article_news_list')  # grabe articles without photo
        articles_with_photo = all_news_articles.find_all(class_='article_news_list article_news_bold article_news_img')
        lst_of_united_articles = [*default_articles, *articles_with_photo]

        for article in lst_of_united_articles:
            time = article.find(class_='article_time').text
            link = article.find(class_='article_header').find('a').get('href')
            link = link if link[0] == 'h' else 'https://www.pravda.com.ua' + link
            title = article.find(class_='article_header').text
            article_obj = {
                'time': time,
                'link': link,
                'title': title
            }
            self.lst_articles.append(article_obj)

            pass

    def get_news(self, period: int = 1, only_main: bool = False) -> list[dict]:
        '''

        :param period: number of days that we want to observe
        :param only_main: true if we want grab only main news
        :return: json of news articles
        '''

        if period < 1 and type(period) != int:
            return list()

        tdelta = datetime.timedelta(days=period)
        lower_bounds_day = current_time - tdelta

        while lower_bounds_day < current_time:
            tmp = self.current_day
            str_day = str(tmp).split('-')
            str_day.reverse()
            str_day = ''.join(str_day)
            url = f'https://www.pravda.com.ua/news/date_{str_day}/'
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')

            all_news_articles = soup.find(class_='container_sub_news_list_wrapper mode1')
            articles_with_photo = all_news_articles.find_all(
                class_='article_news_list article_news_bold article_news_img')
            bold_articles = all_news_articles.find_all(class_='article_news_list article_news_bold')
            lst_of_united_articles = [*articles_with_photo, *bold_articles]

            # block with default(not main) news under
            if not only_main:
                default_articles = all_news_articles.find_all(class_='article_news_list')
                lst_of_united_articles.extend(default_articles)

            for article in lst_of_united_articles:
                time = article.find(class_='article_time').text
                link = article.find(class_='article_header').find('a').get('href')
                link = link if link[0] == 'h' else 'https://www.pravda.com.ua' + link
                title = article.find(class_='article_header').text
                article_obj = {
                    'time': time,
                    'link': link,
                    'title': title
                }
                self.lst_articles.append(article_obj)
                # print(url)

            lower_bounds_day += datetime.timedelta(days=1)
            self.current_day -= datetime.timedelta(days=1)  # problem with current_day

        print(self.lst_articles)
        return self.lst_articles


if __name__ == '__main__':
    scraper = UkrainianTruthScraper()
    scraper.get_news(period=2)