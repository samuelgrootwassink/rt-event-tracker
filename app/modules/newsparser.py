import requests, re
import xml.etree.ElementTree as ET

class NewsParser():
    
    def file_to_set(self, file_path:str):
        """
        Reads file from file_path and returns each line as an element of a set.
        Ignores comments '#' and empty lines

        Args:
            file_path (str): The file to be read

        Returns:
            set: A set with all lines of the read file
        """
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
    
    
    # def parse_feed(self, rss_url:str):
    #     """
    #     Parses a rss feed url and returns the content in a dictionary with a feed title and provided entries title and summary. s

    #     Args:
    #         url (str): The url to parse
    #     """
        
    #     html_pattern = '<[^<]+?>'
        
    #     xml_feed = requests.get(rss_url).content
    #     tree = ET.parse(xml_feed)
    #     root = tree.getroot()
    #     re.sub(html_pattern, '', summary)
       
                