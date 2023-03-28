from modules.newsparser import NewsAggregator
from modules.sample_data import SampleData
from modules.twitter_scraper import TwitterScraper
# sd = SampleData(3)
# sd.sample_news_articles()
# sd.sample_common_entity_types(1.5)

ts = TwitterScraper()
ts.search_tweets([frozenset({'Ukraine', 'Russia', 'Donetsk'})])