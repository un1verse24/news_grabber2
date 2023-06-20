import sys


from news_scrappers.ukrainian_truth_scraper import UkrainianTruthScraper
from news_scrappers.channel24 import Channel24Scraper
from news_scrappers.censor import CensorScraper
from news_scrappers.nv import NewVoiceScraper



def get_all_news() -> list[dict]:
    scraper1 = scraper2 = scraper3 = scraper4 = None
    lst_scrapers = []
    res = []
    hash_map = {
        '1': [UkrainianTruthScraper, scraper1],
        '2': [Channel24Scraper, scraper2],
        '3': [CensorScraper, scraper3],
        '4': [NewVoiceScraper, scraper4]
    }
    period = (input('For how many days you want to observe news?(press q for exit)'))

    if period.strip().lower() == 'q' or not period:
        sys.exit()
    try:
        period = abs(int(period))
    except Exception:
        print("You print not a integer number, please type integer number next time!")

    print('Please choose from which news sites you want to grab news.(press q for exit)',
          'List:',
          '1. Ukrainian Truth',
          '2. Channel 24',
          '3. Censor.net',
          '4. New Voice', sep='\n')

    which_news_sites = input()


    if which_news_sites.strip().lower() == 'q' or not which_news_sites:
        print(" ending a program....")
        sys.exit()


    for key, item in hash_map.items():
        if key in which_news_sites:
            item[1] = item[0]()
            lst_scrapers.append(item[1])

    if not lst_scrapers:
        print("You didn't choose any scraper, please choose another time existing scraper")
        sys.exit()


    for scraper in lst_scrapers:
        res.extend(scraper.get_news(period))


    return res



if __name__ ==  '__main__':
    print(get_all_news())