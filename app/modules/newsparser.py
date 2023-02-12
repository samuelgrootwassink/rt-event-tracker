import requests, re, validators
import xml.etree.ElementTree as ET

ERROR_PARSING = 'The parser was unable to succesfully parse the feed or the feed was incomplete'

class NewsAggregator():
    
    def __init__(self):
        self._feeds = []
    
    
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
    
    
    def _html_strip(self, content:str):
        """
        Strip all HTML tags through RegEx, not sanitized.

        Args:
            content (str): String that needs to be stripped of HTML tags

        Returns:
            str: Stripped version of content that is returned
        """
        pattern = r'<[^>]+>'
        html_stripped_content = re.sub(pattern, '', content)
        return html_stripped_content
    
    
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

        if validators.url(rss_url) is True:
            content = requests.get(rss_url).content
            xml_feed = ET.fromstring(content)
        else:
             xml_feed = ET.parse(rss_url)
        tree = ET.ElementTree(xml_feed)
        root = tree.find('channel')
        feed_dict = dict()
        feed_dict['title'] = root.find('title').text
        feed_dict['lang'] = root.find('language').text
        feed_dict['items'] = []        
        items = root.findall('item')
        for item in items:
            title = item.find('title').text.strip()
            summary = "".join(item.find('description').itertext()).strip()
            html_stripped_summary = self._html_strip(summary)
            item_dict = {'title': title, 
                         'summary': html_stripped_summary
                         }
            feed_dict['items'].append(item_dict)
            
        if feed_dict['title'] is None or feed_dict['items'] == []:
            raise Exception(ERROR_PARSING)
        return feed_dict
        
       
    def aggregate(self, file_path:str):
        """
        Aggregates all feeds and saves them in list of feeeds. 

        Args:
            file_path (str): File path as to what file to turn into a set

        Raises:
            TypeError: Checks whether the provided argument is the correct type, namely a string
        """
        if isinstance(file_path, str) is False:
            raise TypeError()
        
        rss_url_set = self._file_to_set(file_path)
        
        for rss_url in rss_url_set:
            feed = self._parse_feed(rss_url)
            self._feeds.append(feed)
        
    

        
        