import requests
import re
import xml.etree.ElementTree as ET
import modules.ner as ner
from unidecode import unidecode

ERROR_PARSING = 'The parser was unable to succesfully parse the feed or the feed was incomplete'
DEFAULT_PATH = 'modules/files/news_feeds.txt'


class Item():

    def __init__(self, feed, title, description):
        self._feed = feed
        self._title = title
        self._description = description
        self._content = f'{title.strip("?!.;")}. {description}'

    @property
    def title(self):
        return self._title


    @property
    def description(self):
        return self._description


    @property
    def weight(self):
        return self._feed.weight()

    
    @property
    def content(self):
        return self._content
    
    
    def to_dict(self):
        """
        Returns a dict of all the information contained by an Item() instance

        Returns:
            dict: Dict containing all info
        """
        return {'title': self._title, 'description': self._description, 'content': self._content}


class Feed():

    def __init__(self, title, language):
        self._title = title
        self._language = language
        self._items = []


    @property
    def title(self):
        return self._title


    @property
    def language(self):
        return self._language


    @property
    def items(self):
        return self._items


    def _already_exists(self, title):
        """
        Checks whether an Item() instance allready exists, returns a boolean value

        Args:
            title (str): Title of a specific Item()

        Returns:
            bool: Whether an item with this title already exists in this feed
        """
        existing_titles = {item.title.lower() for item in self._items}
        if title.lower() in existing_titles:
            return True
        return False


    def add_item(self, item):
        """
        Adds an Item() instance to this feed instance

        Args:
            item (tuple): The item that is parsed from a an xml feed
        """
        title, description = item
        if self._already_exists(title):
            return

        self._items.append(Item(self, title, description))


    def to_dict(self):
        """
        Converts the feed information and its items to a dictionary

        Returns:
            dict: Dictioary containing all feed information
        """
        feed_dict = {'title': self._title,
                     'language': self._language,
                     'items': [item.to_dict() for item in self._items]}

        return feed_dict


class NewsAggregator():

    def __init__(self):
        self._feeds = []
        self._ner = ner.NER()


    def _file_to_set(self, file_path: str):
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


    def _html_strip(self, content: str):
        """
        Strip all HTML tags through RegEx, not sanitized.

        Args:
            content (str): String that needs to be stripped of HTML tags

        Returns:
            str: Stripped version of content that is returned
        """
        pattern = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        html_stripped_content = re.sub(
            pattern, ' ', content).replace('  ', ' ').strip()
        return html_stripped_content


    def _remove_accents(self, content: str):
        """
        Replaces all accented characters for later text processing

        Args:
            content (str): Content that needs to be checked for accented characters

        Returns:
            str: String with 'all' (In english language) accented characters replaced
        """
        s = unidecode(content, "utf-8")
        return unidecode(s)


    def _clean(self, content: str):
        """
        Handles the cleaning of strings by replacing accented characters, stripping html, 

        Args:
            content (str): Content that needs to be cleaned

        Returns:
            str: Cleaned string
        """
        unaccented_content = self._remove_accents(content)
        clean_content = self._html_strip(unaccented_content)
        return clean_content


    def _parse_rdf(self, tree: ET.ElementTree, root: ET.Element):
        """
        Provides the information needed by the _parse_feed() method to succesfully parse a RDF feed

        Args:
            tree (ET.ElementTree): The tree containing all information
            root (ET.Element): The root item from whic to start working

        Returns:
            Feed: A feed instance containing all parsed data
        """
        RDF_NS = {
            'xmlns': 'http://purl.org/rss/1.0/',
            'xmlns:rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
            'xmlns_dc': 'http://purl.org/dc/elements/1.1/',
            'xmlns:sy': 'http://purl.org/rss/modules/syndication/',
            'xmlns:content': 'http://purl.org/rss/1.0/modules/content/',
            'xmlns:dwsyn': 'http://rss.dw.com/syndication/dwsyn/'
        }
        PATH_OPTIONS_RDF = {
            'title': ['xmlns:title', 'xmlns:channel/xmlns:title'],
            'language': ['xmlns:language', 'xmlns:channel/xmlns:language'],
            'items': ['xmlns:item'],
            'item_title': ['xmlns:title'],
            'item_description': ['xmlns:description']
        }

        return self._parse_feed(tree, root, PATH_OPTIONS_RDF, RDF_NS)


    def _parse_rss(self, tree: ET.ElementTree, root: ET.Element):
        """
        Provides the information needed by the _parse_feed() method to succesfully parse a RSS feed

        Args:
            tree (ET.ElementTree): The tree containing all information
            root (ET.Element): The root item from whic to start working

        Returns:
            Feed: A feed instance containing all parsed data
        """
        PATH_OPTIONS_RSS = {
            'title': ['title', 'channel/title'],
            'language': ['language', 'channel/language'],
            'items': ['item', 'channel/item'],
            'item_title': ['title'],
            'item_description': ['description']
        }

        return self._parse_feed(tree, root, PATH_OPTIONS_RSS)


    def _parse_feed(self, tree: ET.ElementTree, root: ET.Element, path_options: dict, ns: dict = {}):
        """
        Parses the feed provided it has the correct paths/ namespaces

        Args:
            tree (ET.ElementTree): The tree containing all information
            root (ET.Element): The root item from whic to start working
            path_options (dict): Path options that need to be checked in order to get to the good stuff that we want
            ns (dict, optional): Namespaces needed for handling RDF feeds. Defaults to {}.

        Returns:
            Feed: A feed instances with all the parsed iniformation
        """
        for path in path_options['title']:
            title = root.find(path, ns)
            if title != None:
                title = title.text
                break

        for path in path_options['language']:
            language = root.find(path, ns)
            if language != None:
                language = language.text
                break

        for path in path_options['items']:
            items = root.findall(path, ns)
            if items != []:
                break
        feed = Feed(title, language)
        for item in items:
            for path in path_options['item_title']:
                item_title = item.find(path, ns)
                if item_title != None:
                    item_title = item_title.text
                    break
            for path in path_options['item_description']:
                item_description = item.find(path, ns)
                if item_description != None:
                    item_description = ''.join(
                        item.find(path, ns).itertext()).strip()
                    break
            item_description = self._clean(item_description)
            feed.add_item((item_title, item_description))

        return feed


    def _generate_feed(self, rss_url: str):
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
            tree = ET.ElementTree(ET.fromstring(content))
        else:
            print('wrong')
            tree = ET.parse(rss_url)

        root = tree.getroot()

        feed = dict()
        if 'rdf' in root.tag.lower():
            feed = self._parse_rdf(tree, root)
        else:
            # assuming that else the feed is a rss feed
            feed = self._parse_rss(tree, root)

        if feed.title is None or feed.items == []:
            raise Exception(ERROR_PARSING)
        return feed


    @property
    def named_entities(self):
        """
        Retrives named entities from all feed items that are stored within the NewsAggregator() instance

        Returns:
            set: All encountered named entities
        """
        named_entity_list = []
        for feed in self._feeds:
            for item in feed.items:

                ne_set = self._ner.named_entities(item.content)
                named_entity_list.append(ne_set)

        common_entity_sets = self._ner.common_entity_sets(named_entity_list)

        return common_entity_sets


    def aggregate(self, file_path: str = DEFAULT_PATH):
        """
        Aggregates all feeds and saves them in list of feeeds. 

        Args:
            file_path (str): File path as to what file to turn into a set

        Raises:
            TypeError: Checks whether the provided argument is the correct type, namely a string
        """
        rss_url_set = self._file_to_set(file_path)
        for rss_url in rss_url_set:
            feed = self._generate_feed(rss_url)
            self._feeds.append(feed)

    def to_dict(self):
        """
        Returns a list containing a dictionary for each feeds and it's items

        Returns:
            list: A list filled with dictionaries
        """
        return [feed.to_dict() for feed in self._feeds]
