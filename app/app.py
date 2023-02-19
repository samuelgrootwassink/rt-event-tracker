from modules.newsparser import NewsAggregator

np = NewsAggregator()
np.aggregate()
print(np.named_entities)