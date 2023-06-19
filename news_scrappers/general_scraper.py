import datetime
from fake_useragent import UserAgent


class NewsScraper:
    headers = {
        'User-Agent': UserAgent().random
    }
    lst_articles = []
    today = datetime.date.today()


    def calculate_lower_bound_day(self, period: int = 0):
        if period < 1 and type(period) != int:
            return ''
        self.lower_bound_day = self.today - datetime.timedelta(days=period)


    def create_article_object(self, time: datetime, title: str, link: str) -> dict:
        article_obj = {
            'time': time,
            'link': link,
            'title': title
        }

        return article_obj


