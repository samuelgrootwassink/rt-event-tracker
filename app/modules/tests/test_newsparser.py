import unittest
from modules.feedparser_lib import *

# parse feeds into dictionary


class TestNewsParser(unittest.TestCase):
    
    second
    def test_file_to_set(self):
        """
        Checks whether the text_to_set functions properly, leaves out any whitespaces and #comments. Also checks whether the correct type is returned
        """
        
        contol_results = set('https://test1.com','http://test2.org','www.test3.tech')
        test_results = NewsParser.file_to_set('app/modules/tests/test_files/test_file_to_set.txt')
        
        self.assertEquals(test_results, results)
        self.assertIsInstance(test_results, set)
        self.assertEquals(NewsParser.file_to_set('app/non_existant_file.txt'), FileNotFoundError)


    
