# Development Log

## 01-02-2023

Started working on news aggregator module with the **feedparser** module to aggregate news articles and put them through a sort of sorting algorithm.

> Sorting algorithm calculates weight per feed, after that looks for word occurences and tries to find all *named entities* and sort them to occurance. 

Found out however that the feedparser module does not seem to work with all rss feeds I want to use, therefore planning to use **XML** module instead and write a feedparser of my own. 

Besides that I realised that recognising *named entities* by using **RegEx** and building an algorithm of my own is way too complex to be able to get quality results that I will be start testing with **NLTK** instead.

Also using stopwords by **NLTK** instead of writing them by myself


## 06-02-2023

Starting with high level concept and idea, written in [README.md](/README.md)
Unclear what goal should be, after chat with ChatGPT clearer image. 

Website with geared towards end users being researchers & journalists that aggregates and sorts tweets according to current news events.

> Current news events being provided by a number or well established news sources, both international and regional

>Run script whenever one of the news sources has tweeted a tweet that contains a link to their website? 
Making sure the rss aggregate script does not have to run needlessly
**idea provided by Timothy**

Just read about NLTK VADER, which might be nice to use for twitter content


## 09-02-23

To handle the news parsing module of the application I am thinking of creating a NewsParser class that handles all parsing and returning of parsed news feeds for use in NER. 

In case I'd want to use the newsfeeds in other instances however storing them in objects would also not be a bad idea. 

New dilemma: Does the newsparser call the NER or the other way around. What will the NewsParser be used for: **Only to be run through
 NER**

The only things the Entry() class needs is therefore a title and description/summary as the rest of the information will not be used. 
Possibility to merge title and description but keeping them seperate may yield interesting information in the future.

```mermaid
classDiagram 
direction LR

class NewsParser{
    -feeds: set

    -file_to_set(file_path:str) set
    +parse_feed(url:str) dict
    +dict_feeds() dict
    
}


class Feed{
    +name: str
    +url: str
    -entries: set

    +process_entries(entries:set)
    +dict_entries() dict
}


class Entry{
    -title
    -description
    
    +dict_entry() dict
}

NewsParser  --> "0..*" Feed : has
Feed  --> "0..*" Entry : has

```
> Maybe parsing of certain feeds on certain signs is better than to parse them all together changing the classes to be NewsAggregate and spliting the parsing portion as NewsParser


```mermaid
classDiagram 
direction LR

class NewsParser{
    -file_to_set(file_path:str) set
    +parse_feed(url:str) dict
    
}

class NewsAggregator{
    -feeds: set
    +dict_feeds() dict

}

class Feed{
    +name: str
    +url: str
    -entries: set

    +process_entries(entries:set)
    +dict_entries() dict
}


class Item{
    -title
    -description
    
    +dict_entry() dict
}
NewsParser <-- NewsAggregator
NewsAggregator  --> "0..*" Feed : has
Feed  --> "0..*" Item : has

```

> **Side note for future reference**
> Havent thought about accessibility, might be handy for the front en dpart, maybe too much though...

## 11-02-2023
Started working on NewsParser() and tests, not resally sure whether creating own xml parser is best course of action but we will find out. In a sense it is a very simple parser that only needs to acess certain information, therefore handling it should not be too complex. 
Besides that: Creating a class for the parsing part might be too overkill and a functional programming approach would work better instead of OO.


NewsAggregator() and NewsParser() can once again be combined into one single class which then creates instances of Feed() and Item()

```mermaid
classDiagram 
direction LR

class NewsParser{
    -feeds: set

    -file_to_set(file_path:str) set
    +parse_feed(url:str) dict
    +dict_feeds() dict
    
}
```

## 12-02-23

Thinking I have maybe already overengineered something, namely the NewsAggregator() module that also contains a Feed class and Item class that I will likely not use and makes everything a bit more complex as it converts a dict into objects but for use by NER it converts these objects back into dicts....
Below what I had, stripping away the Feed and Item class
<details>
<summary>Code snippet with redundant classes</summary>

```
import requests, re, validators
import xml.etree.ElementTree as ET

ERROR_PARSING = 'The parser was unable to succesfully parse the feed or the feed was incomplete'

class Item():
    
    def __init__(self, title, summary):
        self.__title = title
        self.__summary = summary
    
    
    def to_dict(self):
        return {self.__title:self.__summary}
        


class Feed():
    
    def __init__(self, title, language):
        self.__title = title
        self.__language = language
        self.__items = []
    
    
    def add_item(self, item):
        
        self.__items.append(Item(item['title'], item['summary']))
        
    
    def to_dict(self):
        
        feed_dict = dict()
        feed_dict['title'] = self.__title
        feed_dict['language'] = self.__language
        feed_dict['items'] = [item.to_dict() for item in self.__items]
        
        return feed_dict


class NewsAggregator():
    
    def __init__(self):
        self._feeds = set()
    
    def _file_to_set(self, file_path:str):
        """
        Reads file from file_path and returns each line as an element of a set.
        Ignores comments '#' and empty lines

        Args:
            file_path (str): The file to be read

        Returns:
            set: A set with all lines of the read file
        """
        if not isinstance(file_path, str):
            raise TypeError
        
        set_of_file = set()
        
        with open(file_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                stripped_line = line.strip()
                if stripped_line == '':
                    continue
                elif stripped_line[0] == '#':
                    continue
                set_of_file.add(stripped_line)
        return set_of_file
    
    
    def _parse_feed(self, rss_url:str):
        """
        Parses a rss xml feed. Raises errors whenever the link provided is no .xml file or when the dictionary returned contains an empty title or items. Retrieves feed name, language and title and description from all items. Returns them in a neat dictionary
        
        Will only parse .xml file in rss feed structure as demonstrated here:
        https://www.w3schools.com/XML/xml_rss.asp

        Args:
            rss_url (str): Url or path proided from which to parse an XML document

        Returns:
            dict: Dictionary containing information regarding the feed and its items
        """
        
        xml_feed = rss_url
        if validators.url(rss_url) is True:
            if '.xml' not in rss_url:
                raise Exception('The url provided is not an .xml file')
            
            xml_feed = requests.get(rss_url).content

        tree = ET.parse(xml_feed)
        root = tree.getroot()
        
        feed_dict = dict()
        feed_dict['title'] = root.find('channel/title').text
        feed_dict['lang'] = root.find('channel/language').text
        feed_dict['items'] = []        
        items = root.findall('channel/item')
        
        for item in items:
            title = item.find('title').text.strip()
            summary = "".join(item.find('description').itertext()).strip()
            item_dict = {'title': title, 
                         'summary': summary
                         }
            feed_dict['items'].append(item_dict)
        
        if feed_dict['title'] is None or feed_dict['items'] == []:
            raise Exception(ERROR_PARSING)
        
        return feed_dict
        
       
    def aggregate(self, file_path:str):
        
        if isinstance(file_path, str) is False:
            raise TypeError()

        
        
```

</details>

Now starting with NER module as this will be called by the NewsAggregator() module to run through all feeds.

Still not sure whether I should assig any weights to NE yet.


## 13-02-23

Started reading up more about NLTK. It would do good when creating the NER to make two variants, one being for well organized and gramatically correct text and the other being for tweets for example as the pretrained models are mostly trained on properly written english.

As an alteration of the end product maybe it would do good to show the most talked about topics, (with links to news articles?) with corresponding tweets organized by sentiment (being positive or negative). If training the model is doable ofcourse, however VADER seems to be doing this exact trick, therefore not sure whether to try myself. 
Links for reference:
https://www.guru99.com/pos-tagging-chunking-nltk.html
https://towardsdatascience.com/intro-to-nltk-for-nlp-with-python-87da6670dde
https://realpython.com/python-nltk-sentiment-analysis/

Model for social media posts : VADER
Model for structured content: ?

In order to create the NER module I wish to create a class which has certain methods to be used by other modules. First off I wish to create a differentiation between the handling of structured text and social media text.
Below a graph detailing the struture of the class: 


```mermaid
graph LR

N(NER)
S(Structured text)
U(Unstructured text)

NE(Named Entities)
SE(Sentiment)


N --> S
N --> U
S --> NE
U --> NE
U --> SE
```

Usecase will be implementing this class in for example the newsparser module to extract named entities that can then be used for further processing.

How do I want to store the processed text, as a 
- Text formatting to remove punctuation and stopwords.
-



## 13-02-23

Experimented with the NLTK chunking and NER, noticed that by removing all stop words before determining NE it results in undesirable results.

Namely in this case:

```
without_stopword_removal = 'Troops blew up the bridge on Monday, according to a local Donetsk region news site. Ukraine denies it intends to leave Bakhmut, despite six months of heavy fighting and reportedly dwindling stockpiles.'
results = {'Donetsk', 'Bakhmut', 'Troops', 'Ukraine'}

with_stopword_removal = 'Troops blew bridge Monday , according local Donetsk region news site . Ukraine denies intends leave Bakhmut , despite six months heavy fighting reportedly dwindling stockpiles .'
results = {'Donetsk', 'Bakhmut', 'Troops'}

def named_entities(self, string:str):
    """
    Uses NLTK Part of Speech tagging and chunking to determine Named Entities in a string for further use.

    Args:
        string (str): The string to take a apart

    Returns:
        set: A set containing all recognized named entities
    """
    tokenized_string = word_tokenize(self.remove_stopwords(string))
    tagged_string =  pos_tag(tokenized_string)
    ne_tree = nltk.ne_chunk(tagged_string, binary=True)
    print(ne_tree)
    named_entities = set()
    
    for ne in ne_tree.subtrees(filter= lambda ne: ne.label() == 'NE'):
        named_entity = ' '.join([word[0] for word in ne])
        named_entities.add(named_entity)

    return named_entities

```

The results show that with removal of stopwords the name Ukraine is no longer identified as a NE, whilst being quite crucial in the context of the string.

Therefore I am considering doing NE without removal of stopwords, firstly for the above stated reason with a side note that most handled text will not be longer than 2-3 Sentences making it doable

Maybe the error has been that I pull entire pieces of text through the method instead of a single sentence. First need to test out
https://nlp.stanford.edu/software/crf-faq.shtml#a
https://pythonprogramming.net/chunking-nltk-tutorial/

```
text_list = sent_tokenize(self.remove_stopwords(string))
# Continue here, change post_tag to post_tag_sents
# tokenized_string = word_tokenize()
tagged_string =  post_tag_sents(text_list)
ne_tree = nltk.ne_chunk(tagged_string, binary=True)
print(ne_tree)
named_entities = set()
```

## 19-02-2023

First experiment with retrieving named entities from the guardian/international rss feed:
https://www.theguardian.com/international/rss

This is the current method

```
def named_entities(self, sentences:str):
        """
        Uses NLTK Part of Speech tagging and chunking to determine Named Entities in a string for further use.

        Args:
            string (str): The string to take a apart

        Returns:
            set: A set containing all recognized named entities
        """
        
        sentence_list = sent_tokenize(sentences)
        cleaned_sentences = [ self.remove_stopwords(sentence) for sentence in sentence_list]
        tokenized_sentence_list = [word_tokenize(sent) for sent in cleaned_sentences]
        tagged_sentence_list =  pos_tag_sents(tokenized_sentence_list)
        
        named_entities = set()
        for sent in tagged_sentence_list:
            tree = nltk.ne_chunk(sent, binary=True)
            for ne in tree.subtrees(filter= lambda ne: ne.label() == 'NE'):
                named_entity = ' '.join([word[0] for word in ne])
                named_entities.add(named_entity)
                
        return named_entities

```
<hr>


<details>
<summary> 
Results gathered by above method on the Guardian/International feed:
</summary>
{'Wang Yi', 'Toronto', 'Nosheen Iqbal', 'Paul Smith', 'Status Quo', 'Qatar', 'Ravi Jadeja Ravichandran Ashwin', 'Sasha', 'International Ski Snowboard Federation', 'Vital', 'Emmanuel Macron', 'Environmental Protection Agency', 'masksHow', 'Mahsa Amini', 'Proteo', 'Continue', 'Washington Post', 'Ovsyannikova', 'Consumption', 'Welcome Avoriaz', 'Jenny Slate', 'Peak District', 'Test Delhi', 'opportunityDivision', 'Arizona', 'exercisesNorth Korea', 'France', 'PRC', 'Brendon', 'Black Sea', 'Republican', 'Vladimir', 'Vermeer', 'Ghana', 'Half', 'Soave Orvieto', 'Alpine', 'London', 'Marcel Shell Shoes', 'Andrey', 'Italian Madrid', 'Tehran', 'Twelve', 'Modi', 'Cypriot', 'Discovery', 'Picture', 'Tarzan', 'Hezbollah', 'Ohio', 'London US', 'incidentAntony Blinken', 'Deborah Dorbert', 'Goalkeeper', 'Europe', 'updatesThe', 'Tom Symonds', 'Damascus', 'Athens', 'Fifa', 'Consumption France', 'Belarussian', 'StreetThe', 'Nigerian', 'Ukraine Middle Eastern African', 'UK', 'Ukrainian', 'Jiaxi', 'squanderWhen Nicola Sturgeon', 'Knesset Jerusalem', 'Joe Biden', 'familyThe', 'Munich', 'MatildasAustralia', 'enchantingAt Baftas', 'Rihanna Super Bowl', 'Istanbul', 'Covid', 'Heinali', 'Waitrose', 'Gavron', 'Norfolk', 'Patrick Stewart', 'ageFrance', 'Australian', 'Oscars', 'Marist College Canberra', 'Mexican', 'Castel', 'Antony Blinken', 'Bute House Edinburgh', 'DNA', 'Sheffield', 'Marina Ovsyannikova', 'British Academy', 'Hyundai Nexo', 'Bond', 'Iran International', 'Sleaford Mods', 'Optical Delusion', 'German', 'Echoes Times', 'Welsh', 'Van Gogh Frida Kahlo', 'Bafta', 'Data Goonies', 'Mike', 'Phil Paul Hartnoll', 'Shpudeiko', 'Turkish', 'Sam Patten', 'Carlo Ancelotti', 'Buhari', 'Liverpool', 'Kentucky', 'Bukky Bakray', 'Light', 'Tippett', 'Frascati', 'worldAs', 'Norway', 'Paris', 'themFollow', 'Mum', 'failuresUefa', 'Max Robertson', 'Cyclone Gabrielle New Zealand', 'Short', 'Food Monthly', 'South Africa', 'North Island', 'MPs', 'Legislation', 'Kyiv', 'Buckinghamshire', 'BBC Turkish', 'Jamie Demetriou', 'Russian', 'Nick Pope', 'Alun Wyn Jones', 'AKA Ukrainian', 'America', 'Moscow Nato', 'Syria', 'Anfield', 'Experience', 'Paolis Frascati', 'Parramatta', 'Louisville', 'Pyongyang', 'Libyan', 'BBC', 'Oscar', 'Champions League', 'Madrid', 'Uefa', 'Les Républicains', 'Carter Center', 'Spaniard', 'North Korea', 'Demetriou', 'Etonian', 'Six Nations', 'Romania', 'Liverpool St James', 'Shakin', 'Moscow', 'Waymond Wang Everything', 'wagesWarren Gatland', 'Ancelotti', 'explainsThe', 'Brother Jerome Hickman', 'Chris', 'Scotland', 'Sarah Gavron', 'Soviet', 'Fragile', 'Daniel Tulloch', 'Hawke', 'Lenin', 'Rafa Benítez', 'Enjoy', 'Tristan', 'Bavaria', 'Ringa', 'Bordeaux', 'Footballer Christian Atsu', 'Mohamed Salah', 'Nana Connie', 'Ingrid Fosse Sæthre', 'Sturgeon', 'Brittany Kaiser', 'Chris Hipkins', 'Narendra Modi', 'Stath', 'Dean', 'Vucic', 'Sunak', 'Benjamin Netanyahu', 'Australia', 'Italy', 'Iran Mahsa Amini', 'British', 'Omayyad', 'SNP', 'BordersMarina Ovsyannikova', 'Missouri', 'Composer Ricky Kej', 'David Smith', 'Newcastle', 'Boris Johnson', 'warRussia', 'Soleil', 'Ole House', 'Kamala Harris', 'Death', 'Kyiv Eternal', 'Germany', 'Indiana', 'devicesPurism', 'scientistThe', 'Welcome Country', 'Northland', 'Please', 'Scottish National', 'Scottish', 'AdıyamanAmid', 'Home', 'canBritish', 'Dunbar', 'East Palestine', 'BJP', 'China', 'European', 'Stephen Hough', 'EURishi Sunak', 'Paolis Frascati Superiore DOCG', 'Brexit', 'Zelensky', 'Hundreds', 'Northern Ireland', 'podcastFor', 'Israel', 'Shouts', 'US', 'Airbnb', 'Catholic', 'Avoriaz', 'Mardi Gras Fair', 'Truth Women', 'economyThe', 'Syria Turkey', 'Portes', 'ChatGPT', 'FIS', 'Orbital', 'Sue', 'Jamaican', 'Earth', 'Tolaga Bay', 'Harris', 'Chinese', 'David Hockney', 'Nigeria', 'India', 'Upper East', 'Better', 'Muriel Box', 'Charles', 'Lake Garda', 'IMF', 'TikTok', 'Macron', 'Mustafa Avci', 'Asian', 'saysJimmy Carter', 'Former', 'militantsAn Israeli', 'Michael Regan', 'Carabao Cup', 'New Zealand', 'Mariko Klug', 'Tesco Finest Soave Classico Superiore', 'ecDNA', 'Benball', 'Santarelli', 'Solkiki', 'James Cook', 'French', 'Putin', 'Harriet Harman', 'New York', 'Brazil', 'waterItaly', 'American', 'updatesAs', 'Turkey', 'Nick', 'Sydney', 'MorningRoutine', 'Debussy', 'Kiwi', 'Lamar Johnson', 'Volodymyr Zelenskiy', 'Bakhmut', 'updatesJoe Biden', 'illnessIn', 'Cher Yam Tian', 'Phobias', 'Cyclone Gabrielle', 'Radio', 'Alex Moshakis', 'Alexander Nix', 'lieLive', 'Cook', 'Caleb Blair', 'Guillermo', 'Dirty Rat', 'Muslims', 'Marcel', 'Florida', 'England', 'Observer', 'Mediaeval Baebes', 'Labour', 'Blinken', 'Aurélien Pradié', 'Spain', 'Vikram Dodd', 'Jami Cozza', 'Hough', 'Benítez', 'Nicola Sturgeon', 'South Korea', 'Anna', 'Born Cardiff', 'Indoor Built', 'Mitch McConnell', 'Toro', 'Green Door Merry Christmas Everyone', 'Olia Hercules', 'JohnsonThe', 'Jawaharlal Nehru University', 'moreDon', 'himThe', 'emailI', 'Nepali', 'Kanchan Gupta', 'custodyWe', 'France Continue', 'MargateAn', 'Norfolk Southern', 'Bulgaria', 'Dean Fleischer Camp Jenny Slate', 'Johnson', 'Londoner Bafta', 'Natasia', 'Kafr Sousa', 'Afraid', 'Harrison Ford', 'Whole Lifetime Jamie Demetriou', 'Severin Carrell', 'England Cardiff', 'Karan Rai', 'affectedCyclone Gabrielle', 'Poland', 'Sign', 'Dean Fleischer Camp', 'Tash', 'Israeli', 'Rachid', 'Passionate Stranger', 'Adıyaman', 'Joe Root', 'EnglandHave', 'McCullum', 'Shakespeare', 'Ben Stokes', 'Lucy Pardee', 'Veteran', 'Auckland Coromandel', 'Andrew Tate', 'Banksy', 'Gabrielle New Zealand', 'Senate', 'Italian', 'Syrian', 'Iranian', 'Guardian', 'Iran', 'DeWine', 'Stath Lets Flats', 'cerealGet', 'Tal Hanan', 'Phoenix', 'Rachel Signer', 'Arab', 'Russia', 'EU', 'Gujarat', 'South Carolina', 'updatesGet', 'NHS', 'Regan', 'Vladimir Putin', 'Moon Princess', 'Qatari', 'Guardian Australia', 'Bakray', 'Mihir Shukla', 'English Test', 'Netflix', 'Britain', 'Ofsted', 'Ukraine', 'Federico Mompou', 'Madrid Champions League', 'France Switzerland', 'Japanese', 'Kherson', 'Google', 'Klaveness', 'Ukraine Continue'}
</details>
<hr>


The results clearly show that there *needs* to be a lot of finetuning, starting with maybe weighting the retrieved NE and seeing if there is a way to filter *faulty* NE or whether this is not needed as they will not appear on top when weighted.

Lot to consider and for accuracy a failsafe would be appropriate to remove incorrect NE

NLTK offers FreqDist for the weighting ot NE but since what I will need is not a lot of added functionality I rather add my own method the NER class than import FreqDist

Encountered a problem, where to place a frequency destribution check

By adding a custom frequency check this is the following result:

```
>> in
def common_entities(self, named_entities, amount: int = 10):
        
    ne_dict = dict()
    for entity in named_entities:
        ne_dict[entity] = ne_dict.get(entity, 0) + 1
    
    common_entities = sorted(ne_dict, key = lambda key: ne_dict.get(key), reverse=True)
    
    return common_entities[:amount]


>> out
['Continue', 'Russian', 'London', 'Guardian', 'US', 'Ukraine', 'Labour', 'Vladimir Putin', 'updatesThe', 'EU']
```

What now seems to be the issue is that certain unimportant words are included, therefore recognizing named entities needs to be corrected, maybe by changing the model or corpus or narrowing criteria.

The stripping of rss feed tet needs to be more thorough and thaught about. Although the results match up with what I am seeing on the guardian/international feed the amount of incorrect words is still mor the I like to admit. I think this has to do with how I parse feeds.

The Guardian feeds features a lot of the word 'Guardian':p


## 20-02-2023

Refactor of the newsparser module, to decrease complexity of the module I will add another class called Item(),
This way every item parsed from rss feeds gets it own objects with its own methods to determine relations and NE.
The inclusion of a Feed() object to relate their origin will also be included to weigh the amount of items produced by each feed.


## 01-03-2023

Instead of checking for single NE we are now going to check for sets of NE so that sets of NE are then run through Twitter to get a more narrow result list (that being the plan).
This however requires a method that check how many two sets are the same, and to set for example a treshold of 80%. If sets contain this or higher percentage of the same values the weigh is increased (maybe the larger set is then being used?). Or the set that contains the most overlapping words is used.

## 03-03-2023

After some experimentation I figured out there were more types of xml feeds used by news websites, nameluy also rdf feeds. Therefore I am splitting the _parse_feed() into two for respectively rdf & rss

At east the part for the rss feeds seems to work as well as the rdf xml feeds. Now acceptig that the NER is not a 100 percent but continuing on the common_entity_sets() method.

## 12-03-2023

Started fixing some issues and working on full test coverage. Still not completed due to new way of parsing feeds with different methods.
Still need to create test coverage.

## 13-03-2023

Methods that returns common entity sets in a dictionary. Whenever an identical set is found the weight is increased by one, whenever a set is more than 50% identical a value between 0.1 and 0.9 is added (per 10% 0.2 weight is added).

Maybe a tershold of 80% identitcal would be more valuable as any lower can create a misinterpretation of data as a match of 50% does not mean a lot. This also means that of 5 words in a set 4 need to be identical raising the chances the added word only expands on the subject instead of talking about something unrelated

I need to add a lemmatizer to the named entities method to prevent almost duplicate words from entering the NE sets for more accurate results

## 15-03-2023

Updated the common_entity_sets() roughly to compare sets and add any that have a similarity of 80% or above, want to change the mothod to easily change this percentage and the weight added according to specific similarity. Now any similarity above 80% adds a weight of 0.5. Identical sets add to a weight of 1.

Added a small class called SampleData() that takes a sample of the parsed news data and their respective named entities for manual comparison and writes it to a txt file, to check whether the ner works as expected.

After creating two samples to manually check with around 10-15 samples each I have come to the conclusion that what I want to extract out of the text only matches for around 60-70% of what my ner algorithm catches. 
Now seeing what I should change, extended my tests to include some of the failed manual samples and see where the problem lies, whether it is the preprocessing, the nlm or something else.