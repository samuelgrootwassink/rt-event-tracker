from modules.newsparser import NewsAggregator
from modules.ner import NER
from random import randint
from datetime import datetime

class SampleData():
    
    def __init__(self, sample_size: int = 3):
        self._na = NewsAggregator()
        self._na.aggregate()
        self._ner = NER()
        self._feeds = self._na.to_dict()
        self._sample_size = sample_size
        self._samples = []
        self._sources = [feed['title'] for feed in self._feeds]
        for feed in self._feeds:
            for _ in range(sample_size):
                index = randint(0, len(feed['items']) - 1)
                content = str(feed['items'][index]['description'])
                ne_set = self._ner.named_entities(content)
                self._samples.append((content, ne_set))
        
        
    def sample_text_file(self):
        """
        Write a sample of all collected news articles and the recovered named entities to a text file for manual comparison
        """
        with open(f'samples/sample-{datetime.now()}.txt','x') as f:
            f.write(f'Date: {datetime.now()}, Sample size: {self._sample_size},\n Sources: {self._sources}\n')
            for sample in self._samples:
                content ,ne_set = sample
                ne_set = str(ne_set)
                f.write(content + '\n')
                f.write(ne_set + '\n\n')
    