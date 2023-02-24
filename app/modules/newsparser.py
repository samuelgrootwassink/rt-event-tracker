import requests, re
import xml.etree.ElementTree as ET
import modules.ner as ner

ERROR_PARSING = 'The parser was unable to succesfully parse the feed or the feed was incomplete'
DEFAULT_PATH = 'modules/files/news_feeds.txt'


class Item():
    
    
class NewsAggregator():
    
    def __init__(self):
        self._feeds = {}
        self._ner = ner.NER()
    
    
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
    
    
    def _is_url(self, string: str):
        """
        Checks wether a string is a url
        Very barebones, only checks if contains:
        http
        https

        Args:
            string (str): Provide a string and check wether it is a url

        Returns:
            bool: Whether it is found to be a url
        """
        for prefix in ['http://', 'https://']:
            if prefix in string:
                return True
            
        return False
    
    def _html_strip(self, content:str):
        """
        Strip all HTML tags through RegEx, not sanitized.

        Args:
            content (str): String that needs to be stripped of HTML tags

        Returns:
            str: Stripped version of content that is returned
        """
        pattern = r'<[^<]+?>'
        html_stripped_content = re.sub(pattern, '', content)
        return html_stripped_content
    
    
    def _clean(self, content):
        
        html_stripped = self._html_strip(content)
        
        return html_stripped
    
    def _parse_feed(self, rss_url:str):
        """
        Parses a rss xml feed. Raises error the dictionary returned contains an empty title or items list. Retrieves feed name, language and title and description from all items. Returns them in a neat dictionary
        
        Will only parse .xml file in rss feed structure as demonstrated here:
        https://www.w3schools.com/XML/xml_rss.asp

        Args:
            rss_url (str): Url or path proided from which to parse an XML document

        Raises:
            Exception: The second exception raised is whenever the feed that is to be returned is incomplete therefore indicating either a parsing error or a broken feed.

        Returns:
            dict: Dictionary containing information regarding the feed and its items
        """

        if self._is_url(rss_url) is True:
            content = requests.get(rss_url).content
            xml_feed = ET.fromstring(content)
        else:
             xml_feed = ET.parse(rss_url)
        tree = ET.ElementTree(xml_feed)
        root = tree.getroot()
        # working here, checking how to handle different types of rss feeds, check guardian and deutche welle
        title = root.find('channel/title').text
        lang = root.find('language').text
        
        feed = Feed(title, lang)  
        items = root.findall('channel/item')
        for item in items:
            title = item.find('title').text.strip()
            summary = "".join(item.find('description').itertext()).strip()
            html_stripped_summary = self._clean(summary)
            item_dict = {'title': title, 
                         'summary': html_stripped_summary
                         }
            feed_dict['items'].append(item_dict)
            
        if feed_dict['title'] is None or feed_dict['items'] == []:
            raise Exception(ERROR_PARSING)
        return feed_dict
        
    @property
    def named_entities(self):
        """
        Retrives named entities from all feed items that are stored within the NewsAggregator() instance

        Returns:
            set: All encountered named entities
        """
        # change set into list and apply common entities method to return the most popular entities for further manipulation?
        named_entity_list = []
        for feed in self._feeds:
            for entry in feed['items']:
                
                ne_set = self._ner.named_entities(entry['summary'])
                print(1, ne_set)
                named_entity_list += ne_set
                
        common_entities = self._ner.common_entities(named_entity_list)
        
        return common_entities
            
       
    def aggregate(self, file_path:str = DEFAULT_PATH):
        """
        Aggregates all feeds and saves them in list of feeeds. 

        Args:
            file_path (str): File path as to what file to turn into a set

        Raises:
            TypeError: Checks whether the provided argument is the correct type, namely a string
        """
        rss_url_set = self._file_to_set(file_path)
        for rss_url in rss_url_set:
            feed = self._parse_feed(rss_url)
            self._feeds.append(feed)
        
    
    
        
class Feed():
    
    pass