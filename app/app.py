from modules.newsparser import NewsAggregator
from modules.sample_data import SampleData

np = NewsAggregator()
np.aggregate()
ne_sets = np.named_entities

sd = SampleData()
sd.sample_text_file()

# for s, w in ne_sets.items():
#     if w > 1:
#         print(w,s)

