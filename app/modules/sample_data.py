from modules.newsparser import NewsAggregator
from modules.ner import NER
from random import randint, sample
from datetime import datetime

class SampleData():
    
    def __init__(self, sample_size: int = 10):
        self._na = NewsAggregator()
        self._na.aggregate()
        self._common_entity_types = self._na.named_entities
        self._ner = NER()
        self._feeds = self._na.to_dict()
        self._sample_size = sample_size
        self._samples = []
        self._sources = [feed['title'] for feed in self._feeds]
        for feed in self._feeds:
            indexes = sample(range(len(feed['items']) - 1), sample_size)
            for index in indexes:
                content = str(feed['items'][index]['content'])
                ne_set = self._ner.named_entities(content)
                self._samples.append((content, ne_set))
        
        
    def sample_news_articles(self):
        """
        Write a sample of all collected news articles and the recovered named entities to a text file for manual comparison
        """
        with open(f'samples/sample-news-{datetime.now()}.txt','x') as f:
            f.write(f'Date: {datetime.now()}, Sample size: {self._sample_size},\nSources: {self._sources}\n')
            for sample in self._samples:
                content ,ne_set = sample
                ne_set = str(ne_set)
                f.write(content + '\n')
                f.write(ne_set + '\n\n')
    
    
    def sample_common_entity_types(self, treshold = 0.1):
        
        with open(f'samples/sample-common-entity-sets-{datetime.now()}.txt','x') as f:
            f.write(f'Date: {datetime.now()}\nSources: {self._sources}\nWeight Treshold: {treshold}\n\n')
            for ne_set, weight in self._common_entity_types.items():
                if weight < treshold:
                    continue
                ne_set = str(ne_set)
                weight = str(weight)
                f.write(weight + '>>')
                f.write(ne_set + '\n\n')
        